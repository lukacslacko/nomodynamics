/* xcensus.c -- complete census engine for 2-D cross-amendment nomodynamics.
 *
 * Board: 64 bits (x) x 64 rows (y), one uint64 per row per kind, with one
 * guard row above and below.  The state is renormalised every step so that
 * min x = 1 and min y = 1; a pattern wider/taller than 60 is declared ESCAPE.
 * Canonical hashing of the normalised planes gives exact certificates for
 * FIXED / BALANCED / CYCLE / GLIDER; anything else is ESCAPE or UNRESOLVED.
 *
 * Semantics identical to xnomos.py / xa2d.py (verified by cross-check).
 *
 * build:  clang -O3 -march=native -pthread -o xcensus xcensus.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <pthread.h>
#include <stdarg.h>
#include <math.h>

#define NK 3
#define NROW 68
#define ORG 2          /* normalised min index (x bit and y row) */
#define MAXSPAN 59
#ifndef TBITS
#define TBITS 16
#endif
#define TSIZE (1 << TBITS)

/* offsets: O E W N S NE NW SE SW */
static const int OX[9] = {0, 1, -1, 0, 0, 1, -1, 1, -1};
static const int OY[9] = {0, 0, 0, 1, -1, 1, 1, -1, -1};
static const char *ONM = "OEWNSPQRT";

typedef struct {
    int n;                 /* kinds */
    int a[NK], b[NK], c[NK];   /* offset indices */
    int tgt[NK];           /* bitmask of target kinds */
} Univ;

typedef struct {
    uint64_t p[NK][NROW];
} Board;

/* verdicts */
enum { V_EXTINCT, V_FIXED, V_BALANCED, V_CYCLE, V_GLIDER, V_ESCAPE,
       V_UNRES, V_NVERD };
static const char *VNM[] = {"extinct", "fixed", "balanced", "cycle",
                            "glider", "escape", "unres"};

typedef struct {
    int verdict, t0, period, dx, dy, card, maxcard, tend, nactive;
} Res;

static inline uint64_t shx(uint64_t w, int dx) {
    return dx >= 0 ? (w >> dx) : (w << (-dx));
}
static inline uint64_t emx(uint64_t w, int cx) {
    return cx >= 0 ? (w << cx) : (w >> (-cx));
}

static int popall(const Board *B, int n) {
    int s = 0;
    for (int k = 0; k < n; k++)
        for (int y = 0; y < NROW; y++) s += __builtin_popcountll(B->p[k][y]);
    return s;
}

/* one synchronous step; sem 0 = parity, 1 = or.  returns number of active laws */
static int stepB(Board *B, const Univ *U, int sem, int *nact_out) {
    uint64_t occ[NROW], tog[NK][NROW], act[NROW];
    int n = U->n, nact = 0;
    for (int y = 0; y < NROW; y++) {
        uint64_t o = 0;
        for (int k = 0; k < n; k++) o |= B->p[k][y];
        occ[y] = o;
    }
    memset(act, 0, sizeof(act));
    memset(tog, 0, sizeof(uint64_t) * NK * NROW);
    for (int k = 0; k < n; k++) {
        int ax = OX[U->a[k]], ay = OY[U->a[k]];
        int bx = OX[U->b[k]], by = OY[U->b[k]];
        int cx = OX[U->c[k]], cy = OY[U->c[k]];
        int any = 0;
        for (int y = 1; y < NROW - 1; y++) {
            uint64_t la = shx(occ[y + ay], ax);
            uint64_t lb = shx(occ[y + by], bx);
            uint64_t w = B->p[k][y] & la & ~lb;
            act[y] = w;
            if (w) { any = 1; nact += __builtin_popcountll(w); }
        }
        if (!any) continue;
        for (int y = 1; y < NROW - 1; y++) {
            if (!act[y]) continue;
            uint64_t e = emx(act[y], cx);
            int yy = y + cy;
            if (sem >= 2) { tog[k][yy] |= e; continue; }
            for (int t = 0; t < n; t++)
                if (U->tgt[k] & (1 << t)) {
                    if (sem) tog[t][yy] |= e; else tog[t][yy] ^= e;
                }
        }
    }
    int changed = 0;
    if (sem >= 2) {
        /* SUPERSESSION: an active law of kind k enacts kind k at i+c_k when
         * that cell is EMPTY, and otherwise CLEARS the whole cell.  Clear
         * votes resolve by parity (sem==2) or by OR (sem==3).  Targets are
         * ignored by design -- enactment is own-kind (cf. xnomos._step_super). */
        uint64_t cleared[NROW];
        for (int y = 0; y < NROW; y++) {
            uint64_t c = 0;
            for (int k = 0; k < n; k++) {
                uint64_t hit = tog[k][y] & occ[y];
                if (sem == 3) c |= hit; else c ^= hit;
            }
            cleared[y] = c;
        }
        for (int k = 0; k < n; k++)
            for (int y = 0; y < NROW; y++) {
                uint64_t nw = (B->p[k][y] & ~cleared[y]) | (tog[k][y] & ~occ[y]);
                if (nw != B->p[k][y]) { B->p[k][y] = nw; changed = 1; }
            }
        if (nact_out) *nact_out = nact;
        return changed;
    }
    for (int k = 0; k < n; k++)
        for (int y = 0; y < NROW; y++)
            if (tog[k][y]) { B->p[k][y] ^= tog[k][y]; changed = 1; }
    if (nact_out) *nact_out = nact;
    return changed;
}

