# Nomodynamics — founding session findings
*2026-08-26. First-contact results for the window-1 nomic chain (parity semantics),
obtained hands-on before the three sub-expeditions (glider-question/, nomos2d/,
rings/) launched. Scored against the pre-registrations in NOMOS.md §3.*

## Specimens and phenomena (all verified by direct simulation)

- **Colonizers.** Law (0,1,1) — "while I stand and my right is vacant, enact my
  kind to the right" — marches rightward at speed 1: only its frontmost copy is
  ever active; the wake is inert solid code. Mirror: (0,−1,−1). The only two
  single-law growers among 27.
- **The sunset clause.** Law (0,−1,1) enacts a right-neighbor which its own
  presence then blocks; the pair then repeals — a period-2 blinker.
- **Sunset codes.** Blocks of type (−1,1,0) dissolve from their newest end at
  speed 1 (the edge law, seeing vacancy ahead, perpetually repeals itself).
- **Welds.** Two colonizer fronts meeting fuse into frozen solid with a
  double-law seam at the junction ("2" cell) — total activity death.
- **Assimilation with refraction ≈ 2.** A colonizer front consumes a sunset wall
  at speed ≈ 1/2 (vs 1 in vacuum), converting it to its own kind, with a
  characteristic transient scar (brief bite-back into its own wake at contact).
- **Wall transparency classes.** Of 27 wall types facing an X-front: 19 opaque
  (weld/freeze), 3 pulsing interfaces (persistent boundary activity), 5
  effectively transparent (self-eroding or same-kind-trivial).
- **Conversion waves.** In porous period-2 media, point defects launch one-way
  waves converting porous code to solid gridlock (speed ≈ 2/3, stuttering edge),
  anchored at the defect — not localized signals.

## Laws of the territory (proved or proof-sketched)

- **The Gridlock Theorem** (trivial once seen, structurally decisive): in any
  solid region all three offsets of every law point at occupied cells, so every
  vacancy-guard fails: *fully-occupied code is frozen; all dynamics is surface
  dynamics.* Corollary: solidification is death; the living structures are
  interfaces.
- **The Front Law (no-go for free gliders under parity).** In a static occupancy
  background each law-type's indicator field evolves F₂-linearly (masked
  shift-and-add). A finite-support pattern translating by d with period p in a
  uniformly-enabled region would require (1 + σᶜ)ᵖ = σᵈ in F₂[σ, σ⁻¹] — but
  binomial expansion mod 2 leaves ≥ 2 terms; impossible. Hence every localized
  propagating structure must be an occupancy front. This *explains* the census
  (complete 1-and-2-law sweeps at W=1: fronts, blinkers p ≤ 4, welds — nothing
  else) and *refutes pre-registration N3* (a glider among small seeds): the
  territory answered back with a theorem. Formalization delegated to
  glider-question/.

## Pre-registration scorecard (NOMOS.md §3)

- N1 (degenerate majority): **HELD** — 21/27 single laws freeze, 2 die.
- N2 (structured growth from ≤2 laws): **HELD** — colonizers; two-front growth.
- N3 (free glider among seeds ≤2): **REFUTED, with mechanism** — the Front Law.
- N4 (speed quantization): **PARTIAL** — observed speeds 1, 2/3, 1/2 (vacuum
  colonization, conversion waves, in-medium assimilation).
- N5 (constitution algebra): delegated to rings/.
- N6 (cryptids near the summit): open; 1D looks tame; 2D is the live hope.

## Rings expedition results (N-C, same day — see rings/RESULTS.md)

- **Single-Author Lemma.** Kind k = (a,b,c) at slot j can only be toggled by the
  kind-k law at j − c: one author per (slot, kind) — in ANY window and ANY
  dimension. Corollaries: OR ≡ parity identically (the resolution-variant axis
  collapses); the per-kind dynamics is occupancy-modulated F₂-LINEAR everywhere.
- **Dead Letter Theorem.** Fixed ⟺ every law blocked; *balanced constitutions
  (living-but-stationary codes) do not exist.* Stability is always gridlock.
