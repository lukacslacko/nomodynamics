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
τ = 1, 2, 3, with speeds 1, 2/3, 1/2, 1/3, 1/4, 1/6 *within the searched box* (see §5:
speed sets from bounded searches are narrow-glider statements).

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

## 5. The width correction — what a bounded search actually decides

Expedition X-E was sent to explain why the number of kinds appeared to cap the
speed. It found that the premise is false, and the way it fails is the more
valuable result.

> **Bounded searches decide a box, not a question.** Every census in this
> program used boxes of at most ~26 interior cells. The two-kind universe
> **MIRROR** (W = 1; rules (0,1,−1) and (0,−1,1), each amending *both* kinds —
> *a left-edge law pushes right, a right-edge law pushes left*) carries
> displacement-2 gliders of minimal period 4, 5, 6, 7 and 12, with spans
> **53, 20, 616, 438, 39**. Not one of them fits in the boxes that "decided"
> them impossible. Coordinator-verified: MIRROR-2/5, 32 laws over 20 cells,
> Φ⁵ = σ² under parity and correctly *not* a glider under OR.

A second confound compounds the first: a sweep restricted to **coprime** (p, d)
is structurally blind to Φ⁴ = σ² whenever Φ² = σ¹ fails — and MIRROR's family
is exactly of that shape.

**Consequence, applied to this document.** Every "decided impossible" produced
by a fixed box — in `xamend1d/RESULTS.md` §4.6, in the sunset speed sets of
`xtheory/`, and in my own earlier summary of the speed spectrum — is a
statement about **narrow** gliders and is re-labelled as such. The *theorems*
are untouched: the Out-Degree Law, the supersession no-go, the Tropical Speed
Law, Path-Sum Confinement and the Balance Theorem are proofs, not box searches.
It is precisely the census-shaped claims that needed the correction — which is
the program's own thesis about celebrity samples, arriving on schedule and at
its own expense.

**What survives, and is sharper.** In the **single-field sector** — every kind
sharing the same target set, so the system is a one-bit automaton with n
channels — the measured cap is `|d| ≤ 2` under parity and `|d| ≤ 1` under OR at
two channels, **for any number of channels and at any width** (33,630
constitutions decided, 0 undecided, by a new subshift-of-finite-type decider
that carries *no* width bound at all). The resource that buys `|d| ≥ 3` is
**another 𝔽₂ field, not another kind**: four kinds in one field cannot reach
(4,3) at any width; four kinds in two fields reach it with a three-cell seed.

**New theory.** The *Dilation Theorem* — (W, p, d) ↦ (rW, p, rd) — rules out any
width-independent cap a priori. The *Even-Support Law* (Theorem K): for any
subset U of kinds with |T_k ∩ U| even for every k, the symmetric difference of
the supports over U is a constant of the motion, and must vanish in a glider;
the relevant determinant over 𝔽₂ is the parity of the amendment digraph's cycle
covers. It strictly generalises X-A's Twin-Kind Lemma (239 non-twin instances;
27,876 fuzz checks, 0 violations).

**The fourth parity/OR split, and the sharpest.** `TRIAD` (three kinds, W = 2,
single field, seeded with **one cell** carrying all three): the same seed in the
same universe is a **p = 3, d = 5** glider under parity and a **p = 2, d = 3**
glider under OR — different period *and* different displacement
(coordinator-verified, including that each verdict fails for the other's
(p, d)). The resolution convention does not merely decide whether a code moves;
it decides **how fast**.

## 6. Rings — and a retraction that reaches back into chapter one

Expedition X-C (`xrings/RESULTS.md`; 122,238 complete state-space censuses =
3.5 × 10¹⁰ codes. Rings are the one sector where "complete" is honest without a
width caveat: a ring code cannot be wider than its ring.)

### The retraction

Chapter one's **ring rotors** were reported as *"the first moving law-packets of
nomodynamics"*, hopping m/2 cells per step — and the founding note, the README
and the demo all said so. That reading is **wrong**, and X-C caught it.

