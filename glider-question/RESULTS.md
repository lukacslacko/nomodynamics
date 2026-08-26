# The Free Glider Question — RESOLVED (no-go theorem)
### Expedition N-A, Treeline program · 2026-08-26
*Question: does 1-D nomodynamics admit a free glider — a finite law-packet S with
Φᵖ(S) = σᵈ(S), p ≥ 1, d ≠ 0 — under parity or OR-toggle resolution, any window?*

**VERDICT: NO — and not by exhaustion but by theorem.** The Front Law is now a
proved theorem (the **Anchor Theorem** below), covering parity *and* OR-toggle,
every window W, and in fact every dimension. Along the way the OR-vs-parity
axis itself collapses: the two semantics are **identically equal** dynamical
systems (Collision Lemma = the Single-Author Lemma, found independently by
Expedition N-C), because two same-kind actors can never target the same cell —
the "two-actor regime" the OR-hunt was to search is *empty*. All sweeps
(inventory in §5; ≈ 15.3 million certified classifications across four
universes) agree: zero gliders, zero parity/OR divergences, zero anchor
violations. And the theorem's boundary is mapped by *realized* phenomena: on
rings, where there is no eldest law, verified **rotors** exist (§4.2) — the
first moving law-packets of nomodynamics. The foundational law:

> **In 1-D nomic chains, all propagation is frontal.** Per kind, one edge of
> the population is pinned for its entire lifetime at an unrepealable anchor
> law; all change radiates to the other side. *The eldest law cannot be
> repealed.*

The hypotheses that carry the theorem are identified exactly (§2.3), and every
escape from it is charted and probed (§4): rings (rotors exist — the order of
ℤ is load-bearing), reciprocal amendment (anchor dies, single-authorship
survives, no glider in 2.79 M seeds), and supersession (the one place the
resolution axis awakens — parity ≠ OR from exactly 2 laws; no glider in 1.2 M
seeds). The cross-amendment universes are where the hunt continues.

---

## 1. Setting (precise)

Fix a window W ≥ 1. The **kind set** is T_W = {−W..W}³, |T_W| = (2W+1)³
(27 at W=1, 125 at W=2). A **state** is a map S : ℤ → 2^(T_W) with finite
support; occ_S(i) = [S(i) ≠ ∅]. A law is a pair (i, t), t = (a,b,c), present
when t ∈ S(i). Law (i,t) is **active** in S iff occ_S(i+a) = 1 and
occ_S(i+b) = 0 (occupancy guards). Each active law of kind t at i emits one
**toggle of kind t at cell i + c**. Synchronous update; per-(cell, kind)
resolution of the received toggle multiset:

- **parity**: kind t at cell j flips iff it received an odd number of toggles;
- **OR-toggle**: kind t at cell j flips iff it received ≥ 1 toggle.

Φ_par, Φ_or denote the two update maps; σᵈ the translation (σᵈS)(i) = S(i−d).
A **free glider** is a finite S ≠ ∅ with Φᵖ(S) = σᵈ(S) for some p ≥ 1, d ≠ 0.

## 2. The theorems

### 2.1 Collision Lemma = Single-Author Lemma (the resolution axis is vacuous)

**Lemma 1.** *In every state S, for every kind t and cell j, the number of
active kind-t laws targeting j is at most 1 — indeed the only law that could
ever toggle the slot (j, t) is the kind-t law at j − c_t. Hence Φ_par = Φ_or
identically: parity and OR-toggle define the same dynamical system — for every
W, and likewise on ℤⁿ and on rings ℤ/m.*

*Proof.* A kind-t actor targeting j stands at i = j − c_t, and there is at most
one kind-t law at one cell. So the multiplicity is ≤ 1, where "odd" ⟺ "≥ 1". ∎

