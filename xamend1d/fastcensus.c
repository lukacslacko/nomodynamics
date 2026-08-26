/* fastcensus.c — bit-parallel census engine for 1-D cross-amendment nomodynamics.
 *
 * State: one 64-bit word per kind; bit i of w[k] = "a law of kind k stands at
 * cell (anchor + i - PAD)".  All four semantics of xnomos.step are implemented
 * with shifts and masks:
 *
 *   occ            = OR_k w[k]
 *   act[k]         = w[k] & (occ >> a_k) & ~(occ >> b_k)
 *   emit[k]        = act[k] << c_k
 *   parity : out[t] = w[t] ^ XOR_{k : t in targets(k)} emit[k]
 *   or     : out[t] = w[t] ^  OR_{k : t in targets(k)} emit[k]
 *   super  : clr = XOR_k (emit[k] & occ)   [super_or: OR]
 *            out[k] = (w[k] & ~clr) | (emit[k] & ~occ)
 *
 * Classification mirrors xnomos.classify exactly: the FIRST repeat of the
 * translation-normalised state ends the run; equal anchors => FIXED/BALANCED/
 * CYCLE, unequal anchors => GLIDER.  Budget checks come after the recurrence
 * check, exactly as in the Python.
 *
 * Build:  clang -O3 -march=native -shared -fPIC -o fastcensus.so fastcensus.c
 */
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>

#define MAXK 6
#define PAD  6

typedef struct {
    int32_t  a[MAXK], b[MAXK], c[MAXK];
    uint32_t tm[MAXK];          /* bitmask of target kinds (parity/or only) */
    int32_t  n, mode;           /* 0=parity 1=or 2=super 3=super_or */
} Cst;

/* shift RIGHT by s (s<0 => shift left by -s) */
static inline uint64_t sh(uint64_t x, int s) {
    return s >= 0 ? (x >> s) : (x << (-s));
}

/* ------------------------------------------------------------ one step (64b) */
static inline void one_step(const Cst *C, const uint64_t *in, uint64_t *out) {
    const int n = C->n;
    int k;
    uint64_t occ = 0;
    for (k = 0; k < n; k++) occ |= in[k];
    uint64_t emit[MAXK];
    for (k = 0; k < n; k++) {
        uint64_t act = in[k] & sh(occ, C->a[k]) & ~sh(occ, C->b[k]);
        emit[k] = sh(act, -C->c[k]);
    }
    if (C->mode == 0) {
        uint64_t acc[MAXK];
        for (k = 0; k < n; k++) acc[k] = 0;
        for (k = 0; k < n; k++) {
            uint32_t t = C->tm[k];
            while (t) { int j = __builtin_ctz(t); t &= t - 1; acc[j] ^= emit[k]; }
        }
        for (k = 0; k < n; k++) out[k] = in[k] ^ acc[k];
    } else if (C->mode == 1) {
        uint64_t acc[MAXK];
        for (k = 0; k < n; k++) acc[k] = 0;
        for (k = 0; k < n; k++) {
            uint32_t t = C->tm[k];
            while (t) { int j = __builtin_ctz(t); t &= t - 1; acc[j] |= emit[k]; }
        }
        for (k = 0; k < n; k++) out[k] = in[k] ^ acc[k];
    } else if (C->mode < 4) {
        uint64_t clr = 0;
        if (C->mode == 3) { for (k = 0; k < n; k++) clr |= (emit[k] & occ); }
        else              { for (k = 0; k < n; k++) clr ^= (emit[k] & occ); }
        for (k = 0; k < n; k++) out[k] = (in[k] & ~clr) | (emit[k] & ~occ);
    } else {
        /* ---- TEST-ONLY translation semantics.  Not nomodynamics: these exist
         * solely so the GLIDER branch of run_one (normalised-state recurrence
         * with a nonzero anchor displacement) can be validated against a
         * Python reference, since no real glider is available to test with.
         * Never used by any census. */
        if (C->mode == 4)      for (k = 0; k < n; k++) out[k] = in[k] << 1;
        else if (C->mode == 5) for (k = 0; k < n; k++) out[k] = in[k] >> 1;
        else {
            if (n >= 2) {
                uint64_t t0 = in[1] << 1, t1 = in[0];
                for (k = 2; k < n; k++) out[k] = in[k];
                out[0] = t0; out[1] = t1;
            } else out[0] = in[0] << 1;
        }
    }
}

