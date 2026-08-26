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
* **TRIPTYCH** moves under parity and does **not** under OR — under OR the same
  seed stops travelling and detonates into a two-sided sparse lattice growing by
  3 laws per step (verified to t = 500, 1 503 laws). With author multiplicity 2,
  the resolution convention — vacuous throughout chapter one — decides whether a
  law-packet travels or explodes.

## 2b. Balanced constitutions (coordinator, then X-D)

The own-kind **Dead Letter Theorem** says stability is always gridlock: a code
is fixed iff every law in it is blocked. Under cross-amendment it fails.

> **Balance.** Under parity, two active laws whose enactments cancel leave the
> code *fixed forever while remaining alive*. Minimal witness, 2 placed laws:
> kinds 0:(0,1,1)→2, 1:(0,−1,−1)→2, 2:(0,1,0)→2 with kind 0 at cell 0 and kind 1
> at cell 2. Both laws are active at every step; their enactments of kind 2 at
> cell 1 annihilate. Under **OR** the enactment passes at t = 1 — and the new
> provision, standing between them, blocks both of its own authors: the code
> becomes a genuine dead letter (fixed, zero active laws). Dead Letter survives
> OR verbatim; balance is a parity-only phenomenon.

*A constitution can be perpetually active and perfectly unchanging — but only if
contradictory simultaneous amendments cancel rather than both taking effect.*

## 3. Two dimensions: the plane fills, and the degrees govern everything

Expedition X-B (`xamend2d/RESULTS.md`; 199.5M certified classifications,
31/31 battery on the independent engine). Every headline below was re-verified
by the coordinator on `xnomos.py`.

**Growth (prediction X4, settled).** Own-kind 2-D growth is pinned to axis rays,
α ≤ 1 — a chapter-one theorem. The generalisation is exact:

> **Out-degree 1 ⟹ |S_t| ≤ |S₀|(t+1), hence α ≤ 1 in every dimension**
> (parity, OR, supersession alike). **Out-degree ≥ 2 ⟹ α = 2 is attainable,
> with bounding-box fill → 1.**

The witness is one law. **LAND GRANT** — kinds `A = (O,NE,NE) → {A,B,C}`,
`B = (O,E,E) → {B}`, `C = (O,N,N) → {C}`, seeded with a single `A` — has
`|S_t| = (t+1)²` **exactly** (verified t ≤ 8, support `{(0,0)} ∪ [1,t]²`): a
solid growing square. *The plane fills.* Chapter one's ray confinement was not a
fact about two dimensions; it was a fact about narrow laws.

**Guns and rakes exist — and they run on ℤ.** The ingredient X-A's travelling
packets were missing is not a second dimension but a kind of **in-degree 0**: a
provision nobody can amend, which therefore stands forever and pumps. On the
line, `A = (0,1,0) → {A,B}`, `B = (0,1,1) → {A,B}`, `C = (0,1,0) → {A,B}`
seeded with a single immortal `C` emits a periodic stream of two-law shots
forever, `|S_t| = 2⌊t/2⌋+3` (verified). An entrenched clause is a *gun*.