/* normalise so that min x = 1, min y = 1.  returns 0 if empty, -1 if too big,
 * else 1, writing the applied shift into (*sx,*sy)                       */
static int normB(Board *B, int n, int *sx, int *sy) {
    uint64_t all = 0;
    int ymin = -1, ymax = -1;
    for (int y = 0; y < NROW; y++) {
        uint64_t o = 0;
        for (int k = 0; k < n; k++) o |= B->p[k][y];
        if (o) { if (ymin < 0) ymin = y; ymax = y; all |= o; }
    }
    if (!all) return 0;
    int xmin = __builtin_ctzll(all);
    int xmax = 63 - __builtin_clzll(all);
    if (xmax - xmin > MAXSPAN || ymax - ymin > MAXSPAN) return -1;
    int dy = ORG - ymin, dx = ORG - xmin;
    *sx = -dx; *sy = -dy;                    /* anchor moved by (-dx,-dy) */
    if (dx || dy) {
        for (int k = 0; k < n; k++) {
            uint64_t tmp[NROW];
            memset(tmp, 0, sizeof(tmp));
            for (int y = ymin; y <= ymax; y++) {
                uint64_t w = B->p[k][y];
                if (!w) continue;
                tmp[y + dy] = dx >= 0 ? (w << dx) : (w >> (-dx));
            }
            memcpy(B->p[k], tmp, sizeof(tmp));
        }
    }
    return 1;
}

static inline uint64_t mix64(uint64_t x) {
    x ^= x >> 30; x *= 0xbf58476d1ce4e5b9ULL;
    x ^= x >> 27; x *= 0x94d049bb133111ebULL;
    x ^= x >> 31; return x;
}

/* avalanche hash: a one-bit change in any word changes ~half the bits, so the
 * exact cancellation that FNV-1a suffers here cannot occur. */
static uint64_t hashB(const Board *B, int n) {
    uint64_t h = 0x243f6a8885a308d3ULL;
    for (int k = 0; k < n; k++)
        for (int y = 0; y < NROW; y++) {
            uint64_t w = B->p[k][y];
            if (!w) continue;
            h ^= mix64(w * 0x9E3779B97F4A7C15ULL
                       + (uint64_t)(k * NROW + y) * 0xD6E8FEB86659FD93ULL);
            h = mix64(h);
        }
    return h;
}

typedef struct { uint64_t h; int t, ax, ay; uint32_t gen; } Ent;
static __thread Ent tab[TSIZE];
static __thread uint32_t curgen = 0;

static int TRACE = 0;
static void run(const Univ *U, const int *seed, int nseed, int sem,
                int maxsteps, int maxcard, Res *R) {
    Board B;
    memset(&B, 0, sizeof(B));
    for (int i = 0; i < nseed; i++) {
        int x = seed[3 * i], y = seed[3 * i + 1], k = seed[3 * i + 2];
        if (k >= U->n) continue;
        B.p[k][y + 20] |= 1ULL << (x + 20);
    }
    if (++curgen == 0) { memset(tab, 0, sizeof(tab)); curgen = 1; }
    uint32_t gen = curgen;
    int ax = 0, ay = 0, maxc = 0;
    R->verdict = V_UNRES; R->t0 = R->period = R->dx = R->dy = 0;
    R->nactive = 0;
    for (int t = 0; t <= maxsteps; t++) {
        int sx, sy, st = normB(&B, U->n, &sx, &sy);
        if (st == 0) { R->verdict = V_EXTINCT; R->tend = t; R->card = 0; return; }
        if (st < 0) { R->verdict = V_ESCAPE; R->tend = t; R->card = popall(&B, U->n);
                      R->maxcard = maxc; return; }
        ax += sx; ay += sy;
        int c = popall(&B, U->n);
        if (c > maxc) maxc = c;
        if (c > maxcard) { R->verdict = V_ESCAPE; R->tend = t; R->card = c;
                           R->maxcard = maxc; return; }
        if (TRACE) {
            uint64_t all = 0; int ymin=-1, ymax=-1;
            for (int y = 0; y < NROW; y++) { uint64_t o=0;
                for (int k=0;k<U->n;k++) o|=B.p[k][y];
                if (o){ if(ymin<0) ymin=y; ymax=y; all|=o; } }
            fprintf(stderr, "t=%d card=%d x[%d..%d] y[%d..%d] h=%llx\n", t, c,
                    all?__builtin_ctzll(all):-1, all?63-__builtin_clzll(all):-1,
                    ymin, ymax, (unsigned long long)hashB(&B, U->n));
        }
        uint64_t h = hashB(&B, U->n);
        int idx = (int)(h & (TSIZE - 1));
        while (tab[idx].gen == gen && tab[idx].h != h) idx = (idx + 1) & (TSIZE - 1);
        if (tab[idx].gen == gen && tab[idx].h == h) {
            int p = t - tab[idx].t;
            int ddx = ax - tab[idx].ax, ddy = ay - tab[idx].ay;
            R->t0 = tab[idx].t; R->period = p; R->dx = ddx; R->dy = ddy;
            R->card = c; R->maxcard = maxc; R->tend = t;
            if (ddx == 0 && ddy == 0) {
                if (p == 1) {
                    int na = 0; Board tmp = B;
                    stepB(&tmp, U, sem, &na);
                    R->nactive = na;
                    R->verdict = na ? V_BALANCED : V_FIXED;
                } else R->verdict = V_CYCLE;
            } else R->verdict = V_GLIDER;
            return;
        }
        tab[idx].h = h; tab[idx].t = t; tab[idx].ax = ax; tab[idx].ay = ay;
        tab[idx].gen = gen;
        if (t == maxsteps) { R->card = c; R->maxcard = maxc; R->tend = t; return; }
        stepB(&B, U, sem, NULL);
    }
}