/* Per-step trace of the normalised state and the anchor, for validating the
 * exact machinery the glider detector runs on. */
int32_t c_trace(const int32_t *cd, int32_t n, int32_t mode, const uint64_t *seed,
                int32_t T, uint64_t *wout, int32_t *aout) {
    Cst C; C.n = n; C.mode = mode;
    for (int k = 0; k < n; k++) { C.a[k] = cd[k]; C.b[k] = cd[n+k];
                                  C.c[k] = cd[2*n+k]; C.tm[k] = (uint32_t)cd[3*n+k]; }
    uint64_t s[MAXK], nx[MAXK];
    int k;
    for (k = 0; k < n; k++) s[k] = seed[k];
    uint64_t occ = 0;
    for (k = 0; k < n; k++) occ |= s[k];
    if (!occ) return 0;
    int d0 = __builtin_ctzll(occ) - PAD;
    if (d0) for (k = 0; k < n; k++) s[k] = sh(s[k], d0);
    int anchor = 0;
    for (int t = 0; t < T; t++) {
        occ = 0;
        for (k = 0; k < n; k++) occ |= s[k];
        if (!occ) return t;
        for (k = 0; k < n; k++) wout[t * n + k] = s[k];
        aout[t] = anchor;
        one_step(&C, s, nx);
        uint64_t o2 = 0;
        for (k = 0; k < n; k++) o2 |= nx[k];
        if (o2) {
            int dsh = __builtin_ctzll(o2) - PAD;
            if (dsh) for (k = 0; k < n; k++) nx[k] = sh(nx[k], dsh);
            anchor += dsh;
        }
        for (k = 0; k < n; k++) s[k] = nx[k];
    }
    return T;
}

/* exported single step, for the fidelity battery */
void c_step(const int32_t *cd, int32_t n, int32_t mode,
            const uint64_t *in, uint64_t *out) {
    Cst C; int k;
    C.n = n; C.mode = mode;
    for (k = 0; k < n; k++) { C.a[k] = cd[k]; C.b[k] = cd[n+k];
                              C.c[k] = cd[2*n+k]; C.tm[k] = (uint32_t)cd[3*n+k]; }
    one_step(&C, in, out);
}

static inline int any_active(const Cst *C, const uint64_t *in) {
    const int n = C->n; int k;
    uint64_t occ = 0;
    for (k = 0; k < n; k++) occ |= in[k];
    for (k = 0; k < n; k++)
        if (in[k] & sh(occ, C->a[k]) & ~sh(occ, C->b[k])) return 1;
    return 0;
}

/* --------------------------------------------------------------- hash table */
#define HBITS 13
#define HSIZE (1 << HBITS)
#define HMASK (HSIZE - 1)

typedef struct {
    uint64_t w[MAXK];
    int32_t  t, anchor;
    uint32_t gen;
} Slot;

enum { R_EXTINCT = 0, R_FIXED, R_BALANCED, R_CYCLE, R_GLIDER, R_GROWING,
       R_UNRESOLVED, R_NCLASS };

typedef struct { int32_t kind, p, d, t0, card; } Res;

