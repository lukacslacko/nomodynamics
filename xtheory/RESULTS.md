# The Structure Theory of Cross-Amendment
### Expedition X-D, NOMODYNAMICS · 2026-08-26
*Which laws of the solvable sector survive when a law may amend another kind,
what replaces the ones that fall, and the complete classification of the
two-kind universe.*

**Honesty labels used throughout: `[proved]` = theorem with proof given here;
`[measured]` = exact count over a stated box, complete unless marked `sampled`;
`[proposal]` = original conjecture / interpretation, not established.**

---

## 0. Verdict in one page

The own-kind sector rested on four pillars. Cross-amendment breaks two of them
and leaves two standing in changed shape:

| pillar | verdict | what replaces it |
|---|---|---|
| **Gridlock** | **survives verbatim**, everywhere on the lattice | — (guards never read kinds) |
| **Single-Author** | **survives exactly on permutation constitutions** | in-degree ≤ 1 criterion |
| **Dead Letter** | **fails under parity, survives under OR** | the **Balance Theorem** |
| **Anchor (permanence)** | **fails — from one placed law** | **Path-Sum Confinement** |

and the new organising object is the **cycle offset-sum**. Every kind's forward
orbit in the amendment digraph ends in a cycle *Z*; the vector
S_Z = Σ_{k∈Z} c_k is the direction the whole component can ever travel. It
controls growth (S_Z = 0 ⟹ bounded forever), it controls direction (a glider's
velocity must be a positive multiple of S_Z), and it controls the clock
(S_Z ≠ 0 ⟹ constant-occupancy periods are powers of 2). Own-kind is the case
of one-element cycles, where S_Z = c_k and everything collapses to the ray
confinement and the anchor already known.

The two most quotable results:

> **The Balance Theorem.** Under parity, a code stands perpetually active yet
> unchanged iff its active laws fall into *cohorts* — even-sized groups of
> distinct kinds proposing the same amendment at the same cell, which annihilate.
> Consequently, and this is the duality: *a code can move only if every present
> provision is amendable by an active one (its alphabet carries a permutation);
> a code can stand perpetually active yet unchanged only if some active
> provision is amendable by none — entrenched.* The minimum is two laws in one
> cell; the maximum is unbounded; and 70 % of the balanced verdicts in a
> 143-million-run complete census are **reached**, not seeded — balance is an
> attractor, not a coincidence.

> **The Zero-Sum No-Go.** If every amendment cycle reachable from the seed has
> vanishing offset-sum, the code is confined to a fixed finite region for all
> time. Complete certificate: of the 2916 two-kind constitutions, 810 satisfy
> the hypothesis; across their 39,813,120 runs there is **not one** growing
> code, while the remaining 2106 constitutions produce all 15,101,294.

And one negative result that matters for the whole programme: the field's
central no-go rests on **permanence**, not on own-kind targeting. Drop H3
(let statutes lapse unless re-enacted — *sunset by default*) and **free
gliders on ℤ appear at 11–15 % of the census**, with speeds 1, 2/3, 1/2, 1/3,
1/4, 1/6. Nothing else on the semantic lattice does this.

---

## 1. Pre-registration

Written before the first run, kept verbatim in [`PREREG.md`](PREREG.md).
Scorecard in §8. Headline: **P2.3 refuted** (the coordinator's duality as
literally stated is false), **P2.7 refuted** (balance *is* an attractor),
**P1 anchor prediction beaten** (the minimal anchor death is one law, not
three), **P4.3 confirmed** (sunset is the live axis).

---

## 2. Setting

A **constitution** is a finite kind set *K*; each k ∈ K carries a rule
(a_k, b_k, c_k) ∈ (ℤ^d)³ and a target t(k) ∈ K (multi-target: t(k) ⊆ K).
A **code** is a finite S ⊆ ℤ^d × K. occ(i) = "some law of any kind at i".
Law (i,k) ∈ S is **active** iff occ(i+a_k) ∧ ¬occ(i+b_k). Each active law
emits one **toggle** of kind t(k) at cell i + c_k. Toggles landing on the same
slot (cell, kind) resolve by **parity** (odd count flips) or **OR** (≥1 flips).
Φ is the synchronous update; σ^v is translation.

The **amendment digraph** G has node set K and edges k → t(k). With out-degree
1 it is a *functional graph*: every component is a directed cycle with in-trees
hanging off it. Write ρ(k) = (tail of length τ_k, cycle Z_k of length L_k) for
the forward orbit of k, and

  **C_r(k) = c_k + c_{t(k)} + … + c_{t^{r−1}(k)}**  (the *r-step path-sum*, C_0 = 0),
  **S_Z = Σ_{k ∈ Z} c_k**  (the *cycle offset-sum*).

Own-kind nomodynamics is t = id: every cycle is a self-loop and S_Z = c_k.