/* ---------------------------------------------------------------- alpha --
 * 256-bit-wide x 260-row board, seed at centre; measures the growth exponent
 * alpha from a least-squares fit of log|S_t| against log t, plus the fill
 * fraction of the bounding box at the end of the run.                      */
#ifndef AW
#define AW 4
#endif
#ifndef AH
#define AH 260
#endif
#ifndef ATMAX
#define ATMAX 120
#endif
#define ACX ((AW*64)/2)
#define ACY (AH/2)
typedef struct { uint64_t p[NK][AH][AW]; } BigB;

static inline void rsh(const uint64_t *src, uint64_t *dst, int s) {
    if (s == 0) { for (int i = 0; i < AW; i++) dst[i] = src[i]; return; }
    if (s > 0) {                                   /* dst bit x = src bit x+1 */
        for (int i = 0; i < AW; i++)
            dst[i] = (src[i] >> 1) | (i + 1 < AW ? src[i + 1] << 63 : 0);
    } else {                                       /* dst bit x = src bit x-1 */
        for (int i = AW - 1; i >= 0; i--)
            dst[i] = (src[i] << 1) | (i > 0 ? src[i - 1] >> 63 : 0);
    }
}

static __thread int ASIZES[ATMAX+2], ANT;
static double alpha_run(const Univ *U, const int *seed, int nseed, int sem,
                        double *fill_out, int *size_out, int *bbw, int *bbh) {
    static __thread BigB B;
    static __thread uint64_t occ[AH][AW], tog[NK][AH][AW], act[AH][AW];
    memset(&B, 0, sizeof(B));
    for (int i = 0; i < nseed; i++) {
        int x = seed[3*i] + ACX, y = seed[3*i+1] + ACY, k = seed[3*i+2];
        if (k >= U->n) continue;
        B.p[k][y][x >> 6] |= 1ULL << (x & 63);
    }
    static __thread int sizes[ATMAX + 1];
    int T = 0;
    for (int t = 0; t <= ATMAX; t++) {
        int sz = 0;
        for (int k = 0; k < U->n; k++)
            for (int y = 0; y < AH; y++)
                for (int i = 0; i < AW; i++) sz += __builtin_popcountll(B.p[k][y][i]);
        sizes[t] = sz; T = t;
        if (!sz) break;
        if (t == ATMAX) break;
        for (int y = 0; y < AH; y++) {
            for (int i = 0; i < AW; i++) {
                uint64_t o = 0;
                for (int k = 0; k < U->n; k++) o |= B.p[k][y][i];
                occ[y][i] = o;
            }
        }
        memset(tog, 0, sizeof(tog));
        for (int k = 0; k < U->n; k++) {
            int ax = OX[U->a[k]], ay = OY[U->a[k]];
            int bx = OX[U->b[k]], by = OY[U->b[k]];
            int cx = OX[U->c[k]], cy = OY[U->c[k]];
            int any = 0;
            for (int y = 1; y < AH - 1; y++) {
                uint64_t la[AW], lb[AW];
                rsh(occ[y + ay], la, ax);
                rsh(occ[y + by], lb, bx);
                uint64_t any2 = 0;
                for (int i = 0; i < AW; i++) {
                    act[y][i] = B.p[k][y][i] & la[i] & ~lb[i];
                    any2 |= act[y][i];
                }
                if (any2) any = 1;
            }
            for (int i = 0; i < AW; i++) { act[0][i] = 0; act[AH-1][i] = 0; }
            if (!any) continue;
            for (int y = 1; y < AH - 1; y++) {
                uint64_t e[AW]; int nz = 0;
                for (int i = 0; i < AW; i++) nz |= (act[y][i] != 0);
                if (!nz) continue;
                rsh(act[y], e, -cx);
                int yy = y + cy;
                for (int tt = 0; tt < U->n; tt++)
                    if (U->tgt[k] & (1 << tt))
                        for (int i = 0; i < AW; i++) {
                            if (sem) tog[tt][yy][i] |= e[i];
                            else tog[tt][yy][i] ^= e[i];
                        }
            }
        }
        for (int k = 0; k < U->n; k++)
            for (int y = 0; y < AH; y++)
                for (int i = 0; i < AW; i++) B.p[k][y][i] ^= tog[k][y][i];
        /* border guard: stop if the pattern reaches within 4 of the frame */
        int hit = 0;
        for (int k = 0; k < U->n && !hit; k++) {
            for (int y = 0; y < 4; y++)
                for (int i = 0; i < AW; i++) if (B.p[k][y][i] | B.p[k][AH-1-y][i]) hit = 1;
            for (int y = 0; y < AH; y++)
                if ((B.p[k][y][0] & 0xffULL) || (B.p[k][y][AW-1] & (0xffULL << 56))) hit = 1;
        }
        if (hit) { T = t + 1;
                   int sz2 = 0;
                   for (int k = 0; k < U->n; k++) for (int y = 0; y < AH; y++)
                       for (int i = 0; i < AW; i++) sz2 += __builtin_popcountll(B.p[k][y][i]);
                   sizes[T] = sz2; break; }
    }
    for (int t = 0; t <= T; t++) ASIZES[t] = sizes[t];
    ANT = T;
    /* bounding box + fill */
    int xmin = 1 << 20, xmax = -1, ymin = 1 << 20, ymax = -1, cells = 0;
    for (int y = 0; y < AH; y++) {
        uint64_t r[AW]; int nz = 0;
        for (int i = 0; i < AW; i++) {
            uint64_t o = 0;
            for (int k = 0; k < U->n; k++) o |= B.p[k][y][i];
            r[i] = o; nz |= (o != 0);
        }
        if (!nz) continue;
        if (ymin > y) ymin = y;
        ymax = y;
        for (int i = 0; i < AW; i++) if (r[i]) {
            int lo = i * 64 + __builtin_ctzll(r[i]);
            int hi = i * 64 + 63 - __builtin_clzll(r[i]);
            if (lo < xmin) xmin = lo;
            if (hi > xmax) xmax = hi;
            cells += __builtin_popcountll(r[i]);
        }
    }
    double fill = 0;
    if (xmax >= 0) fill = (double)cells / ((double)(xmax-xmin+1) * (ymax-ymin+1));
    *fill_out = fill;
    *size_out = sizes[T];
    *bbw = xmax >= 0 ? xmax - xmin + 1 : 0;
    *bbh = ymax >= 0 ? ymax - ymin + 1 : 0;
    /* log-log fit over the last two thirds */
    int t0 = T / 3; if (t0 < 6) t0 = 6;
    if (T - t0 < 8) return -1.0;
    double sx=0, sy=0, sxx=0, sxy=0; int m=0;
    for (int t = t0; t <= T; t++) {
        if (sizes[t] <= 0) continue;
        double lx = log((double)t), ly = log((double)sizes[t]);
        sx += lx; sy += ly; sxx += lx*lx; sxy += lx*ly; m++;
    }
    if (m < 8) return -1.0;
    double den = m*sxx - sx*sx;
    if (den <= 0) return -1.0;
    return (m*sxy - sx*sy) / den;
}

