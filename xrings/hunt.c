/* hunt.c — broad sampled ROTOR hunt on rings too large to enumerate.
 *
 *   ./hunt n m mode nconst nstate seed [live]
 *
 * Draws `nconst` random constitutions (rules from the 12 live kinds if
 * live=1, else all 27; targets: a random L-cycle permutation, a random
 * non-injective map, or own-kind, cycled), and for each draws `nstate`
 * random codes, iterates each to its cycle (Brent), and tests every cycle for
 * the rotor property Phi^p(X) = rot_r(X), r not in the stabiliser of X.
 * Prints every rotor found (as a JSON line) plus a summary.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXK 5
static int NK, M, MODE;
static uint32_t MASK;
static int RA[MAXK], RB[MAXK], RC[MAXK], TG[MAXK];
static int A[MAXK], B[MAXK], Cc[MAXK];

static inline uint32_t rot(uint32_t x, int r) {
    return r ? (((x << r) | (x >> (M - r))) & MASK) : x;
}
static void stepX(const uint32_t *X, uint32_t *Y) {
    uint32_t O = 0, emit[MAXK], acc[MAXK];
    for (int k = 0; k < NK; k++) O |= X[k];
    for (int k = 0; k < NK; k++)
        emit[k] = rot(X[k] & rot(O, RA[k]) & (~rot(O, RB[k])) & MASK, RC[k]);
    if (MODE >= 2) {
        uint32_t cl = 0;
        if (MODE == 2) for (int k = 0; k < NK; k++) cl ^= emit[k];
        else           for (int k = 0; k < NK; k++) cl |= emit[k];
        cl &= O;
        for (int k = 0; k < NK; k++)
            Y[k] = ((X[k] & ~cl) | (emit[k] & ~O)) & MASK;
        return;
    }
    for (int k = 0; k < NK; k++) acc[k] = 0;
    if (MODE == 0) for (int k = 0; k < NK; k++) acc[TG[k]] ^= emit[k];
    else           for (int k = 0; k < NK; k++) acc[TG[k]] |= emit[k];
    for (int k = 0; k < NK; k++) Y[k] = X[k] ^ acc[k];
}
static int eqX(const uint32_t *a, const uint32_t *b) {
    for (int k = 0; k < NK; k++) if (a[k] != b[k]) return 0;
    return 1;
}
static void cpX(uint32_t *d, const uint32_t *s) {
    for (int k = 0; k < NK; k++) d[k] = s[k];
}

static uint64_t rs;
static inline uint64_t rnd(void) {
    rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs;
}

static const int OFF[3] = {-1, 0, 1};

int main(int argc, char **argv) {
    NK = atoi(argv[1]); M = atoi(argv[2]); MODE = atoi(argv[3]);
    long nconst = atol(argv[4]), nstate = atol(argv[5]);
    rs = strtoull(argv[6], NULL, 10) | 1;
    int live = (argc > 7) ? atoi(argv[7]) : 1;
    MASK = (1u << M) - 1;

    int pool[27][3], np = 0;
    for (int i = 0; i < 3; i++) for (int j = 0; j < 3; j++)
        for (int k = 0; k < 3; k++) {
            int a = OFF[i], b = OFF[j], c = OFF[k];
            if (live && (b == 0 || a == b)) continue;
            pool[np][0] = a; pool[np][1] = b; pool[np][2] = c; np++;
        }

    long nrot = 0, ncyc = 0;
    uint32_t X[MAXK], T[MAXK], H[MAXK], W[MAXK];
    for (long ci = 0; ci < nconst; ci++) {
        for (int k = 0; k < NK; k++) {
            int q = rnd() % np;
            A[k] = pool[q][0]; B[k] = pool[q][1]; Cc[k] = pool[q][2];
            RA[k] = ((-A[k]) % M + M) % M;
            RB[k] = ((-B[k]) % M + M) % M;
            RC[k] = ((Cc[k]) % M + M) % M;
        }
        int tmode = rnd() % 3;
        for (int k = 0; k < NK; k++)
            TG[k] = (tmode == 0) ? (k + 1) % NK
                  : (tmode == 1) ? (int)(rnd() % NK) : k;
        for (long si = 0; si < nstate; si++) {
            for (int k = 0; k < NK; k++) X[k] = (uint32_t)(rnd() & MASK);
            /* Brent: find cycle length p0 and a state on the cycle */
            long power = 1, lam = 1;
            cpX(H, X); cpX(T, X); stepX(T, W); cpX(T, W);
            while (!eqX(H, T)) {
                if (power == lam) { cpX(H, T); power *= 2; lam = 0; }
                stepX(T, W); cpX(T, W); lam++;
                if (lam > 200000) break;
            }
            if (lam > 200000) continue;
            ncyc++;
            /* T is on the cycle; test rotor */
            cpX(W, T);
            for (long t = 1; t <= lam; t++) {
                uint32_t Z[MAXK]; stepX(W, Z); cpX(W, Z);
                int hit = -1;
                for (int r = 0; r < M; r++) {
                    int ok = 1;
                    for (int k = 0; k < NK && ok; k++)
                        if (W[k] != rot(T[k], r)) ok = 0;
                    if (ok) { hit = r; break; }
                }
                if (hit >= 0) {
                    int moves = 0;
                    for (int k = 0; k < NK; k++)
                        if (rot(T[k], hit) != T[k]) moves = 1;
                    if (moves && hit != 0) {
                        nrot++;
                        printf("{\"m\":%d,\"n\":%d,\"mode\":%d,\"p\":%ld,"
                               "\"rot\":%d,\"rules\":[", M, NK, MODE, t, hit);
                        for (int k = 0; k < NK; k++)
                            printf("%s[%d,%d,%d]", k ? "," : "",
                                   A[k], B[k], Cc[k]);
                        printf("],\"targets\":[");
                        for (int k = 0; k < NK; k++)
                            printf("%s%d", k ? "," : "", TG[k]);
                        printf("],\"state\":[");
                        for (int k = 0; k < NK; k++)
                            printf("%s%u", k ? "," : "", T[k]);
                        printf("]}\n");
                    }
                    break;
                }
            }
        }
    }
    fprintf(stderr, "n=%d m=%d mode=%d consts=%ld states=%ld cycles=%ld "
            "ROTORS=%ld\n", NK, M, MODE, nconst, nstate, ncyc, nrot);
    return 0;
}