static int run_one(const Cst *C, const uint64_t *seed, int max_steps,
                   int max_card, int max_span, Slot *tab, uint32_t gen,
                   Res *R) {
    const int n = C->n;
    int k, t;
    uint64_t s[MAXK], nx[MAXK];
    for (k = 0; k < n; k++) s[k] = seed[k];
    /* normalise the seed to lo == PAD */
    {
        uint64_t occ = 0;
        for (k = 0; k < n; k++) occ |= s[k];
        if (!occ) { R->kind = R_EXTINCT; R->t0 = 0; return R_EXTINCT; }
        int d0 = __builtin_ctzll(occ) - PAD;
        if (d0) for (k = 0; k < n; k++) s[k] = sh(s[k], d0);
    }
    int anchor = 0;
    R->p = 0; R->d = 0; R->card = 0;

    for (t = 0; t < max_steps; t++) {
        uint64_t occ = 0;
        for (k = 0; k < n; k++) occ |= s[k];
        if (!occ) { R->kind = R_EXTINCT; R->t0 = t; return R_EXTINCT; }

        /* ---- recurrence (normalised state == the n words, lo already at PAD) */
        uint64_t h = 1469598103934665603ULL;
        for (k = 0; k < n; k++) { h ^= s[k]; h *= 1099511628211ULL; }
        uint32_t idx = (uint32_t)(h >> 32) & HMASK;
        for (;;) {
            Slot *S = &tab[idx];
            if (S->gen != gen) {                       /* empty: insert */
                S->gen = gen; S->t = t; S->anchor = anchor;
                for (k = 0; k < n; k++) S->w[k] = s[k];
                break;
            }
            int same = 1;
            for (k = 0; k < n; k++) if (S->w[k] != s[k]) { same = 0; break; }
            if (same) {
                int p = t - S->t;
                R->p = p; R->t0 = S->t;
                int cd = 0;
                for (k = 0; k < n; k++) cd += __builtin_popcountll(s[k]);
                R->card = cd;
                if (S->anchor != anchor) {
                    R->d = anchor - S->anchor; R->kind = R_GLIDER; return R_GLIDER;
                }
                if (p == 1) {
                    R->kind = any_active(C, s) ? R_BALANCED : R_FIXED;
                    return R->kind;
                }
                R->kind = R_CYCLE; return R_CYCLE;
            }
            idx = (idx + 1) & HMASK;
        }

        /* ---- budget */
        int lo = __builtin_ctzll(occ), hi = 63 - __builtin_clzll(occ);
        int cd = 0;
        for (k = 0; k < n; k++) cd += __builtin_popcountll(s[k]);
        if (cd > max_card || hi - lo > max_span) {
            R->kind = R_GROWING; R->t0 = t; R->card = cd; return R_GROWING;
        }

        one_step(C, s, nx);
        uint64_t occ2 = 0;
        for (k = 0; k < n; k++) occ2 |= nx[k];
        if (occ2) {
            int dsh = __builtin_ctzll(occ2) - PAD;
            if (dsh) for (k = 0; k < n; k++) nx[k] = sh(nx[k], dsh);
            anchor += dsh;
        }
        for (k = 0; k < n; k++) s[k] = nx[k];
    }
    R->kind = R_UNRESOLVED; R->t0 = max_steps;
    { int cd = 0; for (k = 0; k < n; k++) cd += __builtin_popcountll(s[k]); R->card = cd; }
    return R_UNRESOLVED;
}

/* --------------------------------------------------------------- the census */
typedef struct {
    const int32_t *cdata; int64_t nconst; int32_t n, mode;
    const uint64_t *sdata; int64_t nseed;
    int32_t max_steps, max_card, max_span;
    int64_t ci_lo, ci_hi;
    int64_t hist[R_NCLASS];
    int32_t *hits; int32_t maxhits; int32_t *nhits; pthread_mutex_t *mx;
    int32_t report_mask;        /* which outcome classes to record as hits */
} Job;

static void *worker(void *arg) {
    Job *J = (Job *)arg;
    Slot *tab = (Slot *)calloc(HSIZE, sizeof(Slot));
    uint32_t gen = 0;
    Res R;
    const int n = J->n;
    for (int64_t ci = J->ci_lo; ci < J->ci_hi; ci++) {
        Cst C; C.n = n; C.mode = J->mode;
        const int32_t *cd = J->cdata + ci * 4 * n;
        for (int k = 0; k < n; k++) {
            C.a[k] = cd[k]; C.b[k] = cd[n+k]; C.c[k] = cd[2*n+k];
            C.tm[k] = (uint32_t)cd[3*n+k];
        }
        for (int64_t si = 0; si < J->nseed; si++) {
            gen++;
            if (gen == 0) { memset(tab, 0, HSIZE * sizeof(Slot)); gen = 1; }
            int r = run_one(&C, J->sdata + si * n, J->max_steps,
                            J->max_card, J->max_span, tab, gen, &R);
            J->hist[r]++;
            if ((J->report_mask >> r & 1) && J->hits) {
                pthread_mutex_lock(J->mx);
                if (*J->nhits < J->maxhits) {
                    int32_t *h = J->hits + (*J->nhits) * 5;
                    h[0] = (int32_t)ci; h[1] = (int32_t)si;
                    h[2] = R.p; h[3] = R.d; h[4] = (r == R_GLIDER) ? R.t0 : -r;
                    (*J->nhits)++;
                }
                pthread_mutex_unlock(J->mx);
            }
        }
    }
    free(tab);
    return NULL;
}

