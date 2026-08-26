# Chapter three — citation: laws that read other laws by name

*Frozen 2026-08-26, before the chapter-three expeditions (Y-A … Y-D) ran.
Companion to `NOMOS.md` (chapter one) and `XNOMOS.md` (chapter two), written on
the same discipline: definition and predictions first, outcomes scored after,
refutations kept as found.*

## 1. The vacancy, again

Chapter one let a law amend **its own kind**. Chapter two let it amend
**another kind**, and that turned out to be the wrong axis for motion — what
buys motion is *out-degree*, and what forbids it on the line is *permanence*.
Both chapters share an assumption that nobody questioned because it sits in the
guard rather than in the effect:

> **A law can see only whether something stands nearby — never what it is.**

The founding guard reads *occupancy*: "while some law stands at my precedent and
none stands at my exception." Every theorem of both chapters was proved with
guards of that shape, and the semantic-lattice sweep of chapter two found that
guards are almost inert: every confinement theorem is guard-free.

But the referent has names. A real statute does not say "while something is in
force nearby"; it says **"while section 5 is in force and section 9 has been
repealed."** Citation — reference to another provision *by identity* — is the
most ordinary feature of written law, and it is missing from the object. That is
the vacancy of chapter three.

## 2. The object

> A **constitution** is a finite kind set K. Each kind k carries offsets
> (a_k, b_k, c_k), a **target set** T_k ⊆ K, and a pair of **citations**
> (g_k, h_k) ∈ (K ∪ {any})².
> A placed law (i,k) is **active** iff a law of kind **g_k** stands at i + a_k
> and no law of kind **h_k** stands at i + b_k.
> Time is synchronous; every active law toggles each kind of T_k at i + c_k;
> simultaneous toggles resolve by parity (or by OR).

Setting g_k = h_k = *any* recovers chapters one and two exactly, so the founding
object is the anonymous corner of this one. Reading the guard aloud: *"while
section g stands at my precedent and section h is absent at my exception, amend
T at my target."*

Implemented in `xnomos.py` via `Const(..., guards=[(g,h), …])`; `None` means
*any*, and the 42-check battery passes unchanged, so the extension is
conservative.

## 3. What is already known (verified before freezing this document)

**Gridlock dies.** In a solid block of ten kind-0 laws, occupancy guards leave
exactly **one** law active — chapter one's theorem, *all dynamics is surface
dynamics*. Give the same rules the citation guard "no **kind-1** law stands to
my right" and **all ten** are active: the block fills in and grows. The interior
of a written code can now act.

That is the whole point of the chapter, and it is why the chapter exists: of the
four founding theorems, Gridlock was the only one that survived cross-amendment,
supersession, quorum guards, entrenchment and sunset-by-default untouched. Its
single hypothesis was that the guard contains a *vacancy* clause about
occupancy. Name a kind and the hypothesis fails.

## 4. Pre-registered predictions (Y1–Y8)

- **Y1 — the plenum still freezes.** Gridlock dies in its stated form, but a
  *saturated* code — every kind present at every cell of a region — is still
  frozen there, because every vacancy clause, whatever it names, fails. Total
  law is still total stasis; what changed is what "total" means. Confidence:
  high.
- **Y2 — the Out-Degree Law survives citation verbatim.** Its proof is
  guard-free (guards only thin the actor set), so citation should buy no motion
  whatsoever: gliders still require out-degree ≥ 2. Confidence ≈ 0.85. If this
  fails, the tropical monovariant has a hole and chapter two needs re-auditing.
- **Y3 — citation is the computational substrate.** "Kind A present here, kind B
  absent there" is an AND-NOT over kind-fields at fixed offsets — the classical
  ingredient of a universal gate set. Prediction: the first credible
  universality construction in nomodynamics lives in the citation sector rather
  than in the ballistic (glider-collision) style of Life. Probability that a
  construction is *completed* this cycle: ≈ 0.35; that a gate-level inventory
  with working AND, NOT and fan-out is exhibited: ≈ 0.7.
- **Y4 — growth stays linear.** With n kinds the population is bounded by
  n·(span), and the span grows by at most one cell per step, so card grows at
  most linearly in 1-D however clever the citations. No exponential blow-up.
  Confidence: high (this is close to a proof and should become one).
- **Y5 — a replicator exists.** Some code in the citation or multi-target sector
  produces a disjoint copy of itself. Given von Neumann's constructor is one of
  the three fragments this field was derived from, this is the thematically
  obligatory object. Confidence ≈ 0.4 this cycle.
- **Y6 — the four-law reset is not a coincidence.** The Jubilee Code (own-kind,
  2-D, three kinds) and the Odometer (cross-amendment, 2-D, two kinds) both
  return to **exactly four laws** at every t = 2^k. Prediction: both are
  instances of one binary-counter normal form, and the 4 is forced by it.
  Confidence ≈ 0.5.
- **Y7 — light-cone-admissible odd-ring rotors exist.** X-C left this open
  within its own sector, but TANDEM-1 turns by one cell per step on every ring
  m ≥ 3, which is inside the light cone. Prediction: verifying it at odd m
  settles the question affirmatively, and genuine ring transport is exactly the
  wrapped cross-amendment glider. Confidence: high — this is a check, not a
  hunt.
- **Y8 — the impermanence sector is rich.** Sunset-by-default (a law lapses
  unless re-enacted) already admits gliders on ℤ under own-kind targeting. Its
  full fauna is unexplored; prediction: it carries its own charismatic
  specimens, and *sunset + citation* is the easiest place to build a machine.
  Confidence ≈ 0.6.

## 5. Risk clause

The chapter fails if citation is either **inert** (every phenomenon is a
relabelling of a chapter-two phenomenon on a larger alphabet — diagnosed by a
simulation-preserving map) or **structureless** (censuses dominated by
unresolved trajectories with no reproducible mechanism and no theorem above the
"measured" honesty tier). Gridlock's death is not by itself a result; it is the
door. If nothing charismatic and nothing provable lies behind it, the verdict is
recorded as such and the sector is closed.