/* ------------------------------------------------------------- census -- */

#define MAXSEEDS 300
static int SEEDS[MAXSEEDS][24];   /* up to 8 laws: x,y,k triples */
static int SEEDN[MAXSEEDS], NSEED;

static void mkseeds(int which) {
    NSEED = 0;
    if (which == 2) {          /* 3-kind seed family (8 canonical seeds) */
        int s0[] = {0,0,0};
        int s1[] = {0,0,0, 0,0,1};
        int s2[] = {0,0,0, 0,0,1, 0,0,2};
        int s3[] = {0,0,0, 1,0,1};
        int s4[] = {0,0,0, 1,0,1, 0,1,2};
        int s5[] = {0,0,0, 1,1,1};
        int s6[] = {0,0,0, 1,0,1, 1,1,2};
        int s7[] = {0,0,0, 1,0,0, 0,1,1, 1,1,2};
        int *ss[] = {s0,s1,s2,s3,s4,s5,s6,s7};
        int nn[] = {1,2,3,2,3,2,3,4};
        for (int i = 0; i < 8; i++) {
            memcpy(SEEDS[i], ss[i], sizeof(int) * 3 * nn[i]);
            SEEDN[i] = nn[i];
        }
        NSEED = 8;
        return;
    }
    if (which == 1) {
        /* COMPLETE: every nonempty 2-kind code inside a 2x2 box, i.e. each of
         * the 4 cells carries a subset of {A,B}: 4^4 - 1 = 255 codes.        */
        for (int m = 1; m < 256; m++) {
            int nl = 0;
            for (int cell = 0; cell < 4; cell++) {
                int bits = (m >> (2 * cell)) & 3;
                int x = cell & 1, y = cell >> 1;
                if (bits & 1) { SEEDS[NSEED][3*nl]=x; SEEDS[NSEED][3*nl+1]=y;
                                SEEDS[NSEED][3*nl+2]=0; nl++; }
                if (bits & 2) { SEEDS[NSEED][3*nl]=x; SEEDS[NSEED][3*nl+1]=y;
                                SEEDS[NSEED][3*nl+2]=1; nl++; }
            }
            SEEDN[NSEED] = nl; NSEED++;
        }
        return;
    }
    if (which == 0) {                 /* 6 canonical small seeds */
        int s0[] = {0,0,0};                        /* A            */
        int s1[] = {0,0,0, 0,0,1};                 /* A+B stacked  */
        int s2[] = {0,0,0, 1,0,1};                 /* A . B  (E)   */
        int s3[] = {0,0,0, 0,1,1};                 /* A / B  (N)   */
        int s4[] = {0,0,0, 1,1,1};                 /* A / B  (NE)  */
        int s5[] = {0,0,0, 1,0,0, 0,1,1};          /* AA / B       */
        int *ss[] = {s0,s1,s2,s3,s4,s5};
        int nn[] = {1,2,2,2,2,3};
        for (int i = 0; i < 6; i++) {
            memcpy(SEEDS[i], ss[i], sizeof(int) * 3 * nn[i]);
            SEEDN[i] = nn[i];
        }
        NSEED = 6;
    }
}