int32_t c_census(const int32_t *cdata, int64_t nconst, int32_t n, int32_t mode,
                 const uint64_t *sdata, int64_t nseed,
                 int32_t max_steps, int32_t max_card, int32_t max_span,
                 int64_t *hist, int32_t *hits, int32_t maxhits, int32_t nthread,
                 int32_t report_mask) {
    if (nthread < 1) nthread = 1;
    if (nthread > 64) nthread = 64;
    if ((int64_t)nthread > nconst) nthread = (int32_t)nconst;
    pthread_t th[64];
    Job jobs[64];
    pthread_mutex_t mx = PTHREAD_MUTEX_INITIALIZER;
    int32_t nhits = 0;
    for (int i = 0; i < nthread; i++) {
        memset(&jobs[i], 0, sizeof(Job));
        jobs[i].cdata = cdata; jobs[i].nconst = nconst; jobs[i].n = n;
        jobs[i].mode = mode; jobs[i].sdata = sdata; jobs[i].nseed = nseed;
        jobs[i].max_steps = max_steps; jobs[i].max_card = max_card;
        jobs[i].max_span = max_span;
        jobs[i].ci_lo = nconst * i / nthread;
        jobs[i].ci_hi = nconst * (i + 1) / nthread;
        jobs[i].hits = hits; jobs[i].maxhits = maxhits;
        jobs[i].nhits = &nhits; jobs[i].mx = &mx;
        jobs[i].report_mask = report_mask ? report_mask : (1 << R_GLIDER);
    }
    for (int i = 0; i < nthread; i++) pthread_create(&th[i], NULL, worker, &jobs[i]);
    for (int i = 0; i < nthread; i++) pthread_join(th[i], NULL);
    for (int c = 0; c < R_NCLASS; c++) hist[c] = 0;
    for (int i = 0; i < nthread; i++)
        for (int c = 0; c < R_NCLASS; c++) hist[c] += jobs[i].hist[c];
    return nhits;
}

/* single classification, for spot checks against xnomos.classify */
void c_classify(const int32_t *cd, int32_t n, int32_t mode, const uint64_t *seed,
                int32_t max_steps, int32_t max_card, int32_t max_span,
                int32_t *out /* kind,p,d,t0,card */) {
    Cst C; C.n = n; C.mode = mode;
    for (int k = 0; k < n; k++) { C.a[k] = cd[k]; C.b[k] = cd[n+k];
                                  C.c[k] = cd[2*n+k]; C.tm[k] = (uint32_t)cd[3*n+k]; }
    Slot *tab = (Slot *)calloc(HSIZE, sizeof(Slot));
    Res R; memset(&R, 0, sizeof(R));
    run_one(&C, seed, max_steps, max_card, max_span, tab, 1, &R);
    out[0] = R.kind; out[1] = R.p; out[2] = R.d; out[3] = R.t0; out[4] = R.card;
    free(tab);
}

/* ====================================================================== */
/*  WIDE ENGINE — for the near-miss (puffer / rake / gun) hunt.            */
/*  WB words per kind; no renormalisation, absolute bit index = cell.      */
/* ====================================================================== */
#define WB    8                 /* 512 cells */
#define WBITS (WB * 64)

static inline void wsh(const uint64_t *x, int s, uint64_t *o) {
    /* shift RIGHT by s in {-1,0,1} (s<0 => left) */
    int i;
    if (s == 0) { for (i = 0; i < WB; i++) o[i] = x[i]; return; }
    if (s > 0) {
        for (i = 0; i < WB; i++)
            o[i] = (x[i] >> 1) | (i + 1 < WB ? (x[i+1] << 63) : 0ULL);
    } else {
        for (i = WB - 1; i >= 0; i--)
            o[i] = (x[i] << 1) | (i > 0 ? (x[i-1] >> 63) : 0ULL);
    }
}