**The Odometer.** Three laws, two kinds: `A = (O,E,W) → {B}`,
`B = (N,NW,SE) → {A,B}`. Its population returns to **exactly four laws at every
t = 2^k** (14/14 verified, t < 2^15), crests at 2^k−1 (6, 9, 12, 18, 21, 36,
39, 72, 75, …, doubling every second power), and its reach grows like
≈ 0.20 (log₂ t)² out to t = 2²⁰ — bounded population, unbounded reach, hence
aperiodic. It is the second binary counter in the field and the slowest clock
in it (the Jubilee's reach goes like √t). *Two machines found in different
sectors by different methods both quiesce to exactly four laws at every power of
two* [interpretation: unexplained, and the most suggestive coincidence on the
board].

**Balance is governed by in-degree, not out-degree.** X-B's own prediction that
balance needs out-degree ≥ 2 was refuted and the record kept:

> Balance requires **parity resolution and in-degree ≥ 2** — a provision with
> two authors whose enactments cancel. Minimum two placed laws; 0 balanced codes
> in 81.4M OR runs.

Balanced codes can be large and fully alive: **PERPETUAL SESSION** — twenty
copies each of `A = (O,E,O) → {A}` and `B = (O,E,O) → {A}` stacked in a column —
is fixed forever with **all forty laws active at every step** (verified). A
parliament in permanent session that never changes a word.

**Collision algebra.** Head-on writs obey a parity rule: **even gap ⟹ mutual
transparency** (both packets pass through and continue), **odd gap ⟹ a frozen
four-law arrest** (verified at gaps 6–9). A dead letter is a wall.

**Also new**: a card-50 diagonal spaceship; a **one-law** 2-D glider (period 4,
diagonal); subluminal parity gliders down to speed **1/6** (verified); four
gliders with **no null cycle**, the first sighting of the no-go theorem's other
escape hatch; and — inside *own-kind* 2-D once diagonal offsets are allowed — a
**period-3** oscillator, which kills the 2-adic period conjecture in its own
home sector.

### The organizing principle

Chapter one's phenomena were governed by the *order* of ℤ (the eldest law).
Chapter two's are governed by the **degree sequence of the amendment digraph**:

| structure | consequence |
|---|---|
| out-degree ≤ 1 everywhere | nothing moves (Out-Degree Law); growth α ≤ 1 |
| out-degree ≥ 2 | gliders exist; α = 2 attainable — the plane fills |
| in-degree ≥ 2, parity | balanced constitutions exist (and can be fully active) |
| in-degree ≥ 2, OR | nothing: Dead Letter survives verbatim |
| in-degree 0 (immortal kind) | a pump — guns and rakes, on ℤ as well as ℤ² |

*Who amends whom, counted, decides what the statute book can do.*

## 4. The structure theory, and the second escape from the Anchor

Expedition X-D (`xtheory/RESULTS.md`; 42/42 battery on an independent set-based
engine sharing no code with `xnomos`, 286M-run complete periodic table).

**The survival audit.**

| chapter-one theorem | verdict under cross-amendment |
|---|---|
| Gridlock | **survives verbatim**, across the whole semantic lattice (its only hypothesis is that the guard contains a vacancy clause) |
| Single-Author / parity ≡ OR | **survives iff amendment in-degree ≤ 1** (⟺ the target map is a permutation); splits at **two laws in one cell** |
| Dead Letter | **fails under parity, survives under OR** — it holds exactly when the resolution is *strict* |
| Anchor (permanence of the eldest law) | **fails from one placed law**; replaced by Path-Sum Confinement + a Zero-Sum No-Go |
| 2-D ray confinement | fails as stated; the reach is a finite union of rays ℕ·S_Z, so diagonals are exactly the cycles with diagonal offset-sum |
| "all periods are powers of two" | **fails** — the cross-amendment spectrum runs to 30 |

**The organising invariant** is the **cycle offset-sum** S_Z = Σ_{k∈Z} c_k over
cycles of the amendment digraph. Path-Sum Confinement bounds support by path
sums (linear growth in every dimension); the **Zero-Sum No-Go** says that if
every reachable cycle has S_Z = 0 the code is bounded forever (39.8M-run
complete certificate); and a glider's velocity is always a **positive multiple
of S_Z**. *Where chapter one read the order of ℤ, chapter two reads the
arithmetic of the amendment digraph's cycles.*

**Balance, final form.** Under parity a code is fixed iff its active laws
partition into **cohorts**: even-sized groups of *distinct* kinds proposing the
same amendment at the same cell. Minimum two laws — and the minimal witness
puts both **in a single cell**: `BAL-1`, kinds 0 and 1 both (0,−1,−1) both
targeting kind 0, stacked at one cell, active forever, fixed forever (verified;
changes under OR). Balance is not measure zero: the exact count satisfies
a(s) = 4a(s−1) − 2a(s−2), entropy 1.7716 of 2 bits per cell — and 70.1 % of the
1,572,788 balanced verdicts in the complete census are *reached* rather than
seeded, refuting X-D's own prediction that balance is a seeding artefact.
**My duality (X2) is refuted outright**: balance can exist with every present
kind amendable (`BAL-3`). Entrenchment in balance is *dynamic*, not structural.

**The second escape — and the deeper reading of the Anchor Theorem.** X-D's
semantic-lattice sweep found the live axis: **sunset-by-default**, where a law
lapses unless re-enacted. It is the only semantics in the lattice that breaks
the Anchor's locality hypothesis, and **free gliders exist there on ℤ with
own-kind targeting** — 11.4 / 15.4 / 15.5 % of a complete 139,968-code box at
τ = 1, 2, 3, with speeds 1, 2/3, 1/2, 1/3, 1/4, 1/6.

> **What forbids motion on the line is permanence, not own-kind targeting.**

Two independent escapes, then, and together they say something the founding
note could not: a statute book can move only if its provisions either
**legislate broadly** (out-degree ≥ 2, X-A) or **expire on their own**
(sunset-by-default, X-D). Permanent, narrow law is motionless — that is the
Anchor Theorem's real content.

**Convergence worth recording.** X-D's complete two-kind periodic table
(2,916 constitutions × 49,152 seeds × 2 resolutions = **286,654,464 certified
runs**, 757 symmetry orbits, census constant on every orbit) reports
**zero gliders** — and X-D flagged that as its sharpest open question, having
run concurrently without X-A's result. It is not open: the box is entirely
single-target, so the zero is exactly the empirical shadow of the Out-Degree
Law. Two expeditions, different methods, same wall.

**Also**: `CRY-1`, a period-3 cycle at constant occupancy (verified), where
own-kind linearity would force a power of two; `OWN-8`, one own-kind law
(0,−1,1) at cells {0,2,4,6} with period **8** (verified), refuting the
chapter-one census remark that random-seed cycles carry only periods 2 and 4 —
the "powers of two" law itself stands; and a semantic-lattice verdict that
quorum guards are structurally inert (every confinement theorem here is
guard-free) except at quorum = {2}, where Gridlock *inverts*.

## 5. Scorecard against the frozen predictions

- **X1 (balance exists, minimum 2 laws, none under OR)** — **HELD** for the
  witness and the OR half (verified); the minimality claim is X-D's.
- **X2 (the duality: motion needs every kind amendable, balance needs an
  immortal kind)** — **REFUTED in both halves, and replaced by a better pair.**
  Motion is governed by *out-degree*, not amendability; balance by *in-degree*
  and parity, and X-D exhibits balance with every present kind amendable, so the
  entrenchment in balance is dynamic rather than structural. The surviving
  statement is the degree table in §3.
- **X3 (no glider in E2; supersession the likelier home of motion; a rake before
  a clean glider; ≈35 % that a certified 1-D glider appears)** — **half right,
  and instructively so**. The E2 no-go held *and* was proved by exactly the
  monovariant sketched in the charter. The guess about *where* motion lives was
  wrong in both halves: supersession is provably dead, and motion lives in the
  multi-target sector I did not name. A glider was found — a period-1 one with
  two laws in one cell.
- **X4 (cross-amendment breaks α = 1; ≈ 60 %)** — **HELD**, and settled in both
  directions: α ≤ 1 is a theorem exactly when out-degree ≤ 1, and α = 2 is
  attained by a one-law seed the moment out-degree reaches 2.
- **X5 (odd periods appear under non-injective targeting and supersession;
  permutation constitutions keep 2^a·L-type periods)** — **HELD**: the complete
  two-kind spectrum is {2,3,4,5,6,7,8,9,10,12,14,16,18,30}, with the odd periods
  contributed by the constant (non-injective) target maps exactly as predicted.
- **X7 (some semantics from the referent's lattice yields a phenomenon with no
  analogue elsewhere)** — **HELD, and it is the chapter's second theorem-grade
  result**: sunset-by-default admits free gliders on ℤ under own-kind targeting.
- **X6, X8** — pending.

*The pattern worth keeping: the structural intuition (a tropical monovariant
kills single-target motion) was sound, while the taxonomic guess (which named
sector would harbour the specimen) was not. The charter's own escape lattice
mislabelled the live sector as dead — a chapter-one error found by chapter two.*