#define NCAT 5     /* 0 glider  1 nonpow2  2 balanced  3 longcycle  4 unres */
#define FCAP 400
typedef struct {
    long long tally[V_NVERD];
    long long perhist[512];
    long long ncat[NCAT];
    char finds[NCAT][FCAP][192];
    int nfinds[NCAT];
    long long gl_outdeg[2], bal_outdeg[2], np2_outdeg[2];
    long long gl_card[16], gl_per[16], gl_disp[9][9];
    long long ahist[64]; long long nalpha;
    long long cls[3][V_NVERD]; long long clsnp2[3];
    double amax; char abest[192];
    double amax_cls[3]; long long ahist_cls[3][64]; long long nalpha_cls[3];
    char abest_cls[3][192];
    long long done;
} Acc;

static void addfind(Acc *A, int cat, const char *fmt, ...) {
    A->ncat[cat]++;
    if (A->nfinds[cat] >= FCAP) return;
    va_list ap; va_start(ap, fmt);
    vsnprintf(A->finds[cat][A->nfinds[cat]++], 192, fmt, ap);
    va_end(ap);
}

typedef struct {
    long long lo, hi;
    int mode, sem, steps, maxcard, tid, doalpha;
    const char *dump;
    FILE *fp;
    Acc acc;
} Job;

static void unpack2(long long idx, Univ *U) {
    /* 2-kind Moore: (rA*729 + rB)*9 + tmap */
    int tmap = (int)(idx % 9); idx /= 9;
    int rB = (int)(idx % 729); idx /= 729;
    int rA = (int)idx;
    U->n = 2;
    U->a[0] = rA / 81; U->b[0] = (rA / 9) % 9; U->c[0] = rA % 9;
    U->a[1] = rB / 81; U->b[1] = (rB / 9) % 9; U->c[1] = rB % 9;
    int tA = tmap / 3, tB = tmap % 3;
    int mA[3] = {1, 2, 3}, mB[3] = {1, 2, 3};
    U->tgt[0] = mA[tA]; U->tgt[1] = mB[tB];
}

static void unpack3(long long idx, Univ *U) {
    /* reproducible 3-kind random universe: splitmix64 stream keyed by idx */
    uint64_t z = (uint64_t)idx * 0x9E3779B97F4A7C15ULL + 0x243f6a8885a308d3ULL;
    U->n = 3;
    for (int k = 0; k < 3; k++) {
        z = mix64(z); U->a[k] = (int)(z % 9);
        z = mix64(z); U->b[k] = (int)(z % 9);
        z = mix64(z); U->c[k] = (int)(z % 9);
        z = mix64(z); U->tgt[k] = 1 + (int)(z % 7);
    }
}

static void unpack2vn(long long idx, Univ *U) {
    /* 2-kind von Neumann: (rA*125 + rB)*9 + tmap, offsets from OEWNS */
    int tmap = (int)(idx % 9); idx /= 9;
    int rB = (int)(idx % 125); idx /= 125;
    int rA = (int)idx;
    U->n = 2;
    U->a[0] = rA / 25; U->b[0] = (rA / 5) % 5; U->c[0] = rA % 5;
    U->a[1] = rB / 25; U->b[1] = (rB / 5) % 5; U->c[1] = rB % 5;
    int tA = tmap / 3, tB = tmap % 3;
    int mA[3] = {1, 2, 3}, mB[3] = {1, 2, 3};
    U->tgt[0] = mA[tA]; U->tgt[1] = mB[tB];
}

static int uclass(const Univ *U) {
    int maxout = 0, indeg[NK] = {0, 0, 0};
    for (int k = 0; k < U->n; k++) {
        int o = __builtin_popcount(U->tgt[k]);
        if (o > maxout) maxout = o;
        for (int t = 0; t < U->n; t++) if (U->tgt[k] & (1 << t)) indeg[t]++;
    }
    if (maxout >= 2) return 2;
    for (int t = 0; t < U->n; t++) if (indeg[t] >= 2) return 1;
    return 0;
}

static void ulabel(const Univ *U, char *out) {
    char *p = out;
    for (int k = 0; k < U->n; k++) {
        *p++ = ONM[U->a[k]]; *p++ = ONM[U->b[k]]; *p++ = ONM[U->c[k]];
        *p++ = '>';
        for (int t = 0; t < U->n; t++) if (U->tgt[k] & (1 << t)) *p++ = 'A' + t;
        *p++ = (k == U->n - 1) ? 0 : ' ';
    }
}