static void wide_step(const Cst *C, const uint64_t in[][WB], uint64_t out[][WB]) {
    const int n = C->n; int k, i;
    uint64_t occ[WB], tmpA[WB], tmpB[WB], act[WB], emit[MAXK][WB];
    for (i = 0; i < WB; i++) occ[i] = 0;
    for (k = 0; k < n; k++) for (i = 0; i < WB; i++) occ[i] |= in[k][i];
    for (k = 0; k < n; k++) {
        wsh(occ, C->a[k], tmpA);
        wsh(occ, C->b[k], tmpB);
        for (i = 0; i < WB; i++) act[i] = in[k][i] & tmpA[i] & ~tmpB[i];
        wsh(act, -C->c[k], emit[k]);
    }
    if (C->mode < 2) {
        uint64_t acc[MAXK][WB];
        for (k = 0; k < n; k++) for (i = 0; i < WB; i++) acc[k][i] = 0;
        for (k = 0; k < n; k++) {
            uint32_t t = C->tm[k];
            while (t) {
                int j = __builtin_ctz(t); t &= t - 1;
                if (C->mode == 0) for (i = 0; i < WB; i++) acc[j][i] ^= emit[k][i];
                else              for (i = 0; i < WB; i++) acc[j][i] |= emit[k][i];
            }
        }
        for (k = 0; k < n; k++) for (i = 0; i < WB; i++) out[k][i] = in[k][i] ^ acc[k][i];
    } else {
        uint64_t clr[WB];
        for (i = 0; i < WB; i++) clr[i] = 0;
        for (k = 0; k < n; k++)
            for (i = 0; i < WB; i++) {
                uint64_t v = emit[k][i] & occ[i];
                if (C->mode == 3) clr[i] |= v; else clr[i] ^= v;
            }
        for (k = 0; k < n; k++)
            for (i = 0; i < WB; i++)
                out[k][i] = (in[k][i] & ~clr[i]) | (emit[k][i] & ~occ[i]);
    }
}

static inline uint64_t wget(const uint64_t *x, int start, int width) {
    /* bits [start, start+width) as a word (width <= 63) */
    if (start < 0) return 0;
    int w = start >> 6, b = start & 63;
    if (w >= WB) return 0;
    uint64_t v = x[w] >> b;
    if (b && w + 1 < WB) v |= x[w+1] << (64 - b);
    return v & ((1ULL << width) - 1);
}

#define TMAX 160
#define FW   28                  /* front-window width (cells) */

/* verdict bits */
#define F_FRONT_R  1
#define F_FRONT_L  2
#define F_DEBRIS_P 4             /* interior agrees at lag p (periodic debris) */
#define F_GROWS    8
#define F_OSC     16             /* debris genuinely oscillates (not static)   */
#define F_GAPPY   32             /* debris has >= 4 occupied/empty transitions  */

typedef struct {
    int32_t flags, p, d, t0, card_lo, card_hi, lo_lo, lo_hi, hi_lo, hi_hi, nblk;
} FRes;

/* Run T steps of the wide engine from `seed` (already placed in the wide frame)
 * and look for a right-front that is p-periodic with displacement d != 0.      */