(Found independently and simultaneously by Expedition N-C as the
**Single-Author Lemma** — `rings/RESULTS.md` Lemma 0, where their engine
asserts it on every step; the two proofs are the same. Below "own-kind
dynamics" names the unique semantics that parity and OR both denote.)

Guards are irrelevant (they only thin the actor set); so is dimension (i = j −
c_t still unique). Consequences:

- The pre-registered question "compute the minimal configuration size at which
  two same-kind actors target the same cell simultaneously" has answer:
  **no such configuration exists, at any size** — the premise that OR-toggle
  escapes linearity above some seed size is false. OR-toggle *is* the parity
  system; per-kind dynamics is exactly F₂-linear (given occupancy) at every
  scale, under both names.
- Machine verification: every seed of the W1 ≤3-law and W2 ≤2-law complete
  sweeps and the 10⁶-seed W2 3-law sample was run as a *lockstep duel* — both
  engines advanced in parallel with state equality asserted at every step of
  every trajectory (§5): **0 divergences**. An instrumented step measured
  per-(target, kind) actor multiplicity on 20 000 random dense states: max = 1.
- The resolution axis becomes meaningful only when effects cross kinds — see
  §4, where the minimal bifurcation witness has exactly **2 placed laws**.

### 2.2 The Anchor Theorem (the Front Law, final form)

The previously established front-law argument was conditional (static
occupancy backgrounds). The unconditional obstruction is elementary and much
stronger. Three structural hypotheses:

- **(H1) own-kind effects**: presence of kind t at a cell changes only via
  toggles emitted by kind-t laws;
- **(H2) rigid displacement**: a kind-t law at i emits only at i + c_t, with
  c_t a constant of the kind;
- **(H3) locality of amendment**: a (cell, kind) pair receiving no toggle is
  unchanged.

Parity and OR-toggle (and enact-only, repeal-only, any threshold resolution)
satisfy H1–H3; the guard predicate may be *anything whatsoever* (occupancy
guards, kind guards, arbitrary nonlocal predicates) — activity only selects
which laws emit.

**Theorem 1 (Anchor).** *Let the dynamics satisfy H1–H3, S₀ any state, t a
kind present in S₀, X_n = supp_t(S_n) its cell support at time n.*

1. *If c_t > 0, let m = min X₀. Then for all n: t ∈ S_n(m) and X_n ⊆ [m, ∞).
   The leftmost kind-t law is **permanent** and the left edge of the kind-t
   population is **pinned at m forever**.*
2. *If c_t < 0, mirror: the rightmost kind-t law is permanent, right edge
   pinned at max X₀.*
3. *If c_t = 0: X_{n+1} ⊆ X_n — the support is monotonically non-increasing
   (a cell that loses its law never regains it).*
4. *Kinds are never born: X_n = ∅ implies X_{n'} = ∅ for all n' ≥ n.*

*Proof.* (1) Induction on n with hypothesis (t ∈ S_n(m)) ∧ (X_n ⊆ [m, ∞)); base
by definition of m. Step: by H1–H2 every kind-t toggle at time n is emitted
from some i ∈ X_n ⊆ [m, ∞) and lands at i + c_t ≥ m + 1. So no cell ≤ m
receives a kind-t toggle: by H3 the law at m survives and no kind-t law appears
left of m + 1. (2) mirror. (3) c_t = 0: toggles land exactly on X_n, so cells
outside X_n receive nothing and stay empty of t; hence X_{n+1} ⊆ X_n. (4) no
actors, no toggles, and H3. ∎

**Corollary 1 (No free glider).** *Under H1–H3 there is no finite nonempty S
with Φᵖ(S) = σᵈ(S), p ≥ 1, d ≠ 0. In particular 1-D nomodynamics has no free
glider under parity or OR-toggle resolution, for every window W — and the same
holds verbatim on ℤⁿ.*

*Proof.* Suppose S were one; then supp_t(Φ^{kp}S) = supp_t(S) + kd for every
kind t present and all k ≥ 0. Pick any present kind t.
— If c_t > 0: by Theorem 1.1 the anchor cell m carries t at *every* time, so
m ∈ supp_t(S) + kd for all k, i.e. m − kd ∈ supp_t(S) for all k — infinitely
many cells in a finite support. Contradiction. — c_t < 0: mirror.
— If c_t = 0: Theorem 1.3 gives supp_t(S) + kd = supp_t(Φ^{kp}S) ⊆ supp_t(S),
impossible for a finite nonempty set with kd ≠ 0 (extremal cell argument). ∎

On ℤⁿ, for c_t ≠ 0 run the same induction on the linear functional
φ(x) = ⟨x, c_t⟩: targets satisfy φ(i + c_t) = φ(i) + |c_t|² ≥ φ(i) + 1, so
every kind-t law on the minimal φ-level is permanent. Permanence alone then
kills translation by *any* vector v ≠ 0 — including v ⊥ c_t — because a fixed
anchor cell x₀ carried by all S_kp forces x₀ − kv ∈ supp_t(S) for every k,
infinitely many cells in a finite support; and for c_t = 0 the monotone support
gives supp_t(S) + kv ⊆ supp_t(S), impossible for finite nonempty sets (maximize
⟨·, v⟩). Nothing in the proof uses synchrony; any serial or asynchronous
schedule satisfying H1–H3 obeys it too.

**Corollary 2 (All propagation is frontal).** *For every kind t with c_t > 0
the set of cells ever visited by kind t is contained in [m, ∞), with the
boundary cell m occupied by t at all times (mirror for c_t < 0; for c_t = 0 the
kind never spreads at all). Every kind's dynamics is strictly one-sided motion
away from an immovable anchor — an occupancy front. No bounded packet can
translate, because with respect to each of its kinds' c-directions its trailing
edge is frozen.*

**Corollary 3 (why caterpillars are impossible).** The engineered scheme —
kind A advances the head, kind B repeals A's tail — is void a priori: by H1
only A-toggles can remove A-laws, and by Theorem 1.1 A's rearmost law (w.r.t.
sign c_A) is never targeted by them. *No choreography of other kinds, guards,
or occupancy can ever repeal it.* The caterpillar drags an immortal tail.

### 2.3 Hypothesis audit — exactly what carries the theorem

| hypothesis | used for | if dropped |
|---|---|---|
| H1 own-kind effects | anchor untouchable by other kinds | cross-kind repeal → anchors mortal; gliders no longer excluded (§4) |
| H2 rigid displacement c_t | all targets on one side of the extremal law | state-dependent c could target backwards |
| H3 locality of amendment | untargeted pairs persist | near-definitional (what "amend" means) |
| the *order* of ℤ (an extremal law exists) | picking the anchor | on the ring ℤ/m there is no eldest law — and **rotors really exist** (§4.2) |
| parity resolution | **not used** | — |
| occupancy guards | **not used** (any guard predicate allowed) | — |
| window size / dimension / synchrony | **not used** | — |

The earlier conditional Front Law needed parity (linearity) and a static
background; Theorem 1 needs neither. Notably, *guards* — the only channel by
which kinds interact — cannot rescue gliders, because guards govern only
*whether* a law fires, never *where* its effect lands or *whose* kind it edits.

## 3. The linear front theory (quantitative layer, parity ≡ OR)

Fixing the occupancy trajectory O_n = occ(S_n), each kind's indicator field
x_t⁽ⁿ⁾ : ℤ → F₂ evolves linearly:

  x⁽ⁿ⁺¹⁾ = x⁽ⁿ⁾ + σᶜ(g⁽ⁿ⁾ · x⁽ⁿ⁾),  g⁽ⁿ⁾(i) = O_n(i+a) · (1 − O_n(i+b)),

with (σᶜ f)(j) = f(j − c); kinds couple only through occ. By Lemma 1 this exact
F₂ bookkeeping *is* the OR dynamics too — "small-seed linearity" is
unconditional linearity. In a **uniformly-enabled stretch** (every present
kind-t law active for n₀ ≤ n < n₀+p) the monodromy is (1 + σᶜ)ᵖ, and a
translating finite pattern would need a nonzero finite-support solution of

  (1 + σᶜ)ᵖ X = σᵈ X  in F₂[σ, σ⁻¹].

None exists: F₂[σ, σ⁻¹] is an integral domain, and (1 + σᶜ)ᵖ − σᵈ ≠ 0 because
(1 + σᶜ)ᵖ has 2^{s₂(p)} ≥ 2 monomials for c ≠ 0 (Lucas; s₂ = binary digit sum)
while σᵈ has one — and for c = 0, (1+1)ᵖ = 0 ≠ σᵈ. So X = 0. This was the
original Front Law; it is now the special case g ≡ 1 of Corollary 1, retained
for its quantitative content: in enabled regions x⁽ⁿ⁾ = (1 + σᶜ)ⁿ x⁽⁰⁾ gives
Pascal-mod-2 (Sierpinski) wakes, front speed |c| ≤ W, and the self-cancellation
times 2^k ((1+σᶜ)^{2^k} = 1 + σ^{c·2^k}) behind the observed sunset phenomena.

## 4. Sharpness: charting every escape from the theorem

First, a rigidity lemma that maps the whole variant space — it answers "what is
the minimal semantics that escapes single-authorship?" *structurally*:

**Lemma 2 (Rigidity of fixed targeting).** *Consider any semantics in which
each kind k, when active, toggles exactly one kind φ(k) at one fixed offset
c_k ("fixed single-targeting" — the coordinate-free form of the (a,b,c,e) /
kind-shift-δ proposals). Then:*
1. *Multi-authorship of some slot (j, t) requires φ non-injective.*
2. *If every kind is amendable (in-degree ≥ 1 under φ) and the kind space is
   finite, then out-degree ≡ 1 forces φ to be a **bijection** — so
   single-authorship (hence parity ≡ OR) is a theorem for the entire
   fixed-single-targeting class, not just for own-kind toggles.*
3. *A kind outside im(φ) is **immortal**; a pattern containing one is pinned
   (cannot translate), and by Theorem 1 a φ-fixed-point kind (φ(t) = t) in the
   pattern is anchored. So a glider could only ever live on a fixed-point-free
   sub-permutation of φ.*

*Proof.* (1) The author of (j, φ(k)) of kind k sits at j − c_k: for one k that
is one law. (2) Σ in-degrees = Σ out-degrees = |kinds|; all in-degrees ≥ 1
forces all = 1. (3) Nothing toggles it, and H1–H3 hold kind-wise. ∎

Consequently the escape lattice is exactly:
- **(E1) state-dependent targeting** (the target kind is read off the state,
  not the actor's kind) — canonical minimal instance: *supersession* (§4.1);
  the only route to genuine multi-authorship and a live parity/OR axis.
- **(E2) permutation targeting with a fixed-point-free cycle** — canonical
  minimal instance: *reciprocal amendment* (§4.3); single-author still holds
  (no OR/parity split), but for patterns built of cycle kinds the anchor
  argument dies.
- **(E3) multi-target laws** (out-degree ≥ 2). If each law still toggles its
  own kind among its targets ("riders"), the class is **provably glider-dead**:
  every kind remains its own sole author, Theorem 1 applies kind-wise, and any
  pattern is pure own-kind or contains an anchored kind. Fully-cross
  multi-target designs (no law toggles its own kind) can achieve fixed-target
  multi-authorship, but only by strictly enlarging the effect axiom
  (out-degree ≥ 2); charted, not hunted — E1 reaches multi-authorship with a
  single effect.
- **(E4) leave ℤ** (drop the order) — rotors exist on rings (§4.2).

### 4.1 Drop own-kind effects for state-dependent targets: supersession — the live hunt

Drop H1 minimally — **supersession semantics** (the most Nomic-natural
cross-kind effect: *a law enacted onto occupied ground displaces what stands
there*): an active law with target j = i + c **enacts its own kind at j if j is
empty, and clears the entire cell j (all kinds) if occupied**.

- **Anchors die**: any kind standing ahead can now clear another kind's anchor.
  Theorem 1 does not apply; gliders are no longer excluded by it.
- **The resolution axis awakens exactly here.** Cell-level clears can have
  multiplicity ≥ 2. Minimal bifurcation witness (machine-verified,
  `super_divergence.py`): W=1, **two placed laws** — A=(0,−1,1)@0,
  B=(0,1,0)@1. Cell 1 receives 2 clear-votes (A's forward clear + B's
  self-clear): OR-clear removes B (→ period-2 pulse), parity-clear keeps it
  (→ fixed point). Divergence at t = 1. On 20 000 random supersession states,
  0.87 % of trajectories diverge within 30 steps; single-law seeds never do
  (a 1-law state has one actor, and divergence needs ≥ 2 co-targeting actors,
  so 2 placed laws is the exact minimum). Instrumented multiplicity on 50 000
  random states: per-(cell) clear-vote counts up to **3** — multi-authorship
  is real and routine here, unlike anywhere in own-kind dynamics.
- Empirically (§5: complete ≤3-law/5-cell, 500,000-seed 4-law/5-cell sample,
  500,000-seed 5-law/6-cell sample — 1.2 million supersession seeds):
  **no glider** — fauna is fronts, pulses, and a much larger extinct fraction
  (1,972/200,133 at ≤3 laws, 14× the own-kind rate: mutual annihilation). A
  no-go, if true there, needs a new argument — the anchor is dead and the
  dynamics genuinely non-linear: **open**, flagged as the successor question
  with the two-actor parity/OR split as the first lever.

### 4.2 Drop the order of ℤ: ring rotors EXIST (verified moving law-packets)

The Anchor Theorem consumes the order of ℤ ("the eldest law"). On the **nomic
ring** ℤ/m there is no eldest law — and the theory predicts the obstruction
really vanishes: the translation eigen-equation lives in F₂[σ]/(σᵐ − 1), which
has zero divisors, so the Laurent-domain argument (§3) breaks. The census
delivers (`ring_rotor.py`, `ring_rotor3.py`): complete ≤2-law sweeps on
m = 3..12 find nothing, but complete 3-law sweeps find **18 verified rotors at
m = 6** — and single-kind scans reveal the family. Minimal specimen, W = 1,
**three laws of the single kind (0,1,−1)** ("while I stand and my right is
vacant, repeal my left") at cells {1,2,5} of ℤ/6:

```
t=0  |.XX..X|      X = law (0,1,-1);  each step the bloc
t=1  |..X.XX|      hops m/2 = 3 cells:  Φ(S) = rot₃(S),
t=2  |.XX..X|      period 1, verified over 3 full returns.
t=3  |..X.XX|      Mechanism: the rear pair's front law repeals
t=4  |.XX..X|      the one behind it while the solo law enacts
                   into the gap — the ring feeds the sunset wave
                   back into its own tail.
```

Rotors exist on **every even ring m ≥ 6** (base family: cells {0, 1, m/2+1},
hop m/2, period 1). None were found on odd rings or at m = 4 — complete ≤3-law
sweeps at m ≤ 7 and single-kind sweeps of all patterns up to 7 laws at m ≤ 14
turn up rotors only on even m ≥ 6. Larger even rings add richer classes — at
m = 10 a period-2 hop-5 and a period-3 rot-2 class; at m = 12 even a
**quarter-turn rotor** (period 1, rot 3 ≠ m/2). The m = 10 rot-2-per-3-steps
class is Expedition N-C's "legislative wave" (their Sunset Parliament,
`rings/RESULTS.md` §3, seen there as a period-15 cycle after 5 full laps at
speed 2/3): the two censuses agree; the m = 6 three-law hopper above is the
smallest moving law-packet known in nomodynamics. So *motion of law-packets is real in
nomodynamics* — it is specifically the infinite line, with its unrepealable
eldest law, that forbids it. Free gliders on ℤ: impossible. Rotors on rings:
abundant. The Front Law is exactly the statement of what the horizon does.

### 4.3 Reciprocal amendment: the minimal fixed-target escape, hunted

By Lemma 2 the smallest fixed-target semantics not covered by Theorem 1 is a
fixed-point-free permutation of kinds. Canonical instance (**reciprocal
amendment**, `reciprocal.py`): kinds are pairs (g, h) of chassis g, h ∈ T₀;
law (i,(g,h)) runs on g's guards and offset (a,b,c) and, when active, toggles
kind **(h, g)** at i + c — "I amend the law that amends me". Diagonal kinds
(g,g) reproduce own-kind nomodynamics exactly (conservative extension,
machine-checked on 400 random states); off-diagonal kinds are amended by a
*different* kind, so no anchor exists for them. Single-authorship still holds
(Lemma 2.2: φ is an involution), so parity ≡ OR — verified again by running
the whole hunt in lockstep duel mode. Kind space 729; slot space 5 × 729.

Theory first: the anchor is gone, but the linear obstruction of §3 survives in
sharpened form. For a mutual pair A = (g,h), B = (h,g) the coupled system is
x_A′ = x_A + σ^{c_h}(g_B·x_B), x_B′ = x_B + σ^{c_g}(g_A·x_A); in a uniformly-
enabled region the monodromy matrix M = [[1, σ^{c_h}],[σ^{c_g}, 1]] satisfies
**M² = (1 + σ^s)·I with s = c_g + c_h** (off-diagonals cancel over F₂), so a
period-p, displacement-d glider forces (1 + σ^s)^{p/2} = σ^d for even p, and
(1 + σ^s)^p = σ^{2d} for odd p, in F₂[σ, σ⁻¹] — impossible exactly as in §3
(and s = 0 gives M² = 0: uniformly-enabled mutual pairs annihilate within 2
steps — reciprocal amendment is self-consuming). Pairs decouple given
occupancy and diagonal kinds fall under §3, so the conclusion covers arbitrary
patterns.
**Theorem 3.** *No free glider exists in uniformly-enabled regions of the
reciprocal universe.* A reciprocal glider would need moving-guard
choreography; that regime is what the sweep probes:

Hunt results (`data/reciprocal_w1.json`): **complete** ≤2-law/5-cell stratum,
2,391,849 canonical seeds in parity/OR duel mode — fixed 1,740,675 · cycles
591,246 · big-growth 59,568 · extinct 360 · **0 gliders, 0 holdouts, 0
divergences**; plus 400,000 sampled 3-law seeds (of 3.94 × 10⁹) — cycle
133,629 · fixed 254,235 · big-growth 12,136 · again nothing else. New fauna
but no motion: mutual pairs support **longer legislative oscillators** than
own-kind W1 ever does from 2 laws (periods 6, 8, and 12 appear, vs {2, 4}) —
amendment cycles in the type graph become oscillation periods in time — yet
every packet stays anchored in place. The moving-guard escape, if it exists,
needs more than 3 reciprocal laws in 5 cells.

## 5. Machine certification (the rigorous sweeps)

All classifications carry certificates: extinct (S = ∅ observed), fixed /
cycle-p (exact configuration recurrence, displacement 0), glider (recurrence
with displacement d ≠ 0, then **re-verified by re-simulation over 3 further
periods** before being accepted), big-growth (size > 3000, or evidence-grade:
three consecutive 100-step blocks with strictly increasing block-minimum width
at width > 320 — a test no bounded-width pattern, hence no glider, can ever
trigger), slow-holdout (budget exhausted; every one individually re-run at 10×
budget). Budgets: 2000 steps/seed, recurrence-hash size cap 150, growth cutoff
3000. Engines validated against the founding `nomos2.py` engine (3000 random
states, exact match) and an independent naive per-law reference implementation
(W ∈ {1,2} × {parity, OR}, 600 random states each, exact match).

Per the mid-course Single-Author correction (from Expedition N-C): there are
no separate "OR sweeps" to run — Lemma 1 makes parity and OR one system. The
duel rows below are how that lemma is machine-certified across the census
(both engines advanced in lockstep, state equality asserted at every step of
every seed); the engineered strata (4-, 5-, 6-law) are coverage of the unique
own-kind dynamics, valid under both names; the budget freed by dropping
OR-specific hunts went into §4.1–§4.3 (supersession, rings, reciprocal).

### 5.1 Sweep inventory (generated by `make_tables.py` from `data/*.json`)

| sweep | seeds | extinct | fixed | cycle | glider | growth | holdout | diverg. | anomaly |
|---|---|---|---|---|---|---|---|---|---|
| W1 own-kind, ≤3 laws / 5 cells, COMPLETE, duel | 200,133 | 137 | 137,640 | 35,594 | **0** | 26,762 | 0 | **0** | 0 |
| W2 own-kind, ≤2 laws / 5 cells, COMPLETE, duel | 70,375 | 138 | 52,096 | 9,390 | **0** | 8,247 | 504 | **0** | 0 |
| W2 own-kind, 3 laws / 5 cells, sampled 10⁶, duel | 1,000,000 | 138 | 615,976 | 224,332 | **0** | 144,877 | 14,677 | **0** | 0 |
| W1 own-kind, 4 laws / 5 cells, COMPLETE | 7,873,740 | 380 | 4,980,060 | 1,637,795 | **0** | 1,255,505 | 0 | — | 0 |
| W1 own-kind, 5 laws / 6 cells, ≤4 kinds, sampled 5×10⁵ | 500,000 | 7 | 304,445 | 111,661 | **0** | 83,887 | 0 | — | 0 |
| W1 own-kind, 6 laws / 6 cells, ≤4 kinds, sampled 5×10⁵ | 500,000 | 1 | 293,266 | 113,339 | **0** | 93,394 | 0 | — | 0 |
| W1 SUPERSESSION, ≤3 laws / 5 cells, COMPLETE | 200,133 | 1,972 | 143,062 | 28,141 | **0** | 26,958 | 0 | — | 0 |
| W1 SUPERSESSION, 4 laws / 5 cells, sampled 5×10⁵ | 500,000 | 2,807 | 340,468 | 74,911 | **0** | 81,814 | 0 | — | 0 |
| W1 SUPERSESSION, 5 laws / 6 cells, sampled 5×10⁵ | 500,000 | 1,175 | 328,658 | 84,552 | **0** | 85,615 | 0 | — | 0 |
| W1 RECIPROCAL, ≤2 laws / 5 cells, COMPLETE, duel | 2,391,849 | 360 | 1,740,675 | 591,246 | **0** | 59,568 | 0 | **0** | 0 |
| W1 RECIPROCAL, 3 laws / 5 cells, sampled 4×10⁵, duel | 400,000 | 0 | 254,235 | 133,629 | **0** | 12,136 | 0 | **0** | 0 |
| RING ℤ/m own-kind, ≤2 laws, m=3..12 + 3 laws, m=3..7, COMPLETE | 1,133,775 | — | — | — | **18 rotors (m=6)** | — | 0 | — | 0 |

**14,136,230 line/variant classifications + 1,133,775 ring classifications ≈
15.3 million certified runs. Zero gliders. Zero parity/OR divergences. Zero
anomalies. The only moving packets in the whole census are the ring rotors —
exactly where the Anchor Theorem does not apply.**

Coverage notes (canonical seeds = translation-normalized, leftmost occupied
cell at position 0; raw counts, no reflection quotient):
- W1 5-cell strata are complete through 4 laws: 27 + 3,267 + 196,839 +
  7,873,740. The full ≤6-law/6-cell space is 1.589 × 10¹⁰ (k=5:
  5.269 × 10⁸, k=6: 1.535 × 10¹⁰) — infeasible as pre-registered; the 5- and
  6-law strata are covered by 10⁶ uniform samples restricted to ≤ 4 distinct
  kinds (the caterpillar shape).
- W2: complete through 2 laws (125 + 70,250); the 3-law space (19,786,500) is
  covered by a uniform distinct sample of 10⁶ = 5.05 % (rng 20260826).
- Supersession: complete ≤3 laws; 4-law stratum sampled 5 × 10⁵ = 6.35 %.
- Reciprocal: complete ≤2 laws (729 + 2,391,120 over 729 kinds); 3-law
  stratum (3.94 × 10⁹) sampled 4 × 10⁵.

### 5.2 Census notes (what the territory contains instead of gliders)

- **W1 own-kind, complete through 4 laws + 10⁶ sampled 5-6-law**: across all
  9.07 million seeds, **every cycle has period 2 or 4** (8,073,873 complete:
  p=2 × 1,657,351, p=4 × 16,038; the engineered 5-6-law samples add 225,000
  more, again all p ∈ {2,4}) and **no transient exceeds 7 steps**. Zero
  holdouts. Window-1 own-kind nomodynamics is temporally rigid: blink or
  freeze. The dominance of "fixed" is N-C's Dead Letter Theorem in action
  (all-blocked codes).
- **W2 opens new fauna**: complete ≤2 (70,375): periods 3, 6, 8 appear (odd
  periods absent from the entire W1 own-kind census); 504 slow-holdouts —
  resolved below. 3-law sample (10⁶): fixed 615,976 · cycle 224,332 (period
  spectrum {2, 3, 4, 6, 8, 12, 16, **24**}) · big-growth 144,877 · holdout
  14,677 (1.5 %) · extinct 138; transients reach 12. Specimen renders in
  `census_details.py` output: the 2-law period-3 pulse ((0,−2,2)@0 +
  (0,2,−1)@0), a 2-law period-8 breather.
- **Ruler fronts** (the holdout class, new specimen): bounded population
  (~8–32 laws) advancing on one side only, at density → 0, no recurrence in
  30,000 steps. Example (W2, 2 laws: (−2,−2,−2)@0 + (−2,−1,2)@2):

```
t=0   ..1.1......................    left edge pinned at 0 forever
t=8   ..1.1.........1                (the anchor, visible); right edge
t=16  ..1.1...........1              advances ~2 cells at epochs that
t=30  ..1.1...1.1...1.1...1.1        double — a binary-carry (Sierpinski-
t=32  ..1.1.....................1    gated) stutter of the masked linear
        ...                          recursion x' = x + σ²(g·x).  Extent 194
                                     by t=6,000; 579 by t=30,000.
```

  These are *extreme fronts*, not gliders: size stays bounded, but one edge is
  welded to the origin — the Anchor Theorem made flesh. They are also the 1-D
  cryptids pre-registration N6 asked about: aperiodic at every budget tried,
  for the identifiable reason that the pattern at time n encodes the binary
  carries of n.
- **Supersession fauna**: extinct 1,972/200,133 (≤3 laws) — 14× the own-kind
  rate (mutual annihilation is easy once laws can strike other kinds); and
  **odd periods exist at W=1** (period 3 from 3 laws, period 6 at 5 laws) —
  impossible anywhere in the 9-million-seed own-kind W1 census. Cross-kind
  effects change the period spectrum, not just the extinction rate. No
  holdouts; **no gliders**.
- **Reciprocal fauna**: see §4.3 — mutual 2-law pairs oscillate at periods up
  to 12 (own-kind W1 pairs never exceed 4); still no motion, no holdouts.
- **Deep holdout pass** (every slow-holdout re-run at 10× budget: 20,000
  steps, hash cap 400, growth cap 20,000): W2 ≤2-law — all 504 remain
  aperiodic; W2 3-law — 14,665/14,677 remain aperiodic, 12 resolve to
  big-growth. **None resolves to a cycle and none to a glider.** Edge
  instrumentation over 3,000 steps: 13,267/15,181 keep an occupancy edge
  pinned exactly at its seed position; the rest are double-ended specimens
  (two opposite-kind anchored fronts). The per-kind anchor invariant itself
  was checked separately along 56,000 + 4,000 trajectories: zero violations.
  Verdict: the ruler-front class is *permanently* frontal — bounded law
  population, unbounded aperiodic one-sided advance, no recurrence at any
  budget tried (one specimen hand-run to 30,000 steps).

### 5.3 Verification battery (all clean)

- Fast engines ≡ `nomos2.py` (3,000 random states) and ≡ naive per-law
  reference (600 × 4 configs); supersession and reciprocal engines
  smoke-tested against hand-traced orbits; reciprocal diagonal sub-universe
  ≡ own-kind engine (400 random states).
- Lockstep duels (parity vs OR advanced together, equality asserted every
  step of every seed): W1 ≤3 complete, W2 ≤2 complete, W2 3-law 10⁶,
  reciprocal ≤2 complete + 3-law sample — **0 divergences** anywhere.
- Actor-multiplicity instrument: max 1 per (target, kind) over 20,000 random
  dense states (Lemma 1); supersession clear-votes reach 3 (multi-authorship
  is real exactly where predicted).
- Anchor invariants (per-kind pinned edges, monotone c=0 supports, no kind
  rebirth) checked along 56,000 random trajectories × 300 steps (four
  engine configs) plus a 4,000-seed adversarial fuzz at 600 steps:
  **0 violations**.
- Glider verifier self-tested on a synthetic shift system; every ring rotor
  certificate re-verified over 3 full periods.

## 6. Verdict

**(ii), upgraded from conjecture to theorem — there is no first glider to
find.** The Front Law is proved: the Anchor Theorem covers parity, OR-toggle
(one and the same system — Lemma 1, independently found by N-C as the
Single-Author Lemma), every window, every dimension, every guard predicate,
every resolution satisfying H1–H3, and, via Lemma 2, the entire
fixed-single-targeting variant class. ≈ 15.3 million certified classifications
across four universes (own-kind W1/W2, supersession, reciprocal, rings)
produced **zero gliders, zero parity/OR divergences, zero anchor violations,
zero certificate anomalies**. Pre-registration N3 is refuted with mechanism;
N6 finds its 1-D cryptid in the ruler fronts — anchored, not moving.

> **The Front Law (foundational).** In nomic chains with own-kind fixed-offset
> amendment, all propagation is frontal: each kind's population is pinned at
> an unrepealable extremal law and can only extend away from it. *The eldest
> law cannot be repealed.*

Every hypothesis is certified load-bearing by a realized boundary phenomenon:
leave the infinite line and motion appears (**ring rotors** — 3 laws on ℤ/6,
the smallest moving law-packet in nomodynamics, family on every even m ≥ 6;
= N-C's legislative waves); keep the line but let laws amend other kinds and
the anchor dies — in **reciprocal amendment** single-authorship survives and
Theorem 3 still forbids uniformly-enabled gliders (2.79 M seeds: none), while
in **supersession** multi-authorship is real, parity ≠ OR from 2 placed laws
(the exact minimum), odd periods appear — and still no glider in 1.2 M seeds.

**Conjecture (cross-amendment no-go, evidence-grade).** 1-D supersession and
reciprocal nomodynamics at W = 1 admit no free glider — exhaustive below 4
laws in 5 cells (supersession) and 3 laws in 5 cells (reciprocal), sampled
well beyond, with every moving-guard mechanism observed so far reducing to
anchored fronts and pulses. Settling it — a monovariant that survives
cross-kind repeal, or a first cross-amendment glider — is the successor
charter. The question that opened this expedition is closed either way:

> **In 1-D nomic chains, all propagation is frontal.**