static void *worker(void *arg) {
    Job *J = (Job *)arg;
    memset(&J->acc, 0, sizeof(Acc));
    if (J->dump) {
        char fn[256]; snprintf(fn, 256, "%s.%d", J->dump, J->tid);
        J->fp = fopen(fn, "w");
    }
    Univ U;
    Res R;
    long long idxcount = 0;
    for (long long idx = J->lo; idx < J->hi; idx++) {
        if (J->mode == 0) unpack2(idx, &U);
        else if (J->mode == 2) unpack3(idx, &U);
        else unpack2vn(idx, &U);
        int didalpha = 0;
        int cls = uclass(&U);
        for (int s = 0; s < NSEED; s++) {
            run(&U, SEEDS[s], SEEDN[s], J->sem, J->steps, J->maxcard, &R);
            J->acc.tally[R.verdict]++;
            J->acc.cls[cls][R.verdict]++;
            char lab[64];
            int md = (cls == 2) ? 1 : 0;   /* multi-target (out-degree >= 2)? */
            if (R.verdict == V_CYCLE) {
                int p = R.period;
                J->acc.perhist[p < 511 ? p : 511]++;
                if (p & (p - 1)) {
                    ulabel(&U, lab);
                    J->acc.clsnp2[cls]++;
                    J->acc.np2_outdeg[md]++;
                    addfind(&J->acc, 1, "p=%d seed=%d card=%d U=%s",
                            p, s, R.card, lab);
                    if (J->fp) fprintf(J->fp, "NONPOW2 %d %d %d %d %s\n",
                                       p, s, R.card, md, lab);
                }
                if (p > 16) {
                    ulabel(&U, lab);
                    addfind(&J->acc, 3, "p=%d seed=%d card=%d U=%s",
                            p, s, R.card, lab);
                }
            } else if (R.verdict == V_GLIDER) {
                ulabel(&U, lab);
                J->acc.gl_outdeg[md]++;
                J->acc.gl_card[R.card < 15 ? R.card : 15]++;
                J->acc.gl_per[R.period < 15 ? R.period : 15]++;
                if (R.dx > -5 && R.dx < 5 && R.dy > -5 && R.dy < 5)
                    J->acc.gl_disp[R.dx + 4][R.dy + 4]++;
                addfind(&J->acc, 0, "p=%d d=(%d,%d) seed=%d card=%d t0=%d U=%s",
                        R.period, R.dx, R.dy, s, R.card, R.t0, lab);
                if (J->fp) fprintf(J->fp, "GLIDER %d %d %d %d %d %d %d %s\n",
                                   R.period, R.dx, R.dy, s, R.card, R.t0, md, lab);
            } else if (R.verdict == V_BALANCED) {
                ulabel(&U, lab);
                J->acc.bal_outdeg[md]++;
                addfind(&J->acc, 2, "act=%d seed=%d card=%d U=%s",
                        R.nactive, s, R.card, lab);
                if (J->fp) fprintf(J->fp, "BALANCED %d %d %d %d %s\n",
                                   R.nactive, s, R.card, md, lab);
            } else if (R.verdict == V_UNRES) {
                ulabel(&U, lab);
                addfind(&J->acc, 4, "card=%d maxcard=%d seed=%d U=%s",
                        R.card, R.maxcard, s, lab);
                if (J->fp) fprintf(J->fp, "UNRES %d %d %d %d %s\n",
                                   R.card, R.maxcard, s, md, lab);
            } else if (R.verdict == V_ESCAPE) {
                if (J->fp && (idxcount++ % 64) == 0) {
                    ulabel(&U, lab);
                    fprintf(J->fp, "ESCAPE %d %d %d %d %s\n",
                            R.card, R.maxcard, s, md, lab);
                }
                if (J->doalpha && !didalpha) {
                    didalpha = 1;
                    double fill; int fsz, bw, bh;
                    double al = alpha_run(&U, SEEDS[s], SEEDN[s], J->sem,
                                          &fill, &fsz, &bw, &bh);
                    if (al > -0.5) {
                        J->acc.nalpha++;
                        J->acc.nalpha_cls[cls]++;
                        int bin = (int)(al * 20.0 + 0.5);
                        if (bin < 0) bin = 0; if (bin > 63) bin = 63;
                        J->acc.ahist[bin]++;
                        J->acc.ahist_cls[cls][bin]++;
                        if (al > J->acc.amax_cls[cls]) {
                            J->acc.amax_cls[cls] = al;
                            ulabel(&U, lab);
                            snprintf(J->acc.abest_cls[cls], 192,
                                "alpha=%.3f fill=%.3f sz=%d bbox=%dx%d seed=%d U=%s",
                                al, fill, fsz, bw, bh, s, lab);
                        }
                        if (al > J->acc.amax) {
                            J->acc.amax = al;
                            ulabel(&U, lab);
                            snprintf(J->acc.abest, 192,
                                     "alpha=%.3f fill=%.3f sz=%d bbox=%dx%d seed=%d U=%s",
                                     al, fill, fsz, bw, bh, s, lab);
                        }
                        if (al >= 1.02 && J->fp) {
                            ulabel(&U, lab);
                            fprintf(J->fp, "ALPHA %.4f %.4f %d %d %d %d %d %s\n",
                                    al, fill, fsz, bw, bh, s, cls, lab);
                        }
                    }
                }
            }
            J->acc.done++;
        }
    }
    if (J->fp) fclose(J->fp);
    return NULL;
}

/* stdin protocol (mode 9), one experiment per line:
 *   n  a0 b0 c0 tgt0  a1 b1 c1 tgt1 ...  nseed  x y k  x y k ...
 * prints: verdict t0 period dx dy card nactive maxcard tend           */
static int DOALPHA = 0;
static void stdin_mode(int sem, int steps, int maxcard) {
    char line[512];
    while (fgets(line, sizeof(line), stdin)) {
        char *p = line;
        Univ U; Res R;
        U.n = (int)strtol(p, &p, 10);
        if (U.n <= 0 || U.n > NK) break;
        for (int k = 0; k < U.n; k++) {
            U.a[k] = (int)strtol(p, &p, 10);
            U.b[k] = (int)strtol(p, &p, 10);
            U.c[k] = (int)strtol(p, &p, 10);
            U.tgt[k] = (int)strtol(p, &p, 10);
        }
        int ns = (int)strtol(p, &p, 10);
        int sd[3 * 8];
        for (int i = 0; i < ns && i < 8; i++) {
            sd[3 * i] = (int)strtol(p, &p, 10);
            sd[3 * i + 1] = (int)strtol(p, &p, 10);
            sd[3 * i + 2] = (int)strtol(p, &p, 10);
        }
        run(&U, sd, ns, sem, steps, maxcard, &R);
        printf("%s %d %d %d %d %d %d %d %d\n", VNM[R.verdict], R.t0, R.period,
               R.dx, R.dy, R.card, R.nactive, R.maxcard, R.tend);
        if (DOALPHA) {
            double fill; int fsz, bw, bh;
            double al = alpha_run(&U, sd, ns, sem, &fill, &fsz, &bw, &bh);
            printf("ALPHA %.5f %.5f %d %dx%d T=%d sizes:", al, fill, fsz, bw, bh, ANT);
            for (int t = 0; t <= ANT; t++) printf(" %d", ASIZES[t]);
            printf("\n");
        }
        fflush(stdout);
    }
}


