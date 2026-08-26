import sys
sys.path.insert(0,'.')
from linorder import survey_L
print("PREDICTION: q(M) is locked to powers of 2 exactly when the amendment")
print("cycle length L is a power of 2 (then F2[y]/(y^L-1) is local, 1+y is")
print("nilpotent).  An odd factor L' > 1 contributes F_{2^d} with d=ord_{L'}(2),")
print("where 1+zeta is a unit of ODD order dividing 2^d-1.")
print("  L=2 -> only 2-powers.  L=3 -> F4, 1+w = w^2 has order 3.")
print("  L=4 -> only 2-powers.  L=5 -> F16, orders dividing 15.")
print("  L=6 -> odd part 3 -> order 3.\n")
for L, ms, n in ((4,[3,4],400),(5,[3],400),(6,[3],250)):
    survey_L(L, ms, n)