static void front_scan(const Cst *C, const uint64_t seed[][WB], int T, int Pmax,
                       FRes *F) {
    static __thread uint64_t hist[TMAX][MAXK][WB];
    static __thread int hi_[TMAX], lo_[TMAX], cd_[TMAX];
    const int n = C->n; int t, k, i;
    memset(F, 0, sizeof(FRes));
    if (T > TMAX) T = TMAX;
    for (k = 0; k < n; k++) for (i = 0; i < WB; i++) hist[0][k][i] = seed[k][i];
    for (t = 0; t < T; t++) {
        uint64_t occ[WB]; int cd = 0;
        for (i = 0; i < WB; i++) occ[i] = 0;
        for (k = 0; k < n; k++) for (i = 0; i < WB; i++) {
            occ[i] |= hist[t][k][i]; cd += __builtin_popcountll(hist[t][k][i]);
        }
        cd_[t] = cd;
        int lo = -1, hi = -1;
        for (i = 0; i < WB; i++) if (occ[i]) { lo = i * 64 + __builtin_ctzll(occ[i]); break; }
        for (i = WB - 1; i >= 0; i--) if (occ[i]) { hi = i * 64 + 63 - __builtin_clzll(occ[i]); break; }
        lo_[t] = lo; hi_[t] = hi;
        if (lo < 0) { T = t; break; }               /* extinct */
        if (t + 1 < T) wide_step(C, hist[t], hist[t+1]);
    }
    if (T < 24) return;
    int t0 = T / 2;                                  /* skip the transient */
    F->t0 = t0;
    F->card_lo = cd_[t0]; F->card_hi = cd_[T-1];
    F->lo_lo = lo_[t0];  F->lo_hi = lo_[T-1];
    F->hi_lo = hi_[t0];  F->hi_hi = hi_[T-1];
    if (cd_[T-1] > cd_[t0]) F->flags |= F_GROWS;

    for (int p = 1; p <= Pmax; p++) {
        if (t0 + 2 * p >= T) break;
        int d = hi_[t0+p] - hi_[t0];
        if (d == 0) continue;
        int ok = 1;
        for (t = t0; t + p < T && ok; t++) {
            if (hi_[t+p] - hi_[t] != d) { ok = 0; break; }
            for (k = 0; k < n && ok; k++) {
                uint64_t u = wget(hist[t][k],   hi_[t]   - FW + 1, FW);
                uint64_t v = wget(hist[t+p][k], hi_[t+p] - FW + 1, FW);
                if (u != v) ok = 0;
            }
        }
        if (!ok) continue;
        F->flags |= F_FRONT_R; F->p = p; F->d = d;
        /* debris: does the interior agree at lag p, in place? */
        int dok = 1, osc = 0;
        for (t = t0; t + p < T && dok; t++) {
            int end = hi_[t] - FW;                  /* cells <= end */
            for (k = 0; k < n && dok; k++)
                for (i = 0; i < WB; i++) {
                    int base = i * 64;
                    if (base > end) break;
                    uint64_t m = (end - base >= 63) ? ~0ULL
                                                     : ((1ULL << (end - base + 1)) - 1);
                    if ((hist[t][k][i] & m) != (hist[t+p][k][i] & m)) { dok = 0; break; }
                    if (p > 1 && (hist[t][k][i] & m) != (hist[t+1][k][i] & m)) osc = 1;
                }
        }
        if (dok) F->flags |= F_DEBRIS_P;
        if (osc) F->flags |= F_OSC;
        /* structure of the debris: count occupied/empty transitions in the
         * settled region [lo_[T-1], hi_[T-1]-FW] of the last frame            */
        {
            int end = hi_[T-1] - FW, blk = 0, prev = 0;
            uint64_t occ[WB];
            for (i = 0; i < WB; i++) occ[i] = 0;
            for (k = 0; k < n; k++) for (i = 0; i < WB; i++) occ[i] |= hist[T-1][k][i];
            for (int cpos = lo_[T-1]; cpos <= end && cpos < WBITS; cpos++) {
                int b = (occ[cpos >> 6] >> (cpos & 63)) & 1;
                if (b != prev) blk++;
                prev = b;
            }
            F->nblk = blk;
            if (blk >= 4) F->flags |= F_GAPPY;
        }
        break;
    }
    /* left front */
    for (int p = 1; p <= Pmax; p++) {
        if (t0 + 2 * p >= T) break;
        int d = lo_[t0+p] - lo_[t0];
        if (d == 0) continue;
        int ok = 1;
        for (t = t0; t + p < T && ok; t++) {
            if (lo_[t+p] - lo_[t] != d) { ok = 0; break; }
            for (k = 0; k < n && ok; k++) {
                uint64_t u = wget(hist[t][k],   lo_[t],   FW);
                uint64_t v = wget(hist[t+p][k], lo_[t+p], FW);
                if (u != v) ok = 0;
            }
        }
        if (ok) { F->flags |= F_FRONT_L; if (!F->p) { F->p = p; F->d = d; } break; }
    }
}

/* Batch front scan.  seeds are given as (cell, kindmask) lists compiled by the
 * caller into wide frames: sdata[si*n + k] is a 64-bit word for kind k, whose
 * bit j means cell SEEDBASE + j.  Results: 11 int32 per (ci,si).             */