/* ------------------------------------------------------- batch escalation --
 * mode 10: read experiments from stdin (same format as mode 9), run them in
 * parallel with a large step budget, print one result line per input line in
 * input order.  Used to escalate the census's UNRESOLVED pool.           */
typedef struct { Univ U; int sd[24]; int ns; } Exp;
typedef struct { Exp *ex; Res *rs; long long lo, hi; int sem, steps, maxcard; } EJob;

static void *eworker(void *arg) {
    EJob *J = (EJob *)arg;
    for (long long i = J->lo; i < J->hi; i++)
        run(&J->ex[i].U, J->ex[i].sd, J->ex[i].ns, J->sem, J->steps,
            J->maxcard, &J->rs[i]);
    return NULL;
}

static void batch_mode(int sem, int steps, int maxcard, int nth) {
    long long cap = 1 << 20, n = 0;
    Exp *ex = malloc(sizeof(Exp) * cap);
    char line[512];
    while (fgets(line, sizeof(line), stdin)) {
        char *p = line;
        Univ U;
        U.n = (int)strtol(p, &p, 10);
        if (U.n <= 0 || U.n > NK) continue;
        for (int k = 0; k < U.n; k++) {
            U.a[k] = (int)strtol(p, &p, 10);
            U.b[k] = (int)strtol(p, &p, 10);
            U.c[k] = (int)strtol(p, &p, 10);
            U.tgt[k] = (int)strtol(p, &p, 10);
        }
        int ns = (int)strtol(p, &p, 10);
        if (ns > 8) ns = 8;
        ex[n].U = U; ex[n].ns = ns;
        for (int i = 0; i < ns; i++) {
            ex[n].sd[3*i] = (int)strtol(p, &p, 10);
            ex[n].sd[3*i+1] = (int)strtol(p, &p, 10);
            ex[n].sd[3*i+2] = (int)strtol(p, &p, 10);
        }
        if (++n == cap) { cap *= 2; ex = realloc(ex, sizeof(Exp) * cap); }
    }
    Res *rs = calloc(n, sizeof(Res));
    pthread_t th[64]; EJob *jb = calloc(nth, sizeof(EJob));
    for (int i = 0; i < nth; i++) {
        jb[i].ex = ex; jb[i].rs = rs;
        jb[i].lo = n * i / nth; jb[i].hi = n * (i + 1) / nth;
        jb[i].sem = sem; jb[i].steps = steps; jb[i].maxcard = maxcard;
        pthread_create(&th[i], NULL, eworker, &jb[i]);
    }
    for (int i = 0; i < nth; i++) pthread_join(th[i], NULL);
    for (long long i = 0; i < n; i++)
        printf("%s %d %d %d %d %d %d %d %d\n", VNM[rs[i].verdict], rs[i].t0,
               rs[i].period, rs[i].dx, rs[i].dy, rs[i].card, rs[i].nactive,
               rs[i].maxcard, rs[i].tend);
}

