/* sweep.c — complete state-space census of cross-amendment nomic rings.
 *
 * Reads jobs on stdin, one per line:
 *     n m mode a0 b0 c0 t0 a1 b1 c1 t1 ...
 * mode: 0=parity 1=or 2=super 3=super_or
 *
 * For each job it enumerates the ENTIRE state space (2^(n*m) states),
 * builds the functional graph, and reports exactly:
 *   - the multiset of cycle lengths (period -> #cycles, #states on them)
 *   - for each period a minimum-cardinality representative
 *   - all rotor classes (p, r, j) with a minimum-cardinality representative,
 *     where Phi^p(X) = rot_r(tau^j(X)); j>0 only for homogeneous cyclic
 *     constitutions (where the cyclic kind relabelling tau is an automorphism)
 *   - #fixed points, #balanced fixed points (fixed with >=1 active law)
 *   - #Gardens of Eden (in-degree 0)   [only when goe=1 argv flag]
 *
 * Output: one JSON line per job.  Everything is exact; no sampling.
 *
 * cc -O3 -march=native -o sweep sweep.c
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXK 4

static int NK, M, MODE;
static uint32_t MASK;
static int RA[MAXK], RB[MAXK], RC[MAXK], TG[MAXK];  /* rotation amounts */

static inline uint32_t rot(uint32_t x, int r) {
    return r ? (((x << r) | (x >> (M - r))) & MASK) : x;
}

/* decode/encode: kind k occupies bits [k*M, (k+1)*M) */
static inline void dec(uint64_t v, uint32_t *X) {
    for (int k = 0; k < NK; k++) X[k] = (uint32_t)((v >> (k * M)) & MASK);
}
static inline uint64_t enc(const uint32_t *X) {
    uint64_t v = 0;
    for (int k = 0; k < NK; k++) v |= (uint64_t)X[k] << (k * M);
    return v;
}

static inline void stepX(const uint32_t *X, uint32_t *Y) {
    uint32_t O = 0, emit[MAXK], acc[MAXK];
    for (int k = 0; k < NK; k++) O |= X[k];
    for (int k = 0; k < NK; k++) {
        uint32_t g = X[k] & rot(O, RA[k]) & (~rot(O, RB[k])) & MASK;
        emit[k] = rot(g, RC[k]);
    }
    if (MODE >= 2) {                                   /* supersession */
        uint32_t cl = 0;
        if (MODE == 2) { for (int k = 0; k < NK; k++) cl ^= emit[k]; }
        else           { for (int k = 0; k < NK; k++) cl |= emit[k]; }
        cl &= O;
        for (int k = 0; k < NK; k++)
            Y[k] = ((X[k] & ~cl) | (emit[k] & ~O)) & MASK;
        return;
    }
    for (int k = 0; k < NK; k++) acc[k] = 0;
    if (MODE == 0) { for (int k = 0; k < NK; k++) acc[TG[k]] ^= emit[k]; }
    else           { for (int k = 0; k < NK; k++) acc[TG[k]] |= emit[k]; }
    for (int k = 0; k < NK; k++) Y[k] = X[k] ^ acc[k];
}

static inline uint64_t succ(uint64_t v) {
    uint32_t X[MAXK], Y[MAXK];
    dec(v, X); stepX(X, Y); return enc(Y);
}

static inline int nactive(uint64_t v) {
    uint32_t X[MAXK], O = 0; dec(v, X);
    for (int k = 0; k < NK; k++) O |= X[k];
    int t = 0;
    for (int k = 0; k < NK; k++)
        t += __builtin_popcount(X[k] & rot(O, RA[k]) & (~rot(O, RB[k])) & MASK);
    return t;
}
static inline int cardv(uint64_t v) {
    uint32_t X[MAXK]; dec(v, X);
    int t = 0; for (int k = 0; k < NK; k++) t += __builtin_popcount(X[k]);
    return t;
}
/* rot_r(tau^j(X)) : tau^j sends kind k's field to kind k+j */
static uint64_t rotstate(uint64_t v, int r, int j) {
    uint32_t X[MAXK], Y[MAXK]; dec(v, X);
    for (int k = 0; k < NK; k++) Y[(k + j) % NK] = rot(X[k], r);
    return enc(Y);
}