- Exact fixed-point counts (transfer matrix, brute-force-verified); no critical
  density (smooth extinction → porous-frozen → solid-gridlock crossover);
  transients ≤ m; random-seed cycles only p ∈ {2, 4}.
- **The Sunset Parliament.** Single-kind (0,−1,1) ring codes achieve exact
  maximal cycles at resonant circumferences m ≡ 2 (mod 4): periods 15 (m=10),
  63 (m=18), **341 (m=22)** — a wave rotating 2 cells per 3 steps; the
  Mersenne-flavored periods are orders of F₂ polynomials (number theory
  governing constitutional cycles). Constant-occupancy cycles cap at powers of
  2 (unipotency).
- Gardens of Eden: exact predecessor algebra (occupancy-fibered unipotent
  inversion); GoE fraction peaks ≈ 33% at mid-density. Unique minimal taut
  architecture: the 2-law **Mutual-Veto pair**.

## Glider resolution (N-A) and 2D first contact (N-B) — same day

- **The Anchor Theorem** (supersedes the Front Law, proved in
  glider-question/RESULTS.md): own-kind toggles of kind t land only at t's own
  offset c_t, so the extremal law on the trailing side of any finite code on ℤ
  is never targeted — *the eldest law cannot be repealed*. Consequence: free
  gliders are impossible in every window, dimension, guard predicate, and
  resolution semantics of own-kind nomodynamics. Purely combinatorial; verified
  against ~15.3M certified runs (complete through 4 laws / 5 cells at W1; zero
  gliders, zero parity/OR divergences, zero anchor violations; all holdouts
  resolve to aperiodic anchored "ruler fronts").
- **Ring rotors** — the theorem's sharpness made flesh: on ℤ/6, a 3-law packet
  hops 3 cells per step (family on every even m ≥ 6) — the first moving
  law-packets of the field, existing exactly because a circular code has no
  eldest law. *Entrenchment is a theorem of linear order; circular codes can
  revolve.*
- **2D own-kind (nomos2d/RESULTS.md)**: ray-confinement theorem (each type is
  pinned to one axis ray; growth is 1D forever; quadrants never fill); 239
  certified half-turn rotors ("pinwheel ordinances"); all periods powers of 2;
  Pascal-column growers with size(t) = 2^popcount(t); and **the Jubilee Code**
  — a ~26-law machine, aperiodic through 300k fully-hashed steps, quiescent
  except at t = 2^k when the whole code ignites (~770 laws) and collapses back
  to a handful — a binary counter native to law-space, and an attractor: 791 of
  60,000 random seeds converge to its family. Interaction chart: right-of-way
  transparency, 0–3-step phase refraction, entrenchment caps.
- **The door to the wild sector, theorem-marked**: escaping Anchor/Single-Author
  requires cross-amendment (laws amending other kinds — truer to real law).
  First probes: parity/OR genuinely split (20/4,000 seeds; supersession splits
  at exactly 2 laws); diagonal motion unlocks in 2D; a cross-amendment no-go for
  some classes is conjectured with evidence (glider-question/). The wild sector
  is one honest generalization away, with its doorway located exactly.

## Reading (theory frame)

**Own-kind nomodynamics is an exactly solvable linear theory in disguise** —
the Single-Author Lemma makes the whole founding semantics occupancy-modulated
linear algebra over F₂, completely analyzed within a day of its definition:
Gridlock, Dead Letter, the Front Law, Sunset resonances as polynomial orders.
By the standards of founding events this is the right first chapter: the
field's hydrogen atom — a solvable sector with named laws — plus a sharply
identified door to the wild sector. The door is **cross-amendment**: letting
laws amend OTHER kinds breaks single-authorship, which is provably the only
source of genuine nonlinearity here — and it is also *truer to the pre-formal
referent* (real laws amend other laws; own-kind was the tame simplification).
The founding session's linear sector + the cross-amendment frontier is the
field's opening structure: solvable core, wildness exactly one honest
generalization away.