int main(int argc, char **argv) {
    int mode = 0, sem = 0, steps = 300, maxcard = 900, nth = 12, seedset = 0;
    const char *dump = NULL;
    int doalpha = 0;
    long long nuniv = 2000000;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--mode")) mode = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--sem")) sem = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--steps")) steps = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--maxcard")) maxcard = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--threads")) nth = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--trace")) TRACE = 1;
        else if (!strcmp(argv[i], "--seeds")) seedset = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--dump")) dump = argv[++i];
        else if (!strcmp(argv[i], "--alpha")) doalpha = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--n")) nuniv = atoll(argv[++i]);
    }
    if (mode == 9) { DOALPHA = doalpha; stdin_mode(sem, steps, maxcard); return 0; }
    if (mode == 10) { batch_mode(sem, steps, maxcard, nth); return 0; }
    mkseeds(seedset);
    long long total = (mode == 0) ? 729LL * 729 * 9 :
                      (mode == 2) ? nuniv : 125LL * 125 * 9;
    fprintf(stderr, "census mode=%d sem=%d universes=%lld seeds=%d steps=%d\n",
            mode, sem, total, NSEED, steps);
    pthread_t th[64];
    Job *jobs = calloc(nth, sizeof(Job));
    for (int i = 0; i < nth; i++) {
        jobs[i].lo = total * i / nth;
        jobs[i].hi = total * (i + 1) / nth;
        jobs[i].mode = mode; jobs[i].sem = sem;
        jobs[i].steps = steps; jobs[i].maxcard = maxcard;
        jobs[i].tid = i; jobs[i].dump = dump; jobs[i].doalpha = doalpha;
        pthread_create(&th[i], NULL, worker, &jobs[i]);
    }
    static Acc A; memset(&A, 0, sizeof(A));
    static const char *CATNM[NCAT] = {"GLIDER", "NONPOW2", "BALANCED",
                                      "LONGCYCLE", "UNRES"};
    for (int i = 0; i < nth; i++) {
        pthread_join(th[i], NULL);
        for (int v = 0; v < V_NVERD; v++) A.tally[v] += jobs[i].acc.tally[v];
        for (int p = 0; p < 512; p++) A.perhist[p] += jobs[i].acc.perhist[p];
        A.done += jobs[i].acc.done;
        for (int z = 0; z < 2; z++) {
            A.gl_outdeg[z] += jobs[i].acc.gl_outdeg[z];
            A.bal_outdeg[z] += jobs[i].acc.bal_outdeg[z];
            A.np2_outdeg[z] += jobs[i].acc.np2_outdeg[z];
        }
        for (int z = 0; z < 16; z++) {
            A.gl_card[z] += jobs[i].acc.gl_card[z];
            A.gl_per[z] += jobs[i].acc.gl_per[z];
        }
        for (int u = 0; u < 9; u++) for (int v = 0; v < 9; v++)
            A.gl_disp[u][v] += jobs[i].acc.gl_disp[u][v];
        for (int z = 0; z < 64; z++) A.ahist[z] += jobs[i].acc.ahist[z];
        for (int z = 0; z < 3; z++) {
            A.clsnp2[z] += jobs[i].acc.clsnp2[z];
            for (int v = 0; v < V_NVERD; v++) A.cls[z][v] += jobs[i].acc.cls[z][v];
        }
        A.nalpha += jobs[i].acc.nalpha;
        if (jobs[i].acc.amax > A.amax) { A.amax = jobs[i].acc.amax;
            strcpy(A.abest, jobs[i].acc.abest); }
        for (int z = 0; z < 3; z++) {
            A.nalpha_cls[z] += jobs[i].acc.nalpha_cls[z];
            for (int b = 0; b < 64; b++)
                A.ahist_cls[z][b] += jobs[i].acc.ahist_cls[z][b];
            if (jobs[i].acc.amax_cls[z] > A.amax_cls[z]) {
                A.amax_cls[z] = jobs[i].acc.amax_cls[z];
                strcpy(A.abest_cls[z], jobs[i].acc.abest_cls[z]);
            }
        }
        for (int c = 0; c < NCAT; c++) {
            A.ncat[c] += jobs[i].acc.ncat[c];
            for (int f = 0; f < jobs[i].acc.nfinds[c] && A.nfinds[c] < FCAP; f++)
                strcpy(A.finds[c][A.nfinds[c]++], jobs[i].acc.finds[c][f]);
        }
    }
    printf("RUNS %lld\n", A.done);
    for (int v = 0; v < V_NVERD; v++)
        printf("TALLY %s %lld\n", VNM[v], A.tally[v]);
    for (int p = 0; p < 512; p++)
        if (A.perhist[p]) printf("PERIOD %d %lld\n", p, A.perhist[p]);
    for (int c = 0; c < NCAT; c++) printf("COUNT %s %lld\n", CATNM[c], A.ncat[c]);
    for (int z = 0; z < 3; z++) {
        printf("CLASS %d nonpow2=%lld", z, A.clsnp2[z]);
        for (int v = 0; v < V_NVERD; v++) printf(" %s=%lld", VNM[v], A.cls[z][v]);
        printf("\n");
    }
    printf("GLIDER_OUTDEG single=%lld multi=%lld\n", A.gl_outdeg[0], A.gl_outdeg[1]);
    printf("BALANCED_OUTDEG single=%lld multi=%lld\n", A.bal_outdeg[0], A.bal_outdeg[1]);
    printf("NONPOW2_OUTDEG single=%lld multi=%lld\n", A.np2_outdeg[0], A.np2_outdeg[1]);
    for (int z = 0; z < 16; z++) if (A.gl_card[z]) printf("GLCARD %d %lld\n", z, A.gl_card[z]);
    for (int z = 0; z < 16; z++) if (A.gl_per[z]) printf("GLPER %d %lld\n", z, A.gl_per[z]);
    for (int u = 0; u < 9; u++) for (int v = 0; v < 9; v++)
        if (A.gl_disp[u][v]) printf("GLDISP %d %d %lld\n", u-4, v-4, A.gl_disp[u][v]);
    if (A.nalpha) {
        printf("ALPHA_RUNS %lld\n", A.nalpha);
        for (int z = 0; z < 64; z++)
            if (A.ahist[z]) printf("AHIST %.2f %lld\n", z / 20.0, A.ahist[z]);
        printf("ALPHA_MAX %s\n", A.abest);
        for (int z = 0; z < 3; z++) {
            printf("ALPHA_CLASS %d runs=%lld max=%.3f %s\n", z,
                   A.nalpha_cls[z], A.amax_cls[z], A.abest_cls[z]);
            for (int b = 0; b < 64; b++)
                if (A.ahist_cls[z][b])
                    printf("AHIST_CLASS %d %.2f %lld\n", z, b / 20.0,
                           A.ahist_cls[z][b]);
        }
    }
    for (int c = 0; c < NCAT; c++)
        for (int f = 0; f < A.nfinds[c]; f++)
            printf("FIND %s %s\n", CATNM[c], A.finds[c][f]);
    return 0;
}
