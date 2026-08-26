#!/usr/bin/env python3
"""fields.py — the kind-field count of a constitution.

By Theorem K the kind-supports X_m of any orbit satisfy u.X = 0 for every u in
the F2 left kernel of the amendment incidence matrix A (A[m][k] = [m in T_k]).
So the number of INDEPENDENT kind-fields is rank_{F2}(A).
"""
import sys

def rank_f2(rows, n):
    rows = [r[:] for r in rows]; r = 0
    for c in range(n):
        piv = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                rows[i] = [x ^ y for x, y in zip(rows[i], rows[r])]
        r += 1
    return r

def fields(T, n):
    A = [[1 if m in T[k] else 0 for k in range(n)] for m in range(n)]
    return rank_f2(A, n)

CASES = [
 ("MIRROR (X-E)        n=2 W=1 |d|=2", [(0,1),(0,1)], 2, 2),
 ("TRIAD-5/3 (X-E)     n=3 W=2 |d|=5", [(0,1,2)]*3, 3, 5),
 ("X-A n=3 speed 2/3   n=3 W=1 |d|=2", [(2,),(0,1),(0,1,2)], 3, 2),
 ("X-A DRIFTER-1/2     n=3 W=1 |d|=1", [(0,2),(0,1),(0,1)], 3, 1),
 ("X-E n=3 (5,2)       n=3 W=1 |d|=2", [(1,2),(0,),(0,)], 3, 2),
 ("X-A n=4 speed 3/4   n=4 W=1 |d|=3", [(0,2),(0,2),(0,1,2,3),(0,1,2,3)], 4, 3),
 ("X-A n=4 speed 6/7   n=4 W=1 |d|=6", [(0,1,2,3),(1,3),(0,1,2,3),(0,1,2,3)], 4, 6),
 ("X-A n=4 speed 3/5   n=4 W=1 |d|=3", [(0,1,3),(2,),(0,1,3),(2,)], 4, 3),
 ("TANDEM-1 (X-A)      n=2 W=1 |d|=1", [(0,1),(0,1)], 2, 1),
]
print("%-36s kinds fields  |d|" % "specimen")
for name, T, n, d in CASES:
    print("%-36s %5d %6d %4d" % (name, n, fields(T, n), d))