> On ℤ/m, `Φ(S) = rot_r(S)` says the code coincides with its own rotation. It
> does **not** say anything travelled. With window-1 laws information moves at
> most one cell per step, so any rotor with min(r, m−r) > p is *apparent*
> rotation. In the founding ℤ/6 specimen exactly **two cells change per step** —
> a repeal at cell 1, an enactment at cell 4 — while the resulting state happens
> to equal its own rotation by three (coordinator-verified, including that the
> seed has no rotational symmetry of its own, so r = 3 is the *only* rotation
> relating the two states). Nothing hops three cells. It is a **barber pole**.

Every own-kind ring rotor found fails the light-cone test, and releasing 19,074
such ring codes onto ℤ gives **zero** gliders — exactly as the Out-Degree Law
requires. So the corrected picture is simpler and stronger than the one it
replaces: **chapter one contains no transport anywhere** — not on the line, and
not on rings either. Genuine transport on a ring is a wrapped cross-amendment
glider: TANDEM-1 rotates by one cell per step on every m ≥ 3, inside the light
cone. The old slogan ("entrenchment is a theorem of linear order; circular codes
can revolve") is retired; what rings supply is apparent rotation, and what buys
motion is still out-degree.

### The Cycle-Length Law — why chapter one's clocks were 2-adic

The frozen-occupancy step operator of an L-cycle permutation constitution lives
in 𝔽₂[y]/(y^L − 1), **which is local exactly when L is a power of two**. So:

> "All periods are powers of two" was never a fact about own-kind amendment. It
> was a fact about **cycle length 1** — and 1 is a power of two. An odd factor
> L′ | L contributes 𝔽_{2^d} factors with d = ord_{L′}(2), and the odd periods
> appear immediately.

Predicted and measured exactly at every L = 1…7: L = 3 → 3, L = 5 → **15**,
L = 6 → 3·2^k, L = 7 → **7**. And it shows in the dynamics: on ℤ/3, own-kind
gives periods {1,2}; a 3-cycle gives {1,2,3,4,6,8}; a 5-cycle — complete over
all 248,832 constitutions — gives {1…16, 20, 22, 26, 30, 32, 40, 60}, i.e.
**every odd period 3, 5, 7, 9, 11, 13, 15 from two laws on three cells**.
Controls with the same rule pool and state space (only the target map changes)
at m = 12: own-kind reaches 12 distinct periods, cross-amendment 36. A new
resonance family appears at powers of **three** (27, 45, 81) where own-kind gave
Mersenne numbers (15, 63, 341).

### The rotor gallery (all coordinator-verified)

* **Q-4** — cross-amendment lowers the minimal rotor ring from 6 to **4**:
  `X = (−1,1,−1) → Y`, `Y = (0,−1,0) → X`, three laws on ℤ/4, `Φ = rot₂`.
* **D-3, the doctrinal rotor** — three kinds all `(0,−1,0)` with cyclic targets,
  two laws at one cell of ℤ/3: the **occupied cells never change**, while the
  *kinds* circulate through them and return after three steps. A code frozen on
  its face whose doctrine rotates underneath. No own-kind analogue exists.
* **O-15** — the first rotor on an **odd** ring (prediction X6): twelve laws on
  ℤ/15 with `Φ = rot₅` exactly. Every odd-ring rotor found has r ≡ ±m/3, so
  3 | m (the *Third-Turn* pattern, evidence-grade; confirmed at m = 15, 21, 27,
  33, absent at 9, 25, 35).
* **K-6** — a kind relay that advances two cells *and* changes kind each step,
  closing after three.

### Also proved, and one prediction refuted

The own-kind base rotor family is now derived rather than surveyed: the block
word forces **m = 2γ+4 with hop m/2**, so its restriction to even rings is a
theorem (γ = 1…39 verified). Balance on rings obeys a trichotomy — fixed ⟹ dead
under OR, under `super_or`, and under **every injective target map** (26,244
exact counts, 0 violations) — and under the two-chamber veto **88.8 % of all
fixed codes on ℤ/20 are balanced**, against 0 % for own-kind. X-C's own
pre-registrations P5 (Σc predicts rotation), P8 and P9 were refuted and kept.

## 7. The field computes — and it does so standing still

Expedition Y-B (`computation/RESULTS.md`, 21/21 own battery). Both headline
constructions re-verified by the coordinator against independently written
references.

**The one idea.** A guard — citation *or* the founding occupancy guard — is an
AND-NOT read at fixed offsets, and parity resolution makes several authors of
the same provision XOR together. AND-NOT with XOR is functionally complete; the
only missing ingredient is *assignment*, because a toggle accumulates. That is
supplied by

> **the self-clearing kind**: a provision that repeals *itself* every step. With
> `f(t)` the XOR of every other author's toggle of that slot,
> `x(t+1) = x(t) ⊕ x(t) ⊕ f(t) = f(t)`.
> **A law that expires every step is a register: the code writes it rather than
> amending it.**

> **Theorem (Statute-Circuit).** A constitution in the resulting normal form
> *is* a synchronous AND-NOT network with free XOR fan-in, free fan-out (guards
> are read-only, so any number of gates may cite the same slot) and unit delay.
> A law nobody amends is a **gate**; a law that repeals itself is a **wire**.

**Rule 110 runs inside a constitution.** 24 kinds, window 1, parity, three
nomodynamics steps per Rule-110 step, one cell per cell. The certificate is
*complete rather than sampled*: every offset lies within ±1, so three steps form
a local map on a 7-cell window, and running all 2⁷ = 128 configurations of ℤ/7
evaluates that map at **every one of its inputs** — which decides ℤ entirely.
Coordinator-verified independently: all 512 configurations of ℤ/9 for 8
Rule-110 steps and 40 random configurations of ℤ/17 for 25 steps against a
bit-parallel reference, zero mismatches; and the battery now carries the
complete ℤ/7 certificate.

> **Theorem (finite-code universality).** Every Turing machine compiles into a
> **finite code** of the *founding* occupancy-guard sector, with unbounded tape
> supplied by a self-extending front. Hence nomodynamics is
> **computation-universal**, and halting for finite codes is **undecidable**.

Coordinator-verified against a reference simulator written from scratch: 15
machines — including binary increment and busy beavers 3 and 4, plus ten random
3-state machines — 14 steps each, 225 configurations compared, zero mismatches.

**Citation turned out to be unnecessary, refuting my own charter prediction Y3.**
The founding guard *already* reads "some law stands at i+a **and** none at
i+b" — an AND-NOT over the occupancy field. Citation only buys several bits per
cell; spend cells instead of kinds and the whole circuit substrate reappears
with plain occupancy guards.

**And the deepest sentence the program has produced.** Chapter one spent its
entire effort proving that nothing can move; chapter two priced motion exactly;
chapter four found that motion needs mortality. Computation needs none of it:

> Every gate law and every POWER law is exactly where it started — certified over
> 60 steps at out-degree 1. **A statute book can compute while every one of its
> provisions stands still.** What moves is not law but *information*, and
> information moves because the guards read across cells.
> *Motion was never the resource. The vacancy clause was.*

**Complexity, and where computation is not.** Prediction is **P-complete** under
log-space reductions already at dimension 1, window 0, one cell (complete
certificate over all 256 Boolean functions of three variables). By contrast the
single-author sector is 𝔽₂-linear with Φᵗ = Lᵗ, so prediction there is in **NC**
and is not P-complete unless NC = P: chapter one's exactly solvable sector is
*provably* the wrong place to look for computation, which is exactly why it was
solvable.

**Where it stops, honestly.** The ballistic route — Life-style glider collisions
— does *not* work: 58,203 certified collision runs produced no reflector, no
fan-out, no transparency and no annihilation, with MIRROR freezing everything it
touches and TRIPTYCH detonating everything it touches. Both gateless, for
opposite reasons. Every one of those zeros is labelled a **box** statement, and
the expedition applies the width correction to itself: MIRROR's own gliders span
20–616 cells and were invisible to every earlier census in this program. Also
not claimed: minimality (24 and 31 kinds are what these constructions happened to
need), and **the strict own-kind sector of chapter one remains open** — every
construction here uses cross-amendment, even where out-degree is 1.

## 8. Self-replication — and it is not Fredkin's

Expedition Y-C (`replication/RESULTS.md`, 37/37 own battery). Both headline
specimens re-verified by the coordinator.

The mission pre-registered a four-rung hierarchy and reached **rung 3**: an
unbounded colony of free, exact, debris-free copies.

* **THE SPLIT DECISION** (2 kinds, 2-D, citation, OR) performs true binary
  fission: `Φ²(S) = σ^(0,−2)(S) ⊔ σ^(0,+2)(S)` **exactly** — the parent does not
  survive, the children are separated by more than the interaction radius, and
  the debris is empty. At every even t the state is exactly t/2+1 free exact
  copies (verified to 100 copies at t = 198).
* **THE ENGROSSMENT** needs no citation at all — plain occupancy guards and
  parity, the **founding semantics**: `Φ⁴(S) = S ⊔ σ^(4,4)(S)`, with
  `2^popcount(t/4)` copies (64 at t = 252, verified).

**The hoped-for theorem is refuted.** I expected replication here to be the
known additive (Fredkin) phenomenon of 𝔽₂-linear automata. The decisive test is
splitting — does `Φᵖ(S) = Φᵖ(A) Δ Φᵖ(B)` over splittings `S = A ⊔ B`? — and the
replicators fail it: THE ENGROSSMENT 8/10, THE PRECEDENT 10/10, THE QUORUM 2/2.
Remove one law of four, evolve the halves, XOR them, and *the child is simply
absent*. Two traps were identified and avoided: **`2^popcount(t)` is not a
signature of additivity** (it survives into a demonstrably non-additive system),
and a random-pair superposition test measures the *constitution*, not the
replicator. The genuinely additive specimens are reported as Fredkin and nothing
more.

**A no-go worth as much as the specimens.** `card(S_t) ≤ n(s₀+2Rt+1)^D` — the
light cone bounds the population polynomially — so **exponential replication is
impossible in every dimension**, and no fixed-period doubling can survive: every
free fission must eventually self-collide. THE ENGROSSMENT accordingly doubles
at t = 4(2^k−1), at exponentially stretching intervals, exactly as forced.

**The fauna audit bites, and was run honestly.** LAND GRANT, SOWER, PICKET
PUFFER and the colonizer block are **rung 1 only** — a solid growing region
trivially contains translates of its sub-blocks, which is why rung 2 demands
whole *causal components*. Every gun and rake is **rung 0**: not one lays copies
of its own head. The Pascal column is rung 3 but was ruled degenerate by the
expedition's own pre-registered clause.

**Rung 4 (von Neumann's constructor) was not reached, as pre-registered**, but
both halves were built: **THE ENGROSSING CLERK** reads a blueprint carried in
its own body and constructs a decoded, *different* target from it, and **THE
SCRIBE** copies an arbitrary blueprint faithfully without bound. Neither ever
holds two complete copies of its machinery at once, and the reason is
structural: a child built next door is within the interaction radius of its
parent, so it can only become free by *travelling*. Hence the sharpest open
question the program now has:

> **A rung-4 object in nomodynamics is a blueprint-carrying packet that moves.**
> Chapter two says travelling needs out-degree ≥ 2; chapter three says reading
> needs citation; nothing found so far forbids the combination — and nobody has
> built it.

**Scope.** Complete on ℤ: 6,561 occupancy constitutions × 4 modes × 45 seeds
(1,180,980 runs, 0 hits) and 531,441 citation constitutions × 2 modes × 9 seeds
(9,565,938 runs, 71,784 rung-2 hits — **every one of them citing a kind, none
with pure occupancy guards**, so on the line citation is the enabler). Sampled in
2-D: ≈22.7M runs, 71,511 exact hits, roughly one sampled constitution in 5.5
carrying one. Every zero is labelled a box result.

## 9. Scorecard against the frozen predictions

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
- **X6 (cross-amendment rotors appear on odd rings; ≈ 65 %)** — **HELD**:
  O-15 on ℤ/15, and a Third-Turn pattern (3 | m) across m = 15, 21, 27, 33.
- **X8 (no universality this cycle; ≈ 90 %)** — **HELD**: it stays open, and no
  expedition claimed otherwise.

*The pattern worth keeping: the structural intuition (a tropical monovariant
kills single-target motion) was sound, while the taxonomic guess (which named
sector would harbour the specimen) was not. The charter's own escape lattice
mislabelled the live sector as dead — a chapter-one error found by chapter two.*