Structural hypotheses (the Anchor Theorem's, `glider-question/RESULTS.md` §2.2):
**H1** own-kind effects · **H2** rigid displacement (a kind-k law emits only at
its own constant offset c_k) · **H3** locality (an untoggled slot is unchanged).
Cross-amendment is exactly "drop H1, keep H2 and H3".

---

## 3. The survival audit

| # | theorem of the solvable sector | verdict | replacement / minimal counterexample |
|---|---|---|---|
| T1 | **Gridlock** — solid code is frozen | **SURVIVES VERBATIM**, every semantics, every dimension | none needed. Sharp hypothesis: *the guard must contain a vacancy clause*; drop it and a solid block is fully active |
| T2 | **Single-Author** — one author per slot; parity ≡ OR | **SURVIVES IFF the amendment relation has in-degree ≤ 1**, i.e. (out-degree 1, finite K) iff **t is a permutation** | multi-authorship from 2 placed laws; parity/OR split at 2 placed laws in **one cell** |
| T3 | **Dead Letter** — fixed ⟺ every law blocked; no balanced constitutions | **SURVIVES under OR and super_or; FAILS under parity, super, enact-only, repeal-only, override, entrenchment** | the **Balance Theorem** (§4). Criterion: Dead Letter holds iff the resolution is *strict* |
| T4 | **Anchor** — the eldest law cannot be repealed | **FAILS**, from a **single** placed law | **Path-Sum Confinement** + the **Zero-Sum No-Go** + **one-sided confinement** when all c_k share a sign |
| T5 | **2-D ray confinement** — each kind on one axis ray | **FAILS as stated**; survives as a *ray bundle* | reach ⊆ finite union of translates of ℕ·S_Z; diagonals are exactly the diagonal S_Z |
| T6 | "all periods are powers of 2" (never a theorem: an observed regularity) | **FAILS** — spectrum {2,3,4,5,6,7,8,9,10,12,14,16,18,30} in the complete two-kind box | **Cryptic Unipotency**: at constant occupancy the period is a power of 2 **iff** no reachable cycle has S_Z = 0 |
| T7 | own-kind census regularity "every cycle has period 2 or 4" (W=1) | **FALSE even in the own-kind sector** | certified own-kind W=1 cycles of period 6 and 8 |

### T1. Gridlock — survives verbatim `[proved]`

**Theorem 1.** *If every cell of i + {0, a_k, b_k : k ∈ K} is occupied, no law
at i is active. Hence a code occupying a solid region has no active law in that
region's interior, and a code occupying all of ℤ^d is a fixed point in every
semantics on the lattice of §6.*

*Proof.* Activity requires ¬occ(i + b_k), which fails. ∎

Nothing in the proof mentions targets, resolution, effect type, entrenchment,
dimension, or the ring/line distinction — the guard reads **occ**, and occ is
target-blind. This is why Gridlock is the most robust theorem in the field:
it lives one level below everything cross-amendment touches.

`[measured]` 708,588 solid codes (all 2916 two-kind constitutions × all
3⁵ kind-assignments of a solid 5-block): **0 active interior laws**.
16,000 (solid ring, semantics) pairs across parity/OR/super/super_or:
**0 non-fixed**.

**Hypothesis audit.** The one load-bearing hypothesis is that the guard
contains a *vacancy clause*. Under a purely positive quorum guard ("active iff
≥ q of my neighbours are occupied") Gridlock inverts: a solid block is fully
active and the vacuum is dead. `[measured]` over all 7 nonempty quorum sets
q ⊆ {0,1,2}, the interior of a solid block is alive **iff 2 ∈ q** — exactly the
predicted criterion.

### T2. Single-Author — a sharp criterion `[proved]`

**Theorem 2.** *Let E = {(k,τ) : τ ∈ t(k)} be the amendment relation.*
1. *If every τ ∈ K has in-degree ≤ 1 in E, then every slot receives at most one
   toggle in every state, and Φ_parity = Φ_OR identically.*
2. *Multiplicity ≥ 2 at a slot forces in-degree ≥ 2 at its kind. It is realised
   exactly when two kinds k ≠ k′ with a common target have jointly satisfiable
   guards at the relative offset c_k − c_{k′}.*

*Proof.* The authors of slot (j,τ) are exactly the laws (j − c_k, k) over
k ∈ E^{−1}(τ), one per k — a kind stands at most once per cell, and c_k is a
constant of the kind. If |E^{−1}(τ)| ≤ 1 the multiplicity is ≤ 1 and "odd"
= "≥ 1", so the two resolutions agree. For (2), two authors of one slot are two
laws (j − c_k, k), (j − c_{k′}, k′) with k ≠ k′ and τ ∈ t(k) ∩ t(k′); placing
them and satisfying both guards is the whole content. ∎

The realisability clause is not vacuous — 15 of the 27 W=1 rules are
unconditional dead letters (`rings/RESULTS.md` Lemma 0′) — but it is generic:
`[measured]` 3,792 of 209,952 non-injective two-kind codes of span ≤ 4 already
split parity from OR in a single step.

**Corollary 2.1.** With out-degree ≡ 1 on a finite K, in-degree ≤ 1 everywhere
⟺ t is a bijection. **The exactly-solvable resolution axis survives on exactly
the permutation constitutions** — own-kind (t = id) and reciprocal amendment
(t a fixed-point-free involution) are its two poles. This is Lemma 2.2 of
`glider-question/RESULTS.md` recovered as an iff.

`[measured]` Complete two-kind box, span ≤ 8, 143,327,232 runs per resolution:
the id- and swap-blocks have **byte-identical** census vectors under parity and
OR — id: extinct 150,586 · fixed 22,150,120 · cycle 6,763,998 · growing
6,767,104; swap: extinct 102,164 · fixed 20,774,128 · cycle 13,744,018 ·
growing 1,211,498 — with balanced 0 and glider 0 in both;
the const-blocks differ (parity: fixed 59.03 %, balanced 2.19 %, cycle 28.82 %;
OR: fixed 59.17 %, balanced 0 %, cycle 30.50 %). At state level, 209,952
injective-target codes stepped in both resolutions: **0 divergences**;
209,952 non-injective codes: 3,792 divergences (1.81 %).

**Minimal split: two placed laws, in one cell.** Kinds 0 and 1 are both the
rule (0,−1,−1), both amending kind 0; seed = both kinds at cell 0. Both are
active (their own cell is occupied, the cell to the left is empty) and both
toggle slot (−1, kind 0). Under parity the two proposals cancel; under OR one
of them passes and a kind-0 law appears at cell −1.

### T3. Dead Letter — a criterion on the resolution, not the targeting `[proved]`

Call a resolution rule R (mapping a current slot value v ∈ 𝔽₂ and a nonempty
multiset M of arriving effects to a new value) **strict** if R(v,M) ≠ v for
every v and every nonempty M.

**Theorem 3.** *Under H3, Φ(S) = S for every code with no active law. If R is
strict, the converse holds: fixed ⟺ every law blocked (Dead Letter). If R is
not strict and the failure is realisable by a code, balanced codes exist.*

*Proof.* An active law emits an effect; a strict R changes that slot. ∎

| semantics | strict? | Dead Letter | balanced codes, 2-kind box span ≤ 4 (559,872 codes) |
|---|---|---|---|
| toggle + OR | **yes** | **survives** | **0** |
| toggle + parity, in-degree ≤ 1 | vacuously (\|M\| ≤ 1) | **survives** | **0** |
| toggle + parity, in-degree ≥ 2 | no (even M) | **fails** | 3,176 |
| supersession + OR | **yes** | **survives** | **0** |
| supersession + parity | no (two clear-votes) | **fails** | 4,368 |
| enact-only | no (enact onto 1) | **fails** | 25,824 (span ≤ 3 box) |
| repeal-only | no (repeal a 0) | **fails** | 35,408 (span ≤ 3 box) |
| override (lex posterior) | no | **fails** | 11,056 (span ≤ 3 box) |
| toggle + parity + entrenched kind | no | **fails** | 13,056 (span ≤ 3 box) |

`[measured]` and at census scale: over the complete span-≤8 two-kind box,
**OR gives 0 balanced verdicts in 143,327,232 runs** while parity gives
1,572,788.

**Reading.** Own-kind kept Dead Letter not because of anything about
*amendment*, but because Single-Author made every toggle multiset a singleton,
and every resolution is strict on singletons. Dead Letter was a corollary of
Single-Author all along. There are, moreover, **two species of balance**:
*cancelling* balance (parity, supersession-parity: proposals annihilate) and
*redundant* balance (enact-only, repeal-only, override: the proposal passes but
the slot already had that value).

### T4. Anchor — fails as permanence, survives as confinement

**T4a. Permanence fails, and it takes one law.** `[measured, complete]`

Minimal witness over all 2916 two-kind constitutions × all seeds of span ≤ 3:
a **single** placed law suffices.

```
ANC-1   kind 0 = (-1, 1,-1) -> 1        seed: kind 1 at cell 0
        kind 1 = ( 0, 1, 1) -> 0
    .B..     c_1 = +1 > 0, so the Anchor Theorem would pin B at cell 0 forever
    .BA.     B enacts A at cell 1 ...
    ..A.     ... and A (c_0 = -1) repeals B at cell 0.  The code survives.
    ..A.
```

Control: **the Anchor Theorem holds throughout the own-kind block** —
139,968 own-kind codes × 12 steps, **0 anchor deaths** `[measured, complete]`.

**T4b. Path-Sum Confinement — the replacement.** `[proved]`

**Theorem 4 (Path-Sum Confinement).** *Assume H2 and H3 (the guard, the
resolution, the dimension and the semantics are otherwise arbitrary). Then for
every n ≥ 0*

  **S_n ⊆ ⋃_{(i,k) ∈ S_0} ⋃_{r=0}^{n} { ( i + C_r(k), t^r(k) ) }.**

*Proof.* Induction on n; the case n = 0 is the term r = 0. Let (j,τ) ∈ S_{n+1}.
Either (j,τ) ∈ S_n and H3 gives it for free, or (j,τ) was toggled into
existence, so by H2 some active law (j − c_κ, κ) ∈ S_n with τ = t(κ). By
induction (j − c_κ, κ) = (i + C_r(k), t^r(k)) for some (i,k) ∈ S_0 and r ≤ n,
with κ = t^r(k). Then j = i + C_r(k) + c_{t^r(k)} = i + C_{r+1}(k) and
τ = t^{r+1}(k). ∎

**Corollary 4.1 (linear growth, every dimension).** |S_n| ≤ |S_0|·(n+1); the
growth exponent is α ≤ 1 always. (Generalises `nomos2d` Theorem 3's α ≤ 1 from
own-kind to arbitrary functional targeting.)

**Corollary 4.2 (ray-bundle structure).** For r ≥ τ_k,
C_r(k) = C_{τ_k}(k) + q·S_{Z_k} + (a partial sum of Z_k), q = ⌊(r−τ_k)/L_k⌋.
Hence {C_r(k) : r ≥ 0} ⊆ F_k + ℕ·S_{Z_k} with |F_k| ≤ τ_k + L_k, and the reach
of the whole code is a finite union of at most |S_0|(τ+L) translates of the ray
ℕ·S_Z, one direction per component of the amendment digraph.
*Own-kind is L = 1, S_Z = c_k: the axis-ray confinement of `nomos2d` Theorem 3
is exactly this special case.* In general S_Z need not be an axis vector —
**that is precisely why 2-D cross-amendment unlocks diagonal motion, and the
theorem names the diagonal: it is the cycle offset-sum.**

**Corollary 4.3 (Zero-Sum No-Go).** *If S_{Z_k} = 0 for every kind k reachable
from a seed kind, the reach set is finite. The code is confined to a bounded
region for all time, the reachable state space is finite, and the orbit is
eventually periodic — no growth, no front, no glider, ever.*

`[measured, complete]` Of the 2916 two-kind constitutions, **810 satisfy the
hypothesis**; over their 810 × 49,152 = **39,813,120 runs there is not one
GROWING verdict**, while the remaining 2106 produce all 15,101,294. Plus 4,000
random ≥2-kind zero-sum constitutions × 200 steps: 0 escapes from the
predicted reach bound.
*(The converse is false: 642 of the 757 symmetry orbits have no growth at all,
including many with S_Z ≠ 0. Zero-sum is sufficient, not necessary.)*

**Corollary 4.4 (displacement law).** *If Φ^p(S) = σ^v(S) with v ≠ 0, then v is
a positive rational multiple of S_Z for every component Z present in S; in
particular no present component may have S_Z = 0, and all present components'
offset-sums must be positively parallel.*

*Proof.* supp(S) + mv ⊆ reach(S) for all m ≥ 0, and reach(S) is a finite union
of translates of the rays ℕ·S_Z. Pigeonhole a fixed x ∈ supp(S) into one ray
translate for two indices m < m′; then (m′−m)v = (q′−q)S_Z with q′ > q. ∎

This is the exact replacement of the Anchor Theorem's no-glider corollary in the
cross-amendment sector: it does not forbid motion, it **says where to look** —
the cycle offset-sum is the velocity direction, and the cycle must not balance.

**T4c. One-sided confinement — the surviving fragment of the Anchor.** `[proved]`

**Theorem 5.** *If c_k ≥ 0 for every kind reachable from the seed, then
min supp(S_n) is non-decreasing: the code can never move left. If c_k > 0 for
every reachable kind, the leftmost occupied cell is permanent with its entire
law-set and no free glider exists. (Mirror for ≤ 0 / < 0.)*

*Proof.* Every toggle is emitted from an occupied cell i and lands at i + c ≥ i
(resp. > i), so no cell strictly left of min supp receives anything; H3 keeps
it empty. In the strict case the leftmost occupied cell receives no toggle at
all, hence is frozen, hence pinned — and a fixed cell defeats translation by
the finite-support argument of Anchor Corollary 1. ∎

The *per-kind* anchor dies with H1; the *global* anchor survives whenever the
offsets do not disagree in sign. **The open case for 1-D gliders is therefore
exactly: mixed signs with S_Z ≠ 0.** (Handed to X-A.)

**T4d. Supersession keeps ray confinement.** `[proved]` Under supersession an
active law enacts **its own kind** at its target (clears are removals only), so
supp_k(S_n) ⊆ supp_k(S_0) + ℕ·c_k exactly as in own-kind. Hence linear growth,
a ray bundle, and: *a supersession glider's displacement must be a positive
multiple of c_k for every present kind k.* `[measured]` 20,000 trajectories ×
50 steps: 0 escapes. This is a free monovariant for the supersession hunt.

### T5. 2-D ray confinement — fails as stated, survives as a bundle `[proved]`

By Corollary 4.2 the statement "every law of kind T lies on the ray
seed_T + ℕ·c_T" holds exactly when t = id. Minimal breakage: the 2-cycle
0 ↔ 1 with c_0 = (1,0), c_1 = (0,1) has S_Z = (1,1) and the reach is a
*diagonal* ray; neither kind stays on an axis. What survives is the bundle:
finitely many rays in the directions S_Z, with bounded transverse spread, so
1-dimensional growth and no cone-filling persist in every dimension.
`[measured]` 4,000 random 2-D cross-amendment constitutions × 40 steps:
0 escapes from the path-sum reach set. (2-D census: X-B's ground.)

### T6. Powers of 2 — the correct statement `[proved]` + `[measured]`

**Theorem 6 (Cryptic Unipotency).** *Suppose occ(S_n) is constant on a time
interval. Then on that interval the state evolves 𝔽₂-linearly,
x ↦ (I + N)x, where N is the **amendment operator***

  (Nx)(j,τ) = Σ_{k : t(k)=τ} g_k(j − c_k)·x(j − c_k, k),
  g_k(i) = occ(i+a_k)·(1 − occ(i+b_k)).

*If every cycle reachable from a present kind has S_Z ≠ 0, then N is nilpotent,
I + N is unipotent, and every constant-occupancy cycle has period a power of 2.*

*Proof.* N^r x is nonzero only along a chain j_0, j_1 = j_0 + c_{k_0}, …, j_r
of cells all lying in the finite occupied set (the masks g vanish elsewhere on
a finite code), with kinds k_s = t^s(k_0). After the tail, each L steps advance
the position by S_Z; picking a linear functional φ with ⟨φ, S_Z⟩ > 0 gives
⟨φ, j_r⟩ → ∞, so long chains leave the finite set and N^r = 0. Then
(I+N)^{2^m} = I + N^{2^m} = I over 𝔽₂ once 2^m exceeds the nilpotency index. ∎

**Sharpness.** With a zero-sum cycle the chain can circulate inside the
occupied set forever and N need not be nilpotent. **The zero-sum cryptic clock**
(certified specimen `CRY-1`) is the minimal witness found:

```
kind 0 = (0,-1, 1) -> 2        cycle 0 -> 2 -> 1 -> 0
kind 1 = (0, 1,-1) -> 0        offsets (+1, 0, -1),  S_Z = 0
kind 2 = (-1,1, 0) -> 1
seed: kind 2 at -2 ; kinds {0,2} at 2 ; kinds {0,1} at 3

  .C...##..      occupancy is {-2, 2, 3} FOREVER;
  .C...C#..      the kind content has period 3.
  .C...##..      A code that looks gridlocked from outside and is
  .C...##..      running a 3-cycle inside.
```

`[measured, complete]` Two-kind box, all 2916 constitutions × 144 seeds of
span ≤ 4: 62,784 **cryptic** codes (constant occupancy, live interior), period
spectrum {2: 61,024 · 4: 1,760} — all powers of 2. Two kinds are not enough for
the sharpness witness; three are. `[measured, sampled]` 40,000 random ≥2-kind
runs produced 20 non-power-of-2 cycles, of which **exactly one** had frozen
occupancy, and that one had S_Z = 0 — the prediction hit on the nose.

**What the census says about periods.** `[measured, complete]` span-≤8 two-kind
box, parity: spectrum **{2,3,4,5,6,7,8,9,10,12,14,16,18,30}**, max period 30.
By block: own-kind {2,4,6,8} · reciprocal {2,4,6,8,12,16,18,30} · const-target
{2,3,4,5,6,7,8,9,10,12,14,16,18}. Under OR the odd periods vanish
(const-target becomes {2,4,6,8,12,16,18}).
**Within the two-kind box, odd periods > 1 occur only in the non-injective
(multi-author) blocks, and only under parity.** `[measured]` This is a *two-kind
artefact, not a law*: a 120,000-run sample over 2–4-kind constitutions finds
period 3 in **permutation** (single-author) constitutions too (17 instances),
and period 28 in a 4-kind permutation constitution.

### T7. A negative result about the own-kind census `[measured, certified]`

`glider-question/RESULTS.md` §5.2 reports, across 9.07 M W=1 own-kind seeds,
"every cycle has period 2 or 4 … window-1 own-kind nomodynamics is temporally
rigid: blink or freeze." **That regularity is false.** Its ≤4-law/5-cell strata
were complete but its 5- and 6-law strata were sampled, and the counterexamples
live there:

```
OWN-6   own-kind, W = 1, two kinds, 5 laws in 5 cells, PERIOD 6
        kind A = (0,-1, 1)     (the sunset clause)
        kind B = (0, 1,-1)     (its mirror)
        seed: A@0, {A,B}@2, B@3, B@4

  .A.#BB.      t=0
  .AA#AB.      Re-verified over three full periods through the
  .A.##B.      independent reference engine of xlib.py.
  .AA#.B.      The complete span-<=8 two-kind own-kind block also
  .AB#BB.      contains period 8.
  .A##.B.
  .A.#BB.      t=6 = t=0
```

The own-kind period spectrum at W=1 is therefore at least {2,4,6,8}. The
*theorems* of the own-kind sector are untouched; only this census-level
regularity falls.

---

## 4. The Balance Theorem

Throughout: parity resolution, finite K, single targeting unless stated.
**A(S)** = kinds with an active law in S. **P(S)** = kinds present.
A code is **balanced** if Φ(S) = S and at least one law of S is active.

### 4.1 Structure

**Theorem 7 (Cohort structure).** *Φ(S) = S iff every slot receives an even
number of toggles, i.e. iff the active laws of S partition into **cohorts** —
classes of the relation (i,k) ~ (i′,k′) ⟺ (i + c_k, t(k)) = (i′ + c_{k′}, t(k′)) —
each of even size. Distinct laws in one cohort carry distinct kinds. A cohort of
size m requires a kind of in-degree ≥ m in the amendment digraph.*

*Proof.* Fixedness ⟺ every slot flips an even number of times ⟺ even
multiplicity. Two active laws of the same kind sharing a target slot would
stand at the same cell (i + c_k = i′ + c_k ⟹ i = i′), hence be the same law. ∎

> *Reading: a balanced code is one in which every amendment on the floor is
> co-signed an even number of times, and therefore defeated by its own
> co-signatories.*

**Theorem 8 (Minimality — both bounds tight).** *A balanced code has at least
two active laws and at least two distinct kinds. Both are attained.*

The witness `BAL-1` is **two laws in one cell**:

```
kind 0 = (0,-1,-1) -> 0        seed: kinds {0,1} at cell 0
kind 1 = (0,-1,-1) -> 0
  .#..      both laws active forever (own cell occupied, left cell empty);
  .#..      both repeal the (absent) kind-0 law at cell -1;
  .#..      the two repeals cancel.  Under OR the repeal passes and a
            kind-0 law appears at cell -1.
```

*Degenerate exception.* With multi-target and a **repeated** target inside one
law (t(k) = {τ, τ}) a single law annihilates itself: a provision that proposes
the same amendment twice. Requiring distinct targets within a law restores the
bound — `[measured]` 249,410 single-law codes over random multi-target
constitutions with distinct targets: **0 balanced**.

### 4.2 The duality

**Theorem 9 (Balance ⟹ Entrenchment).** *If S is balanced then t|_{A(S)} is
non-injective and **A(S) ⊄ t(A(S))**: some kind k ∈ A(S) is targeted by no
active kind of S. Since a fixed code's active set is constant for all time, no
kind-k toggle is ever emitted, so every kind-k law of S is **permanent**.
A balanced code always contains an entrenched provision.*

*Proof.* By Theorem 7 there are active k ≠ k′ with t(k) = t(k′), so
|t(A)| ≤ |A| − 1. If A ⊆ t(A) then |A| ≤ |t(A)| ≤ |A| − 1. ∎

**Theorem 10 (Motion ⟹ universal amendability).** *If Φ^p(S) = σ^v(S) with
v ≠ 0, let P be the kinds present in S and A\* the kinds active at some phase
of the period. Then P ⊆ t(A\*); together with A\* ⊆ P this forces
A\* = P = t(P), so **t restricted to a glider's alphabet is a permutation** and
that alphabet is a union of cycles of the amendment digraph.*

*Proof.* The orbit is periodic up to translation, so the active set repeats
with period p and A\* is well defined. If k ∈ P were targeted by no kind of
A\*, no kind-k toggle would ever be emitted, so by H3 supp_k(S_n) = supp_k(S_0)
for all n — contradicting supp_k(S_{mp}) = supp_k(S_0) + mv with supp_k ≠ ∅ and
v ≠ 0. Hence P ⊆ t(A\*). Out-degree 1 gives |t(A\*)| ≤ |A\*|, and A\* ⊆ P
gives |A\*| ≤ |P|; chaining, |P| ≤ |t(A\*)| ≤ |A\*| ≤ |P|, so all are equal:
A\* = P, t(P) = P, and t|_P is injective, hence a permutation of P. ∎

**Corollary (the duality, in final form).**

> **A code can move only if its alphabet satisfies A\* = P = t(P): every
> present provision is amendable by an active one, and the constitution
> restricted to the code is a permutation.
> A code can stand perpetually active yet unchanged only if A ⊄ t(A): some
> active provision is amendable by none, and is thereby entrenched.**

The dividing line is one containment: **A ⊆ t(A)**. Motion needs it; balance
forbids it. Combined with Corollary 4.4, a glider's alphabet is a union of
cycles with positively-parallel nonzero offset-sums, and its velocity is a
positive multiple of them.

### 4.3 Refutations and sharpness

**(i) The coordinator's seed duality is FALSE as literally stated.**
It claimed: *non-injectivity forces some present kind to have in-degree 0 in
the amendment digraph, i.e. to be structurally immortal.* Counterexample
`BAL-3`, machine-verified:

```
kind 0 = (0, 1, 1) -> 2     in-degrees: kind0 <- {2} = 1
kind 1 = (0,-1,-1) -> 2                 kind1 <- {3} = 1
kind 2 = (0, 1, 0) -> 0                 kind2 <- {0,1} = 2
kind 3 = (0, 1, 0) -> 1                 kind3 <- {} = 0
seed: kind 0 at cell 0, kind 1 at cell 2     ->  BALANCED, 2 active laws

  .A.B..     Every PRESENT kind (0 and 1) has in-degree >= 1.  The only
  .A.B..     in-degree-0 kind is 3, which is absent and can never appear.
  .A.B..
```

Entrenchment in the Balance Theorem is **dynamic** — relative to the code's own
active set — not structural. The graph version is a corollary only when the
present alphabet is t-closed. `[measured]` Theorem 9 (the dynamic form)
verified on 28,672,000 codes over 8,000 random 3-kind constitutions: 207,379
balanced, **0 violations**; and on 600,000 random ≥2-kind codes for the
non-injectivity half: 1,168 balanced, 0 violations.

**(ii) Theorem 9 fails for out-degree ≥ 2** — multi-target amendment buys
balance *without* entrenchment. Witness `BAL-5`:

```
kind 0 = (1,-1,-1) -> {0,1}    seed: kinds {0,1} at cell 2, kind 1 at cell 3
kind 1 = (0,-1,-1) -> {0,1}
  .#B..      A = {0,1} = t(A);  NO kind is entrenched;  slots (1,kind0) and
  .#B..      (1,kind1) each receive exactly 2 toggles.  Balanced.
```

So the entrenchment half of the duality is exactly a theorem about
**out-degree 1** — about constitutions in which each provision amends one other.

**(iii) Balance under supersession needs no cross-amendment at all.**
Witness `BAL-6`: kinds 0 = 1 = (0,−1,0), **own-kind targets**, both at cell 0.
Both are active; both target the occupied cell 0, so both cast a *clear-vote*;
under `super` (parity clear-votes) the two clears cancel. Balanced. Under
`super_or` the cell is cleared and Dead Letter survives. `[measured, complete]`
two-kind box span ≤ 4: `super` 4,368 balanced, `super_or` **0**.

### 4.4 Classification and census

**Balanced codes can be arbitrarily large.** `[measured]` Disjoint unions of
`BAL-1` at spacing 3 are balanced for 1, 2, 5, 20 and 100 copies (up to 200
active laws) — the W=1 offsets cannot see across a two-cell gap.

**Balanced codes can carry arbitrarily many distinct active kinds** — the
**cohort construction** `COH-2m`:

```
kinds 0..m-1     = (0,-1, 1) -> 2m       (all m at cell 0)
kinds m..2m-1    = (0, 1,-1) -> 2m       (all m at cell 2)
kind  2m         = anything, ABSENT
seed: cell 0 carries kinds 0..m-1 ; cell 2 carries kinds m..2m-1

  .#.#.        2m active laws of 2m distinct kinds, all co-targeting the
  .#.#.        slot (cell 1, kind 2m).  Even -> cancel.  Verified for
  .#.#.        m = 1,2,3,4,6,10.  Delete ONE actor and the amendment passes.
```

**Exact counts.** For the *balance champion* `BAL-4` (both kinds the rule
(0,−1,0), both amending kind 0), a code is balanced **iff every run-start cell
— occupied with an empty left neighbour — carries both kinds**. The transfer
matrix on (occupied, empty) prefixes is [[3,1],[1,1]] (from an occupied cell:
3 nonempty masks or a gap; from a gap: only the doubled mask 3, or another
gap), giving the number a(s) of balanced codes of span exactly s:

| s | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| a(s) | 1 | 3 | 10 | 34 | 116 | 396 | 1352 | 4616 |

with **a(s) = 4a(s−1) − 2a(s−2)**, growth rate 2 + √2 = 3.41421…
`[measured, complete]` brute force matches the closed form for every s ≤ 8; the
total over spans 1..8 is 6,528 codes that are *born* balanced, against 49,024
seeds of that constitution whose orbit *ends* balanced (see the attractor
paragraph below).
Hence **balanced codes form a positive-entropy subshift: log₂(2+√2) = 1.7716
bits per cell out of a possible 2. Balance is not measure zero in law-space.**

**Global census.** `[measured, complete]` span-≤8 two-kind box, parity,
143,327,232 runs: **1,572,788 balanced verdicts (1.10 %)**, all of them in the
non-injective blocks (2.19 % of those); **0** in the injective blocks — Theorem
9's non-injectivity requirement, confirmed at census scale. 140 of the 2916
constitutions admit balance; the largest balanced code in the box has 8 active
laws.

**Balance is an ATTRACTOR.** `[measured, complete]` Of the 1,572,788 balanced
verdicts only **470,516 (29.9 %) were balanced at t = 0**; **1,102,272 (70.1 %)
converged to balance from an unbalanced seed.** For the champion, 42,496 of
49,152 seeds converge and 49,024/49,152 end balanced. This refutes
pre-registration P2.7 outright. Balance is fragile *pointwise* (delete one
cohort member and the amendment passes) and abundant and attracting *globally* —
both are true, and together they are the honest picture: **perpetual deadlock
is where a large part of the flow ends up.**

### 4.5 Quasi-balance: cryptic codes

Call a code **cryptic** if occ(S_n) is constant for all n while the kind content
is not: gridlocked from outside, alive inside. Balance is exactly *cryptic of
period 1 with active laws*. `[measured, complete]` Cryptic codes exist already
in **own-kind** dynamics — 62,784 in the two-kind span-≤4 box, periods {2, 4}.

So the own-kind sector forbids only the period-1 case, and by Theorem 6 the
periods of cryptic codes are powers of 2 unless a reachable cycle has zero
offset-sum. Cross-amendment removes the period-1 obstruction (the Balance
Theorem); a zero-sum cycle removes the 2-adic one (`CRY-1`, period 3).
**Balance, cryptic clocks and gridlock are one family indexed by the period,
and the two obstructions that shape it are single-authorship and the cycle
offset-sum.**

---

## 5. The periodic table of two-kind constitutions (1-D)

### 5.1 The box, exactly specified

* kinds: 2 · rules: all 27 triples (a,b,c) ∈ {−1,0,1}³ for each kind
  (729 ordered rule pairs)
* target maps: all 4 functions {0,1} → {0,1}: **id** (own-kind), **swap**
  (reciprocal), **const-0**, **const-1** ⟹ **2916 constitutions**
* seeds: every code of support span ≤ 8, translation-normalised (leftmost cell
  occupied, rightmost cell occupied), every kind-subset per cell:
  3 + 9 + 36 + 144 + 576 + 2304 + 9216 + 36864 = **49,152 seeds**
* window 320 cells, escape margin 28, **budget 1024 steps**
* resolutions: parity and OR ⟹ **143,327,232 runs per resolution, complete**
* a smaller complete box (span ≤ 6, 3072 seeds, 8,957,952 runs, budget 512)
  is also reported and agrees on every qualitative statement.

Certificates: EXTINCT (empty state), FIXED / BALANCED / CYCLE-p (exact
recurrence with displacement 0, BALANCED when ≥1 law is still active), GLIDER
(normalised recurrence with displacement ≠ 0), GROWING (escaped the window),
UNRESOLVED (budget exhausted). The C engine was verdict-checked against a
Python re-implementation of the *same* budget on 4,000 random cases:
**0 mismatches**; and xnomos was duelled against the independent set-based
reference engine of `xlib.py` on the same cases: **0 divergences**.

### 5.2 Symmetry group and the soundness of the quotient `[proved]` + `[measured]`

**Proposition.** *The group G = ⟨μ, ρ⟩ ≅ ℤ₂ × ℤ₂ acts on constitutions, where*
* *μ (mirror): (a,b,c) ↦ (−a,−b,−c) for every kind, target map unchanged;*
* *ρ (kind relabelling by a permutation π): rules r′_i = r_{π(i)},
  target map t′ = π^{−1} ∘ t ∘ π.*

*The classification of a seed is G-equivariant: μ conjugates the dynamics by
the reflection x ↦ −x, ρ by the relabelling of kinds, and both map the seed set
of a given span bijectively to itself. Hence the whole census vector is constant
on G-orbits.*

*Proof.* Reflection is an automorphism of ℤ carrying occ to occ ∘ (−1), so
(i,k) is active in S iff (−i,k) is active in −S under μC; likewise the toggle
lands at −(i+c). Relabelling is a bijection of the slot space commuting with
the update by construction of t′. Verdicts are defined by exact/normalised
recurrence, which both maps preserve. ∎

On 2 kinds, ρ is the swap, and it acts on target maps by id ↦ id, swap ↦ swap,
const-0 ↔ const-1. `[measured]` **2916 constitutions → 757 orbits** (2 fixed
points, 53 orbits of size 2, 702 of size 4), and the census vector is
**constant on every orbit: 0 violations** in both resolutions — the reduction
is machine-certified, not merely argued. Full table (757 rows, with cycle
offset-sums, period spectra, transients and balance counts):
[`data/periodic_table8_parity.csv`](data/periodic_table8_parity.csv).

### 5.3 The census

**Aggregate, span ≤ 8, complete** `[measured]`

| verdict | parity | | OR | |
|---|---:|---:|---:|---:|
| EXTINCT | 266,574 | 0.19 % | 266,574 | 0.19 % |
| FIXED | 85,223,788 | 59.46 % | 85,330,564 | 59.54 % |
| **BALANCED** | **1,572,788** | **1.10 %** | **0** | **0 %** |
| CYCLE | 41,162,788 | 28.72 % | 42,363,956 | 29.56 % |
| **GLIDER** | **0** | — | **0** | — |
| GROWING | 15,101,294 | 10.54 % | 15,366,138 | 10.72 % |
| UNRESOLVED | **0** | — | **0** | — |

**By target-map block (parity, span ≤ 8)** `[measured]`

| block | extinct | fixed | balanced | cycle | glider | growing | periods |
|---|---:|---:|---:|---:|---:|---:|---|
| **id** (own-kind) | 0.42 % | 61.82 % | 0 % | 18.88 % | 0 | 18.89 % | {2,4,6,8} |
| **swap** (reciprocal) | 0.29 % | 57.98 % | 0 % | 38.36 % | 0 | 3.38 % | {2,4,6,8,12,16,18,30} |
| **const-0** | 0.02 % | 59.03 % | 2.19 % | 28.82 % | 0 | 9.94 % | {2,3,4,5,6,7,8,9,10,12,14,16,18} |
| **const-1** | identical to const-0 by symmetry | | | | | | |

Structural readings, all from the complete box:
* **balance is exactly the non-injective phenomenon** (0 vs 1.57 M);
* **reciprocal amendment maximises oscillation** (38 % cycles, the longest
  periods, and the least growth of any block — 3.38 %);
* **own-kind maximises growth** (18.9 %) — an anchor is a licence to grow
  one-sidedly forever;
* **cross-amendment maximises extinction only in the reciprocal/const sense of
  mutual repeal**; the totally-extinct universes are exactly the two orbits
  with both kinds (0,±1,0) and t injective — every seed dies.

**Behaviour classes of the 757 orbits** (has-balance / has-growth /
has-odd-period / has-extinction) `[measured]`

| signature | orbits | | signature | orbits |
|---|---:|---|---|---:|
| — / — / — / — | 565 | | bal / grow / — / — | 10 |
| — / grow / — / — | 100 | | bal / — / — / ext | 5 |
| — / — / — / ext | 50 | | — / grow / — / ext | 4 |
| bal / — / — / — | 16 | | bal / — / odd / — | 3 |
| — / — / odd / — | 2 | | bal / grow / odd / — | 1, — / — / odd / ext 1 |

### 5.4 The interesting residue

Five families are non-generic, and each is non-generic for an identifiable
structural reason:

1. **The 810 zero-sum constitutions** (S_Z = 0 for every reachable cycle):
   **no growth is possible**, 39.8 M runs, 0 violations — Corollary 4.3 made
   flesh. 217 of the 642 no-growth orbits are of this kind; the others are
   no-growth for guard reasons, not confinement reasons.
2. **Two totally extinct orbits** (4 constitutions): both kinds the rule
   (0,−1,0) — or its mirror (0,1,0) — with an **injective** target map, id or
   swap. Every one of the 49,152 seeds dies. Repeal at zero offset — self-repeal
   under id, mutual repeal under swap — is the field's only universal solvent;
   the *same* rule pair with a const target map is instead the balance champion.
3. **Three orbits with odd periods > 1**, all in const-target blocks:
   ((−1,1,1),(0,1,−1)) with periods {2,3,4,5,6,8,10,12} and
   ((0,−1,1),(0,1,−1)) with periods {2,3,4,5,6,7,8,9,10,12,14}. Multi-authorship
   plus parity is what breaks the 2-adic clock here — but see T6: with ≥ 3 kinds
   permutation constitutions do it too, so this is a two-kind artefact.
4. **The period-30 constitution** — the longest cycle in 143 M runs:
   ```
   PER-30   kind 0 = (-1, 1, 0) -> 1        RECIPROCAL (single-author!)
            kind 1 = ( 0,-1, 1) -> 0        S_Z = c_0 + c_1 = +1
   seed: kind 1@0, kind 0@2, kind 1@4, kind 0@5, kind 0@6   ->  CYCLE, p = 30
   ```
   30 = 2·3·5 with single-authorship intact: cross-amendment breaks the 2-adic
   clock *without* breaking linearity, by driving the occupancy oscillation.
5. **The 140 balance-admitting constitutions** and their attractor basins
   (§4.4). The champion — both kinds (0,−1,0) amending kind 0 — ends
   **49,024 of its 49,152 seeds** in a balanced state.

Other census records: longest transient **18** steps (four constitutions, all
cross-amendment: e.g. (−1,1,−1)→0 with (0,−1,1)→1); 60,140 runs land on a
non-power-of-2 period, spread over just 24 constitutions (7 orbits); no seed
anywhere in the box exhausts the 1024-step budget, and no seed anywhere in the
box is a glider.

---

## 6. The semantic lattice

### 6.1 The five axes

A semantics is a point of

| axis | values | what it decides |
|---|---|---|
| **GUARD** | occupancy (∃/∄) · quorum(m ⊆ {0,1,2}) · kind guards | when a law is active |
| **TARGET** | own-kind · permutation · functional t · multi-target · state-dependent (supersession, override) | whose kind an effect edits |
| **EFFECT** | toggle · enact-only · repeal-only · override (lex posterior) · supersede | what an effect does |
| **RESOLVE** | parity · OR · threshold | how co-arriving effects combine |
| **PERSIST** | keep (H3) · **sunset(τ)** | what happens to an untouched law |

`xnomos.py` implements (occ, functional, toggle, parity|OR, keep) and
(occ, own, supersede, parity|OR, keep). `xsem.py` adds the rest in one engine
and reproduces `xnomos` exactly on the overlap (`[measured]` 6,000 states,
0 mismatches).

### 6.2 Invariance table `[proved]` where marked

| theorem | GUARD | TARGET | EFFECT | RESOLVE | PERSIST |
|---|---|---|---|---|---|
| **Gridlock** | needs a vacancy clause | free | free | free | free |
| **Path-Sum Confinement** | free | needs H2 (fixed offset per kind) | free | free | **needs H3** |
| **Zero-Sum No-Go** | free | needs H2 | free | free | **needs H3** |
| **One-sided confinement** | free | needs H2 | free | free | **needs H3** |
| **Single-Author / parity ≡ OR** | free | **needs in-degree ≤ 1** | free | — | free |
| **Dead Letter** | free | free | **needs a strict resolution** | **needs a strict resolution** | free |
| **Balance Theorem 9** | free | **needs out-degree 1** | needs cancellation | needs parity | free |
| **Cryptic Unipotency** | free | needs S_Z ≠ 0 | needs linear effect | needs parity | needs H3 |
| **Anchor (permanence)** | free | **needs own-kind (H1)** | free | free | needs H3 |

The single most robust theorem is Gridlock; the single most fragile is the
Anchor. **Everything that confines rests on H3 and nothing else.**

### 6.3 Verdicts on the new semantics

**(a) Entrenchment clauses (a kind that cannot be repealed) — BARREN as
dynamics, ALIVE as a balance amplifier.** `[measured]` An immune kind multiplies
the balanced-code count by 13.6× (13,056 vs 960 in the span-≤3 two-kind box)
because absorbing a repeal is exactly a non-strict resolution. It adds no
motion: an immune kind is never toggled, so its support is constant, and
Theorem 10 pins any pattern containing one. *Verdict: a knob on Dead Letter,
not a new universe.*

**(b) Quorum guards — STRUCTURALLY INERT, CENSUS-CHANGING, with one live
corner.** `[proved]` Every confinement theorem above is guard-free, so
Path-Sum, Zero-Sum, one-sided confinement and the displacement law survive
verbatim. `[measured]` Gridlock survives iff the full neighbourhood count 2 is
**not** an allowed quorum. The corner worth a separate expedition is
**quorum = {2}**, where Gridlock *inverts*: solid code is fully active and the
vacuum is dead — a dual universe in which gridlock is life.

**(c) Supersession by date / override (lex posterior: the enacting law
displaces whatever stands at the target cell) — ALIVE but in the supersession
class.** `[measured]` 11,056 balanced codes in the span-≤3 box (non-strict:
overriding with what is already there changes nothing); breaks Single-Author;
but creation is still own-kind, so `[proved]` **ray confinement survives**
(supp_k ⊆ seed_k + ℕ·c_k) and with it linear growth and the displacement law.

**(d) Enact-only / repeal-only — BARREN dynamically, INSTRUCTIVE
taxonomically.** Monotone in each slot, so every orbit reaches a fixed point in
at most (number of slots) steps: no cycles, no gliders, nothing. But they
exhibit the second species of balance — **redundant** balance (the amendment
passes and changes nothing) as against the **cancelling** balance of parity.
`[measured]` 25,824 and 35,408 balanced codes in the span-≤3 box.

**(e) SUNSET BY DEFAULT — the live axis, and the answer to the field's
central question.** `[measured, complete]` Laws lapse after τ steps without
re-enactment. This is the only point of the lattice that breaks H3, and it is
the only point at which **free gliders exist on ℤ**. Complete two-kind box,
all 2916 constitutions × 48 seeds of span ≤ 3 = 139,968 codes per τ:

| τ | extinct | fixed | cycle | **glider** | growing | unresolved | glider periods | speeds |
|---|---:|---:|---:|---:|---:|---:|---|---|
| 1 | 82.68 % | 5.39 % | 0.36 % | **11.38 %** | 0.18 % | 0.01 % | {1,2} | 1, 1/2 |
| 2 | 78.24 % | 5.56 % | 0.35 % | **15.39 %** | 0.29 % | 0.17 % | {1,2,3,4} | 1, 2/3, 1/2, 1/3, 1/4 |
| 3 | 78.11 % | 5.56 % | 0.35 % | **15.48 %** | 0.30 % | 0.19 % | {1,2,3,4,6} | 1, 1/2, 1/3, 1/4, 1/6 |

Every glider certificate re-verified over three further full periods. The
non-trivial specimen — a genuine two-kind **caterpillar**, impossible under H3
by Anchor Corollary 3:

```
SUN-1   kind 0 = (0,-1, 1) -> 1     RECIPROCAL amendment, sunset tau = 2
        kind 1 = (0,-1, 1) -> 0     seed: a single kind-0 law
   .A...      A enacts B ahead of it;
   .AB..      B enacts A ahead of that;
   ..B..      the wake lapses two steps behind.
   ..BA.      period 4, displacement +2, speed 1/2.
   ...A.      Verified over 3 further periods.
```

`[measured]` 12,000 sunset gliders were tested against the Glider Skeleton
condition P ⊆ t(A\*) of Theorem 10: **0 violations**, even though the theorem's
proof (which uses H3) does not apply there.

**Verdict.** The reason law-packets cannot move on the infinite line is not the
guards, not the resolution, and not own-kind targeting. It is **permanence**:
H3, the axiom that a statute you do not amend is still there tomorrow. Repeal
that axiom and motion becomes generic — 11–15 % of the census. *Entrenchment is
a theorem of linear order (Anchor); circular codes revolve (X-C's rotors); and
codes that expire march.*

---

## 7. Verification battery

All in `theorems.py` (sections 1–7), `xsem.py`, `sunset.py`, `specimens.py`;
raw logs in `data/`. Every positive claim is re-checked through the independent
set-based reference engine `xlib.ref_step`, which shares no code with
`xnomos.step` (sets vs bitmasks, explicit multisets vs XOR accumulation).

| check | scope | result |
|---|---|---|
| reference engine ≡ `xnomos.step` | 1,600 trajectories × 4 semantics + 1,200 census cases | 0 divergences |
| C census engine ≡ Python classifier (same budget) | 4,000 random (constitution, seed, mode) | 0 verdict mismatches |
| Gridlock, solid blocks | 708,588 codes (complete two-kind box) | 0 active interiors |
| Gridlock on solid rings, 4 semantics | 16,000 pairs | 0 non-fixed |
| multiplicity > 1 ⟹ in-degree ≥ 2 | 60,000 random (constitution, state) | 0 violations |
| parity ≡ OR on injective targets | 209,952 codes (complete, span ≤ 4) | 0 divergences |
| Dead Letter under OR / super_or | 559,872 codes (complete) + 143,327,232 (census) | 0 balanced |
| Theorem 7 (non-injectivity) | 600,000 random codes, 1,168 balanced | 0 violations |
| **Theorem 9 (entrenchment)** | **28,672,000 codes, 207,379 balanced** | **0 violations** |
| Anchor holds in the own-kind block | 139,968 codes × 12 steps (complete) | 0 anchor deaths |
| **Path-Sum Confinement, 1-D** | **1,200,000 steps over 20,000 trajectories** | **0 escapes** |
| Path-Sum Confinement, 2-D | 160,000 steps over 4,000 trajectories | 0 escapes |
| Supersession ray confinement | 1,000,000 steps over 20,000 trajectories | 0 escapes |
| **Zero-Sum No-Go** | **39,813,120 runs (complete) + 4,000 × 200 steps** | **0 growth, 0 escapes** |
| Cryptic periods are 2-adic | 62,784 cryptic codes (complete two-kind box) | all powers of 2 |
| frozen-occupancy odd period ⟹ zero-sum cycle | 40,000 runs, 20 non-2-power cycles | 0 violations |
| "never-targeted kind has frozen support" | 3,946,042 (kind, step) checks | 0 violations |
| symmetry quotient soundness | 2916 → 757 orbits, both resolutions | 0 non-constant orbits |
| sunset glider certificates | every glider re-run 3 further periods | all verified |
| glider skeleton on sunset gliders | 12,000 gliders | 0 violations |

**Complete enumerations vs samples.** Complete: the two-kind box at span ≤ 6
(8,957,952 runs × 2 resolutions) and span ≤ 8 (143,327,232 × 2); the solid-code
Gridlock sweep; the injective/non-injective divergence sweep at span ≤ 4; the
Dead Letter sweep at span ≤ 4; the sunset box at span ≤ 3 × three τ; the cryptic
sweep at span ≤ 4. Sampled (and labelled as such in the text): all statements
about ≥ 3-kind constitutions, the multi-target searches, the random-trajectory
confinement checks, and the odd-period probe of §T6.

---

## 8. Pre-registration scorecard

| # | prediction | outcome |
|---|---|---|
| P1 Gridlock survives verbatim | **HELD** |
| P1 Single-Author fails, survives at in-degree ≤ 1 | **HELD** — sharpened to an iff |
| P1 Dead Letter fails under parity, survives OR | **HELD** — sharpened to the strictness criterion |
| P1 Anchor fails, minimal counterexample ≤ 3 laws | **HELD, and beaten**: **one** placed law |
| P1 Anchor survives as a path-sum generalisation | **HELD** (Theorem 4) |
| P1 ray confinement fails, survives as a bounded bundle | **HELD** (Corollary 4.2) |
| P1 powers of 2 fail in 1-D cross-amendment | **HELD** — spectrum up to 30 |
| P2.1 minimum balance = 2 laws, 2 kinds | **HELD**, both tight (two laws in *one cell*) |
| P2.2 balance already in a 2-kind constitution | **HELD** |
| P2.3 the coordinator's in-degree duality is true | **REFUTED** (`BAL-3`); the correct form is dynamic |
| P2.4 balance < 1 % of the census | **NEAR MISS**: 1.10 % |
| P2.5 balance under `super`, not `super_or`; multi-target yes | **HELD** on all three |
| P2.6 balanced codes of unbounded size | **HELD** (disjoint unions; and the cohort family) |
| P2.7 balance is not an attractor | **REFUTED**: 70.1 % of balanced verdicts are *reached* |
| P2.8 cryptic codes exist in own-kind at period 2; 2-adic periods | **HELD**, with the zero-sum exception found |
| P3.1 census dominated by FIXED > 50 %, GROWING second | **HALF**: FIXED 59.5 % held; the order is wrong (CYCLE 28.7 % beats GROWING 10.5 %) |
| P3.2 symmetry group ℤ₂ × ℤ₂, ≈ 4× reduction | **HELD**: 2916 → 757 |
| P3.3 own-kind {2,4}; swap adds 6,8,12; const adds odd from 3 | **HALF-REFUTED**: own-kind reaches 6 and 8 |
| P3.4 zero gliders in the whole two-kind box | **HELD**: 0 in 286,654,464 runs |
| P3.5 extinction commoner in const blocks | **REFUTED**: const 0.02 %, own-kind 0.42 % |
| P4.1 Gridlock the most robust; vacancy clause is the hypothesis | **HELD** |
| P4.2 entrenchment barren | **HALF-HELD**: barren dynamically, a 13× balance amplifier |
| P4.3 sunset is alive and the most promising axis | **HELD, emphatically**: free gliders on ℤ |
| P4.4 quorum guards structurally inert | **HELD**, with the quorum-{2} dual universe as a bonus |
| P4.5 enact/repeal-only barren; second species of balance | **HELD** |
| P5 the true generalisation is about cycle offset-sums | **HELD** (Theorem 4, Corollaries 4.2–4.4, Theorem 6) |

Score: 19 held, 3 half, 4 refuted. The four refutations (P2.3, P2.7, P3.3,
P3.5) are the most informative results in the report.

---

## 9. Verdict and open questions

**What is proved.** Gridlock (verbatim, whole lattice). The Single-Author
criterion (in-degree ≤ 1, iff). The Dead Letter criterion (strict resolutions,
iff-modulo-realisability). Path-Sum Confinement and its four corollaries —
linear growth in every dimension, the ray-bundle structure, the Zero-Sum No-Go,
and the displacement law. One-sided confinement. The supersession ray lemma.
Cryptic Unipotency. The Balance Theorem: cohort structure, minimality,
Balance ⟹ Entrenchment, Motion ⟹ universal amendability, and the duality
A ⊆ t(A).

**What is measured.** The complete two-kind periodic table (286 M certified
runs, both resolutions, 0 gliders, 0 unresolved), the exact balance counts and
their transfer-matrix closed form, the balance attractor fraction, the complete
sunset census, the cryptic census, and every sharpness witness.

**What was refuted.** The coordinator's literal duality; the pre-registered
claim that balance is measure-zero and non-attracting; and, in the own-kind
sector, the census-level regularity "every W=1 cycle has period 2 or 4".

**Open questions, sharpest first.**

1. **Name the second obstruction.** Theorem 10 says a glider's alphabet must
   carry a permutation sub-constitution; Corollary 4.4 says its velocity is a
   positive multiple of the cycle offset-sum, which must be nonzero. Both
   conditions are easy to satisfy — and yet the complete two-kind box
   (286,654,464 runs) contains **zero** gliders. **A third obstruction exists
   in 1-D cross-amendment. What is it?** The remaining gap in the proved
   picture is exactly *mixed-sign offsets with S_Z ≠ 0* (Theorem 5 kills the
   same-sign case). A monovariant for that case would close the cross-amendment
   glider question. `[proposal]`
2. **What controls the maximal period?** Own-kind rings give orders of 𝔽₂
   polynomials (X-C's 341 at m = 22). Cross-amendment on ℤ gives 30 = 2·3·5
   from a **single-author** reciprocal constitution — so the 2-adic clock breaks
   through occupancy oscillation, not through nonlinearity. Is there a
   monodromy-of-unipotents formula for the ℤ case? `[proposal]`
3. **Characterise the basin of balance.** 70 % of balanced verdicts are
   reached, not seeded. Which codes flow to a cohort configuration? Balance is
   an attractor of a *conservative-looking* dynamics; a Lyapunov function for
   it would be the first genuine monovariant of the cross-amendment sector.
4. **The quorum-{2} dual universe**, where Gridlock inverts: solid code is
   alive, vacuum is dead. Nothing in the field has been run there.
5. **Sunset with τ → ∞** interpolates between the glider-rich sunset universe
   and the glider-free permanent one. Where is the transition, and is it sharp?
   `[measured]` τ = 1 → 11.38 %, τ = 2 → 15.39 %, τ = 3 → 15.48 % gliders:
   the fraction *rises then plateaus*, which is not what a naive interpolation
   predicts.

> **The law of the cross-amendment sector.** Every kind's fate is decided by
> the cycle it falls into and by the sum of the offsets around that cycle. If
> the sum vanishes the code is imprisoned; if it does not, the code may travel,
> but only along that sum. And in time: a code stands still and dead when every
> provision is blocked, stands still and alive when every amendment is
> co-signed an even number of times, and moves only when nothing in it is
> entrenched.

---

## 9b. Specimen cards (paste-ready)

Machine-readable in [`data/specimens.json`](data/specimens.json); the
constructor calls below are literal `xnomos.py` API.

```python
import sys; sys.path.insert(0, "..")          # xnomos.py lives one level up
from xnomos import Const, state_of, classify, spacetime

# BAL-1  "the co-signed repeal" -- the minimal balanced constitution.
#        Two laws, two kinds, ONE cell.  Both active forever; both repeal the
#        absent kind-0 law at cell -1; the repeals cancel.  Under 'or' the
#        repeal passes and a law appears at cell -1.
C = Const([(0,-1,-1), (0,-1,-1)], targets=[0, 0])
S = state_of([(0,0), (0,1)])                       # BALANCED, 2 active laws

# COH-6  "the six-fold co-signature" -- balance with six distinct kinds.
#        Six laws co-target one slot; even, so they annihilate.  Delete any
#        one and the amendment passes.  Generalises to any even 2m.
C = Const([(0,-1,1)]*3 + [(0,1,-1)]*3 + [(0,1,0)], targets=[6]*7)
S = state_of([(0,0),(0,1),(0,2), (2,3),(2,4),(2,5)])   # BALANCED, 6 active

# CRY-1  "the zero-sum cryptic clock" -- constant occupancy, period 3.
#        Amendment 3-cycle 0->2->1->0 with offsets (+1,0,-1), sum 0: the one
#        way to beat the 2-adic clock while frozen from outside.
C = Const([(0,-1,1), (0,1,-1), (-1,1,0)], targets=[2, 0, 1])
S = state_of([(-2,2), (2,0), (2,2), (3,0), (3,1)])     # CYCLE, period 3

# PER-30 "the long parliament" -- the longest cycle in 143M runs, and it is
#        SINGLE-AUTHOR (reciprocal amendment, parity == OR here).
C = Const([(-1,1,0), (0,-1,1)], targets=[1, 0])
S = state_of([(0,1), (2,0), (4,1), (5,0), (6,0)])      # CYCLE, period 30

# ANC-1  "the self-repealing seed" -- the Anchor Theorem dies from ONE law.
C = Const([(-1,1,-1), (0,1,1)], targets=[1, 0])
S = state_of([(0,1)])          # kind 1 legislates kind 0, kind 0 repeals it

# SUN-1  "the sunset caterpillar" -- a FREE GLIDER on Z.  Reciprocal
#        amendment under sunset tau = 2, from a SINGLE seed law:
#        period 4, displacement +2, speed 1/2.
from xsem import Sem, sunset_step
C   = Const([(0,-1,1), (0,-1,1)], targets=[1, 0])
sem = Sem(sunset=2)
A   = {(0, 0): 2}                       # one kind-0 law, remaining life 2
#   t=0  [((0,0),2)]                     .A...
#   t=1  [((0,0),1), ((1,1),2)]          .AB..
#   t=2  [((1,1),2)]                     ..B..
#   t=3  [((1,1),1), ((2,0),2)]          ..BA.
#   t=4  [((2,0),2)]  = t=0 shifted +2   ...A.
```

All six were re-run from these exact lines and reproduce the stated verdicts.

---

## 10. Reproduction

```sh
cd xtheory
sh run_all.sh                 # everything below, ~25 min on one core

# or piecemeal:
python3 ../xnomos.py          # shared-engine self-tests (7/7)
python3 xlib.py               # independent reference engine, duel smoke test
clang -O2 -o census2 census2.c
python3 validate_c.py 4000    # C engine vs Python classifier: 0 mismatches
./census2 6 0 > data/census_parity.csv        # complete span<=6 box, parity
./census2 6 1 > data/census_or.csv            #                       OR
# span<=8 needs the wide build (see run_all.sh): ./census2big 8 0|1
python3 analyze.py 8_parity   # aggregate census + period spectra
python3 periodic_table.py 8_parity   # 757-orbit table + Theorem A / Zero-Sum tests
python3 theorems.py           # the full verification battery (sections 1-7)
python3 specimens.py          # the certified specimen gallery
python3 sunset.py             # the sunset census and its gliders
```

Files: `xlib.py` (reference engine + amendment-graph predicates) ·
`xsem.py` (the semantic lattice engine) · `census2.c` (the census engine) ·
`validate_c.py` · `analyze.py` · `periodic_table.py` · `theorems.py` ·
`specimens.py` · `sunset.py` · `PREREG.md` · `data/` (censuses, logs,
`specimens.json`, `periodic_table8_parity.csv`).