/* ------------------------------------------------------------------ tables */
#define MAXP 4096
static long long percnt[MAXP];        /* #cycles of that period */
static long long perstates[MAXP];
static int    permincard[MAXP];
static uint64_t perminrep[MAXP];

typedef struct { int p, r, j, card; uint64_t rep; } Rotor;
#define MAXROT 4096
static Rotor rot_list[MAXROT];
static int nrot;

static void add_rotor(int p, int r, int j, int card, uint64_t rep) {
    for (int i = 0; i < nrot; i++)
        if (rot_list[i].p == p && rot_list[i].r == r && rot_list[i].j == j) {
            if (card < rot_list[i].card) { rot_list[i].card = card;
                                           rot_list[i].rep = rep; }
            return;
        }
    if (nrot < MAXROT) { rot_list[nrot].p = p; rot_list[nrot].r = r;
                         rot_list[nrot].j = j; rot_list[nrot].card = card;
                         rot_list[nrot].rep = rep; nrot++; }
}

int main(int argc, char **argv) {
    int want_goe = (argc > 1 && !strcmp(argv[1], "goe"));
    char line[512];
    uint8_t *color = NULL; int32_t *idx = NULL; uint8_t *hit = NULL;
    uint64_t alloc_n = 0;
    uint64_t *path = NULL; uint64_t path_alloc = 0;

    while (fgets(line, sizeof line, stdin)) {
        int a[MAXK], b[MAXK], c[MAXK];
        char *tok = strtok(line, " \t\n");
        if (!tok) continue;
        NK = atoi(tok);
        M = atoi(strtok(NULL, " \t\n"));
        MODE = atoi(strtok(NULL, " \t\n"));
        for (int k = 0; k < NK; k++) {
            a[k] = atoi(strtok(NULL, " \t\n"));
            b[k] = atoi(strtok(NULL, " \t\n"));
            c[k] = atoi(strtok(NULL, " \t\n"));
            TG[k] = atoi(strtok(NULL, " \t\n"));
            RA[k] = ((-a[k]) % M + M) % M;
            RB[k] = ((-b[k]) % M + M) % M;
            RC[k] = ((c[k]) % M + M) % M;
        }
        MASK = (M >= 32) ? 0xffffffffu : ((1u << M) - 1);
        uint64_t N = 1ULL << (NK * M);

        /* homogeneous cyclic constitution -> tau is an automorphism */
        int homog = (NK > 1);
        for (int k = 0; k < NK && homog; k++) {
            if (a[k] != a[0] || b[k] != b[0] || c[k] != c[0]) homog = 0;
            if (TG[k] != (k + 1) % NK) homog = 0;
        }

        if (N > alloc_n) {
            free(color); free(idx); free(hit);
            color = malloc(N); idx = malloc(N * sizeof(int32_t));
            hit = want_goe ? malloc(N) : NULL;
            if (!color || !idx || (want_goe && !hit)) { fprintf(stderr,
                "alloc fail N=%llu\n", (unsigned long long)N); return 1; }
            alloc_n = N;
        }
        memset(color, 0, N);
        if (want_goe) memset(hit, 0, N);
        memset(percnt, 0, sizeof percnt);
        memset(perstates, 0, sizeof perstates);
        for (int i = 0; i < MAXP; i++) permincard[i] = 1 << 30;
        nrot = 0;
        long long nfix = 0, nbal = 0, ncycstates = 0, overflow = 0;

        for (uint64_t s0 = 0; s0 < N; s0++) {
            if (color[s0]) continue;
            uint64_t np = 0, v = s0;
            while (!color[v]) {
                if (np >= path_alloc) {
                    path_alloc = path_alloc ? path_alloc * 2 : 1024;
                    path = realloc(path, path_alloc * sizeof(uint64_t));
                }
                color[v] = 1; idx[v] = (int32_t)np; path[np++] = v;
                v = succ(v);
            }
            if (color[v] == 1) {                       /* new cycle found */
                long long p = (long long)np - idx[v];
                uint64_t start = v;
                if (p < MAXP) {
                    percnt[p]++; perstates[p] += p;
                    /* min-card NONEMPTY representative on this cycle */
                    uint64_t u = start; int bc = 1 << 30; uint64_t brep = 0;
                    for (long long t = 0; t < p; t++) {
                        int cd = cardv(u);
                        if (cd && cd < bc) { bc = cd; brep = u; }
                        u = succ(u);
                    }
                    if (bc < permincard[p]) { permincard[p] = bc;
                                              perminrep[p] = brep; }
                    if (p == 1) {
                        nfix++;
                        if (nactive(start)) nbal++;
                    }
                    /* ROTOR TEST.  Phi commutes with rot and (when homog) with
                     * tau, so the property is uniform along the cycle.  A state
                     * fixed by rot_r*tau^j is NOT moved by it: the symmetry
                     * group STAB must be quotiented out, else every rotation-
                     * symmetric cycle registers as a spurious rotor. */
                    if (bc < (1 << 30)) {
                        uint64_t q = brep; int found = 0;
                        for (long long t = 1; t <= p && !found; t++) {
                            q = succ(q);
                            for (int r = 0; r < M && !found; r++)
                              for (int j = 0; j < (homog ? NK : 1); j++) {
                                if (q != rotstate(brep, r, j)) continue;
                                found = 1;            /* orbit closes here */
                                if (rotstate(brep, r, j) != brep)
                                    add_rotor((int)t, r, j, bc, brep);
                                break;
                              }
                        }
                    }
                } else overflow++;
                ncycstates += p;
            }
            for (uint64_t i = 0; i < np; i++) color[path[i]] = 2;
        }
        if (want_goe) {
            for (uint64_t s = 0; s < N; s++) hit[succ(s)] = 1;
        }
        long long goe = 0;
        if (want_goe) for (uint64_t s = 0; s < N; s++) if (!hit[s]) goe++;

        /* ------------------------------------------------------- report */
        printf("{\"n\":%d,\"m\":%d,\"mode\":%d,\"rules\":[", NK, M, MODE);
        for (int k = 0; k < NK; k++)
            printf("%s[%d,%d,%d]", k ? "," : "", a[k], b[k], c[k]);
        printf("],\"targets\":[");
        for (int k = 0; k < NK; k++) printf("%s%d", k ? "," : "", TG[k]);
        printf("],\"N\":%llu,\"nfix\":%lld,\"nbal\":%lld,\"ncyc_states\":%lld",
               (unsigned long long)N, nfix, nbal, ncycstates);
        if (want_goe) printf(",\"goe\":%lld", goe);
        printf(",\"periods\":{");
        int first = 1;
        for (int p = 1; p < MAXP; p++) if (percnt[p]) {
            printf("%s\"%d\":[%lld,%d,%llu]", first ? "" : ",", p, percnt[p],
                   permincard[p], (unsigned long long)perminrep[p]);
            first = 0;
        }
        printf("},\"rotors\":[");
        for (int i = 0; i < nrot; i++)
            printf("%s[%d,%d,%d,%d,%llu]", i ? "," : "", rot_list[i].p,
                   rot_list[i].r, rot_list[i].j, rot_list[i].card,
                   (unsigned long long)rot_list[i].rep);
        printf("],\"overflow\":%lld}\n", overflow);
        fflush(stdout);
    }
    return 0;
}
