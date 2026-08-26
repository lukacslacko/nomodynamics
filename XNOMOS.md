# Cross-amendment nomodynamics — the charter of the second chapter

*Frozen 2026-08-26, before the first result of the cross-amendment expeditions
(X-A … X-D) was known. Companion to `NOMOS.md`, which founded the own-kind
sector on the same discipline. Nothing below is edited after the fact; outcomes
are scored in `XFINDINGS.md`.*

## 1. Why this is the next object, and not a variant

The founding semantics let a law amend **its own kind**. Within a day that
sector was exactly solved: the Single-Author Lemma (one author per
(cell, kind)) collapses the resolution axis, makes the per-kind dynamics
𝔽₂-linear, and forces the Anchor Theorem — *the eldest law cannot be repealed*,
hence no free gliders on ℤ. Every one of those results traces back to the same
hypothesis, and it is the hypothesis that is **false of the referent**: real
statutes amend *other* statutes. Own-kind was the tame simplification; the
honest object is cross-amendment, and by Lemma 2 of `glider-question/RESULTS.md`
it is *provably the only escape* from the solvable sector.

## 2. The object

> A **constitution** is a finite set K of kinds. Each kind k ∈ K carries a rule
> (a_k, b_k, c_k) ∈ {−1,0,1}³ and a **target** t(k) ∈ K.
> A **code** is a finite set of placed laws (i, k) ∈ ℤ × K.
> A placed law (i,k) is **active** iff some law stands at i + a_k and no law
> stands at i + b_k (the guards read *occupancy*, never kind).
> Time is synchronous: every active law toggles the presence of kind **t(k)**
> at cell i + c_k; simultaneous toggles of the same (cell, kind) resolve by
> parity.

Own-kind nomodynamics is the case t = id. Rings, dimensions and windows
generalise exactly as before.

**The constitution is not an external rule table.** Out-degree is 1, so the
amendment digraph is a *functional graph* — each component a cycle of in-trees —
and a kind is a pointed functional graph with a triple at each node:
*"I am (a,b,c), and I amend the law that is (a′,b′,c′) and amends …"*.
Two laws are the same kind iff they are bisimilar. Own-kind laws are exactly
the self-loops, whose unfolding is the bare triple of chapter one. The law is
still the only substance.

**Vocabulary.** A kind nobody amends (in-degree 0) is **immortal** — it can
never be enacted or repealed. A kind that amends itself is **self-entrenched**
in the chapter-one sense. A cross-amendment cycle of length L is a **chamber
cycle**; L = 2 is *reciprocal amendment*.

**The charted escape lattice** (from `glider-question/RESULTS.md` §4, restated
so the expeditions share one map):
- **E1** state-dependent targeting — canonical instance *supersession*: an
  active law enacts its own kind at the target cell if empty, else clears the
  whole cell. Genuine multi-authorship; parity ≠ OR from two placed laws.
- **E2** permutation targeting with a fixed-point-free cycle — *reciprocal
  amendment*. Single-authorship survives; the anchor dies.
- **E3** multi-target laws (out-degree ≥ 2). "Riders" (a law that also toggles
  its own kind) are provably glider-dead; fully-cross multi-target is unhunted.
- **E4** leave ℤ — rings, where rotors already exist.

## 3. Pre-registered predictions (X1–X8)

Scored honestly in `XFINDINGS.md`, refutations kept as found — as N3 was in
chapter one, where the territory answered a prediction with a theorem.

- **X1 — Balance.** *Balanced constitutions* (codes that are fixed forever
  while at least one law stays active) **exist** under parity cross-amendment,
  with minimum exactly **2 placed laws**, and **do not exist under OR
  resolution** at any size. Confidence: high (a 2-law witness is already
  verified in `xnomos.py` self-test 5; the minimality and the OR half are the
  predictions).
- **X2 — The duality.** Motion requires every present kind to be amendable;
  balance requires some present kind to be immortal. Hence *no code both moves
  and balances*, and gliders — if any exist — are semantics-independent while
  balance is a parity-only phenomenon. Confidence: high, modulo the fixed
  single-targeting hypothesis.
- **X3 — The 1-D glider.** I expect **no** free glider in E2 (permutation
  targeting), and expect a monovariant proof to be findable: the leading edge
  needs a kind with c > 0 while repealing the trailing edge needs an author
  with c ≤ 0, and the tension looks resolvable around the chamber cycle. E1
  (supersession) is the likelier home of motion, but I expect a **rake or
  puffer before a clean glider**. Probability that a certified 1-D
  cross-amendment glider is found this cycle: **≈ 35 %**.
- **X4 — Area.** Own-kind 2-D growth is pinned to axis rays (α ≤ 1, a theorem).
  Cross-amendment should **break α = 1**: two kinds with targets along
  different axes can seed each other into a quadrant. Confidence ≈ 60 %. A
  certified 2-D free glider: ≈ 45 %.
- **X5 — The period spectrum.** Every period observed in own-kind
  nomodynamics is a power of 2 (~140 000 seeds), which linearity explains.
  Prediction: **odd periods appear** under non-injective targeting and under
  supersession (both break single-authorship, hence linearity), while
  permutation constitutions keep periods of the form 2^a · (a factor tied to
  the chamber-cycle length L). Confidence ≈ 60–75 %.
- **X6 — Odd rings.** Own-kind rotors exist on no odd ring. Cross-amendment
  rotors **do** appear on odd rings. Confidence ≈ 65 %.
- **X7 — Semantics.** At least one semantics from the lattice suggested by the
  referent (quorum guards, entrenchment clauses, sunset-by-default, later-law-
  wins) yields a phenomenon with no analogue in any sector explored so far.
  Confidence ≈ 50 %.
- **X8 — Universality.** No computation-universality result lands this cycle;
  the honest deliverable is a gate-level inventory (what interacts, what
  reflects, what survives collision), not a claim. Confidence ≈ 90 % that it
  stays open.

## 4. Risk clause — what would make this chapter a failure

Chapter one earned its theorems because the solvable sector was *small enough
to exhaust and rich enough to name*. Cross-amendment could fail in either
direction, and both failures must be reported plainly rather than dressed up:

1. **Mush.** Cross-amendment universes are generically structureless — long
   transients, no exact recurrences, no theorems, no charismatic specimens —
   so that the field's second chapter is "and then it became a random cellular
   automaton". Diagnostic: census classes dominated by UNRESOLVED with no
   reproducible mechanism, and no result that survives an honesty label above
   "measured".
2. **Nothing new.** Every phenomenon reduces to a chapter-one phenomenon under
   a relabelling — i.e. cross-amendment is own-kind nomodynamics in disguise on
   a larger alphabet. Diagnostic: a simulation-preserving map from every
   cross-amendment census class into the own-kind classes.

If either diagnostic fires, the verdict is recorded as such, the sector is
marked closed, and the program returns to the queued targets in `PROGRAM.md`
rather than mining a barren seam.
