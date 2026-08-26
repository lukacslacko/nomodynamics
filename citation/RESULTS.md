# Expedition Y-A — the citation sector

*Chapter three of nomodynamics. Scored against `CITATION.md` (frozen
2026-08-26, before this expedition ran). Honesty tiers throughout:
**[established]** = proved here or cited from a proved result;
**[measured]** = machine-checked over a stated box, with the box stated;
**[interpretation]** = reading of an established fact;
**[original proposal]** = conjecture or construction sketch, not completed.*

---

## 0. Pre-registration

*Written before the first census run, from armchair reading of the definition
in `CITATION.md` §2 and of `xnomos.enabled`. Kept verbatim whatever happens.
Where an expectation was already close to a proof when written, that is said so
here, so that a later "confirmed" cannot be read as a lucky guess.*

**P1 — Citation is inert at one kind.** With `|K| = 1`, "a law of kind 0 stands
at `i+a`" and "some law stands at `i+a`" are the same predicate, so the whole
citation alphabet collapses. The smallest sector where citation can do anything
is `n = 2`. (Believed near-certain; a one-line argument.)

**P2 — The plenum theorem (Y1) holds but nearly empties out.** The full plenum
is frozen because every exception clause, whatever it names, is satisfied by a
cell that carries every kind. But the *sharp* criterion will not be "the code is
full": it will be "every cell of the region carries the **exception image**
`E(C) = {h_k : h_k ≠ any}`". Expected consequence: Y1 is technically true and
practically vacuous, because `E(C)` can contain kinds that the dynamics never
enacts. Confidence high.

**P3 — Gridlock's epitaph is a condition on the citation digraph.** I expect a
clean iff: *every solid region is interior-frozen* ⟺ for every kind `k`,
`h_k ∈ {any, k, g_k}`. Confidence ≈ 0.75 that exactly this condition comes out.

**P4 — The bulk is a 0-dimensional dynamical system.** In a region where every
cell carries the same kind-set `U`, offsets are invisible, so the interior
should evolve by a map `β : 2^K → 2^K` depending only on the guards and target
sets. Prediction: this map is exact on homogeneous ring codes for *every*
modulus, giving certified oscillators inside solid code with periods up to
`2^n`, and `β(K) = K` always (which is Y1). Confidence high.

**P5 — Y2 (Out-Degree Law survives) holds.** The monovariant argument only ever
uses "the only laws that can toggle kind `t` at cell `j` are placed laws of
kinds `k` with `t ∈ T_k` at `j − c_k`", which never mentions the guard. I
therefore expect Y2 to survive **verbatim**, and I expect the serious search to
find nothing. Confidence 0.9. *I flag in advance that the charter's stated
reason ("guards only thin the actor set") is **wrong** — citation can make
strictly more laws active than occupancy does; the right reason is that the
proof never reads the guard at all.*

**P6 — Citation buys the unconditionally active law, and that is the whole
mechanism.** Under occupancy no law is ever active regardless of context (the
exception cell, if occupied, always blocks). Under citation, naming a kind that
is never enacted makes the exception clause vacuous. Prediction: this single
device explains Gridlock's death, and it will let citation constitutions realise
**𝔽₂-linear cellular automata** — hence Sierpinski growth on ℤ with *own-kind*
targeting, which chapter one proved impossible in its sector. Confidence 0.8.

**P7 — Y5 (a replicator) falls out of P6.** If the linearisation works, `Φ` is
`I + N` over 𝔽₂ and Frobenius gives `Φ^{2^j} = I + N^{2^j}`: at `t = 2^j` every
finite seed stands beside a disjoint copy of itself. Prediction: a replicator
exists, is provable rather than found, and replicates *every* seed. Confidence
0.7 conditional on P6.

**P8 — Y3 (computational substrate).** The citation guard is literally
`p ∧ ¬q` on kind-fields, and parity resolution is XOR, so I expect a full gate
inventory and, beyond the charter's prediction, an exact simulation of arbitrary
1-D cellular automata at O(1) steps per CA step. Confidence 0.6 for the full CA
simulation, 0.85 for the gate inventory. Turing-universality on ℤ needs a
gate-laying front that outruns the computation; I expect to sketch it and
**not** complete it.

**P9 — Census shape.** Over the complete `n = 2`, `W = 1` citation box I expect:
a large majority extinct/fixed; gliders present but rarer *per constitution*
than in the occupancy corner (citation more often kills the guard than helps
it); and a new, sizeable class the earlier chapters could not produce —
codes that are solid and still moving. I expect the residue of unresolved
trajectories to be small (< 1%).

**P10 — Y4 (linear growth) is a triviality.** `|S_t| ≤ n·(span_0 + 2Wt + 1)` in
1-D holds for *any* constitution, citation or not, because the light cone grows
by `W` per side per step and a cell holds at most `n` laws. Confidence: this is
a proof, not a prediction. What is *not* trivial is whether the rate `2Wn` is
attained; I expect it is.

**P11 — Self-citation is degenerate at offset 0.** `g_k = k` with `a_k = 0` is a
tautology (the law stands at its own cell) and `h_k = k` with `b_k = 0` is a
contradiction. So the interesting self-citation is at nonzero offset, and I
expect self-citation to behave qualitatively differently from cross-citation:
self-citation cannot make a law unconditionally active in a region that contains
its own kind, cross-citation can.

**Anti-predictions (things I expect NOT to find).** No glider at out-degree ≤ 1
(P5). No super-linear growth in 1-D (P10). No violation of Single Author,
Dead Letter (OR), Anchor (own-kind), Path-Sum Confinement, or the Balance
cohort criterion — all of these read only the target sets, never the guard.
