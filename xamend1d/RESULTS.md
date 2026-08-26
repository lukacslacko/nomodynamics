# The Cross-Amendment Glider Question (1-D)
### Expedition X-A, NOMODYNAMICS program · 2026-08-26
*Successor charter of `glider-question/RESULTS.md`: does 1-D nomodynamics admit a
free glider once a law may amend **another kind**?*

---

## 0. Pre-registration (written before the first run; kept verbatim)

Written 2026-08-26, before any code in this directory was executed. Sealed
predictions, with the odds I actually assigned:

**P1 — Where the glider lives, if anywhere.** My ranking of the three escapes,
by probability that a free glider exists at W = 1 inside a box a machine can
reach:

| escape | mechanism I expect to matter | P(glider exists at W=1) |
|---|---|---|
| **E1 supersession** | a kind with `c = 0`, when active, clears *its own cell* — a genuine self-repealing tail that needs no leftward-growing kind. This is the one mechanism I can see that repeals a trailing edge without also extending it. | **0.45** |
| **E3 fully-cross multi-target** | parity cancellation between two authors of the same slot — the only place where two laws can *silently annul each other's amendment*. | 0.30 |
| **E2 permutation targeting** | the anchor dies, but single-authorship survives, so the whole system stays 𝔽₂-linear given occupancy; I expect the Laurent-domain obstruction to survive in some weighted form. | 0.15 |

P(at least one of the three yields a verified glider in this expedition): **0.55**.

**P2 — The monovariant will work, but only partially.** I predict the weighted
tropical monovariant `Ψ(n) = min_t (α_t(n) + w_t)` with `w_s − c_s ≤ w_{t(s)}`
exists exactly when every φ-cycle has `Σ c ≥ 0`, and yields a **cycle speed
law**: for every φ-cycle C meeting the glider, `sign(d) = sign(ρ_C)` and
`|d|/p ≤ |ρ_C|`, where `ρ_C = (Σ_{k∈C} c_k)/|C|`. In particular I predict
**`ρ_C = 0` ⟹ no glider on that cycle** becomes a theorem. I predict this does
*not* close E2 by itself (the case all-`ρ_C` of one strict sign survives).

**P3 — The uniformly-enabled obstruction generalizes.** §4.3 of the predecessor
proved `M² = (1+σ^s)I` for 2-cycles. I predict the norm argument generalises to
every cycle length L: `(1+N)^p = σ^d` forces `(1+σ^s)^p = σ^{dL}` in
𝔽₂[σ,σ⁻¹], impossible. So any E2 glider must live *at the guard boundary*,
never in a uniformly-enabled region — exactly like Life's glider.

**P4 — SAT frontier.** I predict the exact-window SAT encoding (boundary cells
forced empty at all times, so the bounded model is exact for ℤ) will decide,
within a few CPU-hours: E2 n=2 at interior ≈ 12–16 cells and p ≤ 12; E2 n=3 at
interior ≈ 10–12, p ≤ 8; E1 supersession at interior ≈ 10–12, p ≤ 8 (more
clauses per step: the clear/enact split is nonlinear). I predict UNSAT
everywhere I can reach, *unless* P1's supersession guess is right, in which
case I expect the witness at 4–6 laws and p ≤ 6.

**P5 — Near-misses.** I predict that "moving with debris" (rakes/puffers) is
*also* absent under E2 but **present** under E1 supersession, because
supersession's mutual annihilation makes decaying trailing debris cheap. I
predict at least one named specimen of a bounded-population one-sided advancing
front in the cross-amendment universes that is *not* a glider.

**P6 — What I expect to be wrong about.** If I am refuted, I expect it to be
here: I expect E2 to be provably glider-free and I expect the proof to be the
monovariant. If E2 turns out to contain a glider, the monovariant program is
wrong at its root.

*(Post-hoc scoring of P1–P6 in §9.)*

---

*(Sections 1–9 below are written after the runs; this pre-registration is not
edited.)*