#define SEEDBASE 200

typedef struct {
    const int32_t *cdata; int64_t nconst; int32_t n, mode;
    const uint64_t *sdata; int64_t nseed;
    int32_t T, Pmax;
    int64_t ci_lo, ci_hi;
    int32_t *out;               /* nconst*nseed*11 */
} FJob;

static void *fworker(void *arg) {
    FJob *J = (FJob *)arg;
    const int n = J->n;
    uint64_t seed[MAXK][WB];
    FRes F;
    for (int64_t ci = J->ci_lo; ci < J->ci_hi; ci++) {
        Cst C; C.n = n; C.mode = J->mode;
        const int32_t *cd = J->cdata + ci * 4 * n;
        for (int k = 0; k < n; k++) {
            C.a[k] = cd[k]; C.b[k] = cd[n+k]; C.c[k] = cd[2*n+k];
            C.tm[k] = (uint32_t)cd[3*n+k];
        }
        for (int64_t si = 0; si < J->nseed; si++) {
            memset(seed, 0, sizeof(seed));
            for (int k = 0; k < n; k++) {
                uint64_t w = J->sdata[si * n + k];
                seed[k][SEEDBASE >> 6] |= w << (SEEDBASE & 63);
                if (SEEDBASE & 63)
                    seed[k][(SEEDBASE >> 6) + 1] |= w >> (64 - (SEEDBASE & 63));
            }
            front_scan(&C, seed, J->T, J->Pmax, &F);
            int32_t *o = J->out + (ci * J->nseed + si) * 11;
            o[0] = F.flags; o[1] = F.p; o[2] = F.d; o[3] = F.t0;
            o[4] = F.card_lo; o[5] = F.card_hi; o[6] = F.lo_lo; o[7] = F.lo_hi;
            o[8] = F.hi_lo; o[9] = F.hi_hi; o[10] = F.nblk;
        }
    }
    return NULL;
}

void c_frontscan(const int32_t *cdata, int64_t nconst, int32_t n, int32_t mode,
                 const uint64_t *sdata, int64_t nseed, int32_t T, int32_t Pmax,
                 int32_t *out, int32_t nthread) {
    if (nthread < 1) nthread = 1;
    if (nthread > 64) nthread = 64;
    if ((int64_t)nthread > nconst) nthread = (int32_t)nconst;
    pthread_t th[64]; FJob jobs[64];
    for (int i = 0; i < nthread; i++) {
        jobs[i].cdata = cdata; jobs[i].nconst = nconst; jobs[i].n = n;
        jobs[i].mode = mode; jobs[i].sdata = sdata; jobs[i].nseed = nseed;
        jobs[i].T = T; jobs[i].Pmax = Pmax; jobs[i].out = out;
        jobs[i].ci_lo = nconst * i / nthread;
        jobs[i].ci_hi = nconst * (i + 1) / nthread;
    }
    for (int i = 0; i < nthread; i++) pthread_create(&th[i], NULL, fworker, &jobs[i]);
    for (int i = 0; i < nthread; i++) pthread_join(th[i], NULL);
}

/* exported wide step, for validating the wide engine too */
void c_wide_step(const int32_t *cd, int32_t n, int32_t mode,
                 const uint64_t *in, uint64_t *out) {
    Cst C; C.n = n; C.mode = mode;
    for (int k = 0; k < n; k++) { C.a[k] = cd[k]; C.b[k] = cd[n+k];
                                  C.c[k] = cd[2*n+k]; C.tm[k] = (uint32_t)cd[3*n+k]; }
    uint64_t I[MAXK][WB], O[MAXK][WB];
    memset(I, 0, sizeof(I)); memset(O, 0, sizeof(O));
    for (int k = 0; k < n; k++) for (int i = 0; i < WB; i++) I[k][i] = in[k*WB+i];
    wide_step(&C, I, O);
    for (int k = 0; k < n; k++) for (int i = 0; i < WB; i++) out[k*WB+i] = O[k][i];
}

int32_t c_wb(void) { return WB; }
int32_t c_pad(void) { return PAD; }
int32_t c_seedbase(void) { return SEEDBASE; }
