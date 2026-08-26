# Pre-registration — Expedition X-D (structure theory of cross-amendment)
*Written 2026-08-26 BEFORE any run of this expedition. Kept verbatim; scored in
RESULTS.md §8. Author: X-D. Nothing below was edited after the first census.*

## P1 — Survival audit (my predicted verdicts)

| theorem | predicted verdict |
|---|---|
| Gridlock | SURVIVES verbatim, all semantics (guards never read kinds) |
| Single-Author | FAILS; survives exactly when the amendment relation has in-degree ≤ 1 |
| parity ≡ OR | FAILS with Single-Author; minimal split at 2 placed laws |
| Dead Letter | FAILS under parity; SURVIVES under OR verbatim |
| Anchor (permanence of eldest law) | FAILS; minimal counterexample ≤ 3 laws |
| Anchor (frontality / confinement) | SURVIVES in weakened form — I predict a *path-sum* generalisation |
| 2-D ray confinement | FAILS as stated (diagonals); survives as bounded-width ray bundle |
| all periods powers of 2 | FAILS in 1-D cross-amendment; first non-2-power period ≤ 3 laws |

## P2 — Balance

- P2.1 Minimum balanced code: **2 placed laws and 2 distinct kinds**, both tight.
- P2.2 A balanced code exists already in a **2-kind** constitution (t = const).
- P2.3 The coordinator's duality as literally stated ("non-injectivity forces a
  present kind of in-degree 0") I expect to be **TRUE**; I will try to break it.
- P2.4 Balanced codes are rare: < 1 % of fixed codes in any census box.
- P2.5 Balance exists under `super` (parity clear-votes cancel) and NOT under
  `super_or`. Balance exists under multi-target.
- P2.6 Balanced codes can be made arbitrarily large by disjoint union.
- P2.7 Balance is *not* an attractor: random seeds almost never land on one.
- P2.8 Quasi-balance ("cryptic" codes: constant occupancy, live interior) exists
  already in **own-kind** dynamics at period 2, and its periods are powers of 2.

## P3 — The two-kind periodic table (1-D, W=1)

- P3.1 The census box 2916 constitutions × all seeds of span ≤ 6 is dominated by
  FIXED (> 50 %), with GROWING second.
- P3.2 Symmetry group is ℤ₂(mirror) × ℤ₂(kind relabel), order 4, acting freely
  enough to give ≈ 4× reduction on constitutions.
- P3.3 Period spectrum: own-kind block gives only {2,4}; the swap (reciprocal)
  block adds 6, 8, 12; the constant-target blocks add odd periods, first at 3.
- P3.4 **Zero gliders** in the whole 2-kind box (X-A's territory; I predict the
  no-go extends to all 2-kind constitutions at W=1).
- P3.5 EXTINCT is far more common in constant-target blocks than own-kind.

## P4 — Semantic lattice

- P4.1 Gridlock is the single most robust theorem in the field; it survives every
  semantics whose guard contains a vacancy clause and fails the moment one does
  not (purely positive quorum guards).
- P4.2 `entrenchment` (an immune kind) is **barren** — it only pins things.
- P4.3 `sunset-by-default` (laws decay unless re-enacted) is **alive** and is the
  most promising new axis, because it destroys the Anchor Theorem's H3.
- P4.4 `quorum guards` are alive but change nothing structural (Gridlock, Anchor
  and confinement all survive; only the census changes).
- P4.5 `enact-only / repeal-only` are monotone and therefore barren dynamically,
  but they give a *second species of balance* (redundant, not cancelling).

## P5 — The sharpest thing I expect to find

That the true generalisation of the Anchor Theorem is a statement about the
**offset-sum around the cycles of the amendment functional graph**, and that
motion is impossible whenever those sums vanish.
