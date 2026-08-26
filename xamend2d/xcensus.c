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

#define NK 3
#define ROWS 64
#define PAD 1
#define NROW (ROWS + 2 * PAD)
#define MAXSPAN 59
#define TBITS 11
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
    memset(tog, 0, sizeof(uint64_t) * NK * NROW);
    for (int k = 0; k < n; k++) {
        int ax = OX[U->a[k]], ay = OY[U->a[k]];
        int bx = OX[U->b[k]], by = OY[U->b[k]];
        int cx = OX[U->c[k]], cy = OY[U->c[k]];
        int any = 0;
        for (int y = PAD; y < NROW - PAD; y++) {
            uint64_t la = shx(occ[y + ay], ax);
            uint64_t lb = shx(occ[y + by], bx);
            uint64_t w = B->p[k][y] & la & ~lb;
            act[y] = w;
            if (w) { any = 1; nact += __builtin_popcountll(w); }
        }
        if (!any) continue;
        for (int y = PAD; y < NROW - PAD; y++) {
            if (!act[y]) continue;
            uint64_t e = emx(act[y], cx);
            int yy = y + cy;
            for (int t = 0; t < n; t++)
                if (U->tgt[k] & (1 << t)) {
                    if (sem) tog[t][yy] |= e; else tog[t][yy] ^= e;
                }
        }
    }
    int changed = 0;
    for (int k = 0; k < n; k++) {
        for (int y = PAD; y < NROW - PAD; y++) {
            if (tog[k][y]) { B->p[k][y] ^= tog[k][y]; changed = 1; }
        }
        B->p[k][0] = 0; B->p[k][NROW - 1] = 0;
    }
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
    int dy = 1 - ymin, dx = 1 - xmin;
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

static uint64_t hashB(const Board *B, int n) {
    uint64_t h = 1469598103934665603ULL;
    for (int k = 0; k < n; k++)
        for (int y = PAD; y < NROW - PAD; y++) {
            h ^= B->p[k][y];
            h *= 1099511628211ULL;
        }
    return h;
}

typedef struct { uint64_t h; int t, ax, ay; } Ent;

static void run(const Univ *U, const int *seed, int nseed, int sem,
                int maxsteps, int maxcard, Res *R) {
    Board B;
    memset(&B, 0, sizeof(B));
    for (int i = 0; i < nseed; i++) {
        int x = seed[3 * i], y = seed[3 * i + 1], k = seed[3 * i + 2];
        if (k >= U->n) continue;
        B.p[k][y + 8 + PAD] |= 1ULL << (x + 8);
    }
    Ent tab[TSIZE];
    memset(tab, 0, sizeof(tab));
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
        uint64_t h = hashB(&B, U->n);
        int idx = (int)(h & (TSIZE - 1));
        while (tab[idx].h && tab[idx].h != h) idx = (idx + 1) & (TSIZE - 1);
        if (tab[idx].h == h) {
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
        if (t == maxsteps) { R->card = c; R->maxcard = maxc; R->tend = t; return; }
        stepB(&B, U, sem, NULL);
    }
}

/* ------------------------------------------------------------- census -- */

static int SEEDS[16][12];   /* up to 4 laws: x,y,k triples */
static int SEEDN[16], NSEED;

