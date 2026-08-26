# Cross-amendment nomodynamics — findings

*Scored against `XNOMOS.md`, which was frozen before any of this was known.
Refutations are kept as found. Expedition reports: `xamend1d/RESULTS.md`,
`xamend2d/RESULTS.md`, `xrings/RESULTS.md`, `xtheory/RESULTS.md`.*

## 1. The headline: motion is bought with out-degree

Chapter one ended at the Anchor Theorem — *the eldest law cannot be repealed*,
hence no free glider on ℤ — and named cross-amendment as the door out. The door
opens, but not where the escape lattice said it would.

> **The Out-Degree Law** (X-A, Corollary 2.4). If, restricted to the kinds a
> pattern actually uses, every law amends **at most one** kind, there is no free
> glider — for any offsets, any window, any dimension, parity or OR.

This single statement contains the Anchor Theorem (own-kind is the self-loop
case), reciprocal amendment, every permutation constitution of every cycle
length, and every non-permutation single-target constitution. Cross-kind
targeting was never the obstruction: **out-degree** was.

> **The Supersession No-Go** (X-A, Theorem 3). State-dependent targeting of the
> supersession kind — *enact your own kind on empty ground, clear the whole cell
> if occupied* — admits no free glider either, in any dimension. Its creation
> channel is own-kind, and that suffices: every present kind must push in the
> direction of travel, and then nothing can clear the rearmost cell.

> **The threshold is exact.** With out-degree 2 gliders exist, and they are
> tiny. The proof route is a tropical (min-plus) monovariant
> Ψ = min_t(α_t + w_t) with w_k − c_k ≤ w_{t(k)}, refined by a tight-cycle
> argument; it also yields a **Tropical Speed Law**: for a glider of period p
> and displacement d, p·min(λ_min,0) ≤ d ≤ p·max(λ_max,0), where λ are the
> extreme cycle means of the amendment digraph.

**The institutional reading.** A law that amends a single provision — even
somebody else's — can never move. Motion in a statute book requires laws that
amend *several* provisions at once. Entrenchment, in chapter one a consequence
of linear order, is now a consequence of legislative *narrowness*.

**A predecessor claim was refuted.** `glider-question/RESULTS.md` §4 recorded E3
"riders" as *provably* glider-dead. The error is named precisely in
`xamend1d/RESULTS.md` §4.1: "each law toggles its own kind among its targets" is
not the same as "each kind is toggled only by its own laws". The record stands
as written and is corrected here.

## 2. The first free gliders (all re-verified by the coordinator)

Verified independently with `xnomos.verify_glider` over three full periods, and
in the battery (`python3 verify.py`):

| name | constitution | seed | p | d |
|---|---|---|---|---|
| **SOLO** | 0:(0,1,0)→{1,2}, 1:(0,1,1)→{0}, 2:(0,1,0)→{0} | one law, kind 0 at cell 1 | 2 | +1 |
| **TANDEM-1** | 0:(0,−1,1)→{0,1}, 1:(0,−1,0)→{0,1} | kinds 0 and 1 in the single cell 1 | 1 | +1 |
| **TRIPTYCH** | 0:(0,1,0), 1:(0,−1,1), 2:(0,1,−1), all →{0,1,2} | all three kinds at cells 1, 2, 4 | 1 | +1 |

* **SOLO** is the smallest object in the field that moves: *one placed law,
  travelling forever at speed ½.*
* **TANDEM-1** is the minimal period-1 glider — two laws in a **single cell**,
  moving at speed 1, the fastest a window-1 packet can go. It lifts to ℤ² at
  **any** velocity, knight moves included (own-kind 2-D motion is pinned to
  axis rays by ray confinement), and it rotates on **every** ring m ≥ 3
  (own-kind rotors need even m ≥ 6). Coordinator-verified for velocities
  (1,0), (1,1), (0,1), (−1,1), (2,1) and for m = 3…12.
* **TRIPTYCH** moves under parity and does **not** under OR: with author
  multiplicity 2, the resolution convention — vacuous in all of chapter one —
  decides whether a law-packet moves at all.

## 3. Balanced constitutions (coordinator, then X-D)

The own-kind **Dead Letter Theorem** says stability is always gridlock: a code
is fixed iff every law in it is blocked. Under cross-amendment it fails.

> **Balance.** Under parity, two active laws whose enactments cancel leave the
> code *fixed forever while remaining alive*. Minimal witness, 2 placed laws:
> kinds 0:(0,1,1)→2, 1:(0,−1,−1)→2, 2:(0,1,0)→2 with kind 0 at cell 0 and kind 1
> at cell 2. Both laws are active at every step; their enactments of kind 2 at
> cell 1 annihilate. Under **OR** the same seed ignites, and Dead Letter
> survives verbatim: balance is a parity-only phenomenon.

*A constitution can be perpetually active and perfectly unchanging — but only if
contradictory simultaneous amendments cancel rather than both taking effect.*

## 4. Scorecard against the frozen predictions

- **X1 (balance exists, minimum 2 laws, none under OR)** — **HELD** for the
  witness and the OR half (verified); the minimality claim is X-D's.
- **X2 (the duality: motion needs every kind amendable, balance needs an
  immortal kind)** — **superseded**. The true dichotomy is out-degree, not
  amendability: TANDEM-1's kinds are mutually amendable *and* multi-target. What
  survives is the balance half.
- **X3 (no glider in E2; supersession the likelier home of motion; a rake before
  a clean glider; ≈35 % that a certified 1-D glider appears)** — **half right,
  and instructively so**. The E2 no-go held *and* was proved by exactly the
  monovariant sketched in the charter. The guess about *where* motion lives was
  wrong in both halves: supersession is provably dead, and motion lives in the
  multi-target sector I did not name. A glider was found — a period-1 one with
  two laws in one cell.
- **X4–X8** — pending the other expeditions.

*The pattern worth keeping: the structural intuition (a tropical monovariant
kills single-target motion) was sound, while the taxonomic guess (which named
sector would harbour the specimen) was not. The charter's own escape lattice
mislabelled the live sector as dead — a chapter-one error found by chapter two.*