static void mkseeds(int which) {
    NSEED = 0;
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

typedef struct {
    long long tally[V_NVERD];
    long long perhist[64];
    long long nglider, nbal, noddper;
    char finds[64][256];
    int nfinds;
    long long done;
} Acc;

typedef struct {
    long long lo, hi;
    int mode, sem, steps, maxcard;
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
    Univ U;
    Res R;
    for (long long idx = J->lo; idx < J->hi; idx++) {
        if (J->mode == 0) unpack2(idx, &U); else unpack2vn(idx, &U);
        for (int s = 0; s < NSEED; s++) {
            run(&U, SEEDS[s], SEEDN[s], J->sem, J->steps, J->maxcard, &R);
            J->acc.tally[R.verdict]++;
            if (R.verdict == V_CYCLE) {
                int p = R.period;
                J->acc.perhist[p < 63 ? p : 63]++;
                if (p & (p - 1)) {
                    J->acc.noddper++;
                    if (J->acc.nfinds < 64) {
                        char lab[64]; ulabel(&U, lab);
                        snprintf(J->acc.finds[J->acc.nfinds++], 256,
                                 "NONPOW2 p=%d seed=%d card=%d U=%s", p, s,
                                 R.card, lab);
                    }
                }
            } else if (R.verdict == V_GLIDER) {
                J->acc.nglider++;
                if (J->acc.nfinds < 64) {
                    char lab[64]; ulabel(&U, lab);
                    snprintf(J->acc.finds[J->acc.nfinds++], 256,
                             "GLIDER p=%d d=(%d,%d) seed=%d card=%d U=%s",
                             R.period, R.dx, R.dy, s, R.card, lab);
                }
            } else if (R.verdict == V_BALANCED) {
                J->acc.nbal++;
                if (J->acc.nbal < 30 && J->acc.nfinds < 64) {
                    char lab[64]; ulabel(&U, lab);
                    snprintf(J->acc.finds[J->acc.nfinds++], 256,
                             "BALANCED act=%d seed=%d card=%d U=%s",
                             R.nactive, s, R.card, lab);
                }
            }
            J->acc.done++;
        }
    }
    return NULL;
}

/* stdin protocol (mode 9), one experiment per line:
 *   n  a0 b0 c0 tgt0  a1 b1 c1 tgt1 ...  nseed  x y k  x y k ...
 * prints: verdict t0 period dx dy card nactive maxcard tend           */
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
        fflush(stdout);
    }
}

int main(int argc, char **argv) {
    int mode = 0, sem = 0, steps = 300, maxcard = 900, nth = 12;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "--mode")) mode = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--sem")) sem = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--steps")) steps = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--maxcard")) maxcard = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--threads")) nth = atoi(argv[++i]);
    }
    if (mode == 9) { stdin_mode(sem, steps, maxcard); return 0; }
    mkseeds(0);
    long long total = (mode == 0) ? 729LL * 729 * 9 : 125LL * 125 * 9;
    fprintf(stderr, "census mode=%d sem=%d universes=%lld seeds=%d steps=%d\n",
            mode, sem, total, NSEED, steps);
    pthread_t th[64];
    Job *jobs = calloc(nth, sizeof(Job));
    for (int i = 0; i < nth; i++) {
        jobs[i].lo = total * i / nth;
        jobs[i].hi = total * (i + 1) / nth;
        jobs[i].mode = mode; jobs[i].sem = sem;
        jobs[i].steps = steps; jobs[i].maxcard = maxcard;
        pthread_create(&th[i], NULL, worker, &jobs[i]);
    }
    Acc A; memset(&A, 0, sizeof(A));
    for (int i = 0; i < nth; i++) {
        pthread_join(th[i], NULL);
        for (int v = 0; v < V_NVERD; v++) A.tally[v] += jobs[i].acc.tally[v];
        for (int p = 0; p < 64; p++) A.perhist[p] += jobs[i].acc.perhist[p];
        A.nglider += jobs[i].acc.nglider;
        A.nbal += jobs[i].acc.nbal;
        A.noddper += jobs[i].acc.noddper;
        A.done += jobs[i].acc.done;
        for (int f = 0; f < jobs[i].acc.nfinds && A.nfinds < 64; f++)
            strcpy(A.finds[A.nfinds++], jobs[i].acc.finds[f]);
    }
    printf("RUNS %lld\n", A.done);
    for (int v = 0; v < V_NVERD; v++)
        printf("TALLY %s %lld\n", VNM[v], A.tally[v]);
    for (int p = 0; p < 64; p++)
        if (A.perhist[p]) printf("PERIOD %d %lld\n", p, A.perhist[p]);
    printf("NGLIDER %lld\nNBALANCED %lld\nNONPOW2 %lld\n",
           A.nglider, A.nbal, A.noddper);
    for (int f = 0; f < A.nfinds; f++) printf("FIND %s\n", A.finds[f]);
    return 0;
}
