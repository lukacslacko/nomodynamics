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

*(Post-hoc scoring of P1–P6 in §7.)*

---

*(Sections 1–11 below are written after the runs; this pre-registration is not
edited.)*

## 1. Verdict up front

**The successor charter is settled.** Both no-go conjectures of the predecessor
are now **theorems**, and the escape that nobody had hunted turns out to
contain the first free glider in the history of the program.

| escape (predecessor's lattice) | status before | **status now** |
|---|---|---|
| **E1 supersession** | conjecture, 1.2 M seeds | **THEOREM: no glider, ever** (§3, any dimension, any W, parity or OR) |
| **E2 permutation targeting** | conjecture, 2.79 M seeds, only L=2 hunted | **THEOREM: no glider, ever** (§2, all cycle lengths, any W, any dimension) |
| **E3 multi-target** | "riders provably glider-dead; fully-cross charted, never hunted" | **the riders claim is FALSE — glider exhibited** (§4). Out-degree ≥ 2 is the exact threshold. |

Three statements carry it. Write the **amendment digraph** `D` of a
constitution: one vertex per kind, and an edge `k → m` of weight `c_k` for
every `m ∈ T_k` (the kinds that an active kind-`k` law toggles). Then:

> **The Out-Degree Law (Theorem 2′ + Corollary 2.4).** If, restricted to the
> kinds the pattern actually uses, every law amends **at most one** kind, there
> is no free glider — for any offsets, any window, any dimension, parity or OR.
> This single statement contains own-kind nomodynamics (the Anchor Theorem),
> reciprocal amendment, every permutation constitution of every cycle length,
> and every non-permutation single-target constitution.

> **The Supersession No-Go (Theorem 3).** State-dependent targeting of the
> supersession kind — *enact your own kind on empty ground, clear the whole
> cell if occupied* — admits no free glider either, in any dimension. Its
> creation channel is own-kind, and that is enough: every present kind must
> push in the direction of travel, and then nothing can ever clear the
> rearmost cell.

> **The threshold is exact (§4).** With out-degree 2 a glider exists, and it
> is tiny: **two placed laws in a single cell, period 1, displacement 1** —
> the fastest a window-1 packet can possibly move, and the minimum at period 1.
> (The overall minimum is smaller still: **one placed law**, at period 2 —
> §4.2.) Cross-amendment motion is real; it costs exactly one extra target.

---

## 2. The tropical monovariant, and everything that follows from it

### 2.0 Setting

Kinds `K = {0..n−1}`. Kind `k` carries a rule `(a_k, b_k, c_k) ∈ (ℤ^D)³` and a
nonempty **target set** `T_k ⊆ K`. A state `S` is a finite set of placed laws
`(cell, kind)`; `occ_S(i)` says some law of some kind stands at `i`. A law
`(i,k) ∈ S` is **active** iff `occ(i+a_k) ∧ ¬occ(i+b_k)`. Every active law
emits one toggle of **every** kind in `T_k` at cell `i + c_k`. The toggle
multiset at a slot `(j,m)` is resolved by

- **parity** — the slot flips iff the count is odd, or
- **OR** — the slot flips iff the count is ≥ 1.

All that the proofs below use of the resolution rule is:

- **(R0)** a slot that receives no toggle is unchanged;
- **(R1)** a slot flips only if it received at least one toggle.

Parity, OR, and every threshold-≥1 rule satisfy both. A **free glider** is a
finite `S ≠ ∅` with `Φᵖ(S) = σᵈ(S)`, `p ≥ 1`, `d ≠ 0` (`v ≠ 0` in ℤ^D).

`supp_m(n)` is the cell support of kind `m` at time `n`; `α_m(n) = min supp_m(n)`
(`+∞` if empty), `β_m(n) = max supp_m(n)` (`−∞` if empty).

Throughout, `C` denotes the set of kinds **ever present** along the orbit, and
`D[C]` the sub-digraph of `D` induced on `C`. A subset `C′ ⊆ C` is
**predecessor-closed** if `m ∈ C′` and `k → m` in `D[C]` imply `k ∈ C′`.

### 2.1 The two structural lemmas

**Lemma S (support recursion).** `supp_m(n+1) ⊆ supp_m(n) ∪ ⋃_{k→m} (supp_k(n) + c_k)`.
*Proof.* If `(j,m)` is present at `n+1` but not at `n`, the slot flipped, so by
(R1) it received a toggle, necessarily emitted by an active law `(j − c_k, k)`
with `m ∈ T_k`; so `j ∈ supp_k(n) + c_k`. ∎

**Lemma R (repeal witness).** If `(j,m)` is present at `n` and absent at `n+1`,
then some `k` with `m ∈ T_k` has an **active** law at `j − c_k`. ∎ *(Same
argument, other direction.)*

**Lemma P (persistence).** If `C′ ⊆ C` is nonempty and predecessor-closed, then
along a glider orbit some kind of `C′` is present at **every** time.
*Proof.* By Lemma S, if every kind of `C′` is absent at time `n`, then for
`m ∈ C′` at time `n+1` every term of the union is empty (any `k → m` lies in
`C′` if it lies in `C`, and kinds outside `C` are never present), so `C′` is
absent at `n+1` — absence is absorbing. But `S_{n+p} = σᵈ(S_n)` makes presence
`p`-periodic, so a kind present once is present at arbitrarily late times.
Contradiction. ∎

### 2.2 The monovariant

**Lemma M.** Let `w : C → ℝ` satisfy `w_k − c_k ≤ w_m` for every edge `k → m`
of `D[C]` *(1-D; in ℤ^D read `c_k` as `⟨c_k, v⟩`)*. Put
`Ψ(n) = min{ α_m(n) + w_m : m ∈ C, supp_m(n) ≠ ∅ }`. Then

1. `Ψ(n+1) ≥ Ψ(n)`;
2. if `Ψ(n+1) > Ψ(n)`, then the **tight** subgraph
   `{k → m : w_k − c_k = w_m}` restricted to the argmin set `M(n)` contains a
   directed cycle — and every such cycle has `Σ c = 0`.

*Proof.* (1) Let `m` realise `Ψ(n+1)`. By Lemma S,
`α_m(n+1) ≥ min( α_m(n), min_{k→m}(α_k(n) + c_k) )`. The first branch gives
`α_m(n) + w_m ≥ Ψ(n)`; the second gives
`α_k(n) + c_k + w_m ≥ α_k(n) + w_k ≥ Ψ(n)` by the weight inequality.
(2) Suppose `Ψ(n+1) > Ψ(n)` and let `m ∈ M(n)`, i.e. `α_m(n) + w_m = Ψ(n)`.
Then `α_m(n+1) + w_m ≥ Ψ(n+1) > Ψ(n) = α_m(n) + w_m`, so `α_m(n+1) > α_m(n)`:
the law `(α_m(n), m)` was **repealed**. By Lemma R some `k → m` has an active
law at `α_m(n) − c_k`, so `α_k(n) ≤ α_m(n) − c_k` and `k ∈ C`. Hence
`Ψ(n) ≤ α_k(n) + w_k ≤ α_m(n) − c_k + w_k ≤ α_m(n) + w_m = Ψ(n)`, forcing
equality everywhere: `k ∈ M(n)`, the edge `k → m` is tight, and
`α_k(n) = α_m(n) − c_k`. So every vertex of the finite set `M(n)` has a tight
in-edge from inside `M(n)`; walking backwards must repeat, giving a tight
cycle. Summing `w_k − c_k = w_m` around a cycle, the source multiset and the
target multiset coincide, so `Σ w` cancels and `Σ c = 0`. ∎

**Lemma W (feasibility).** A `w` as in Lemma M exists iff every directed cycle
of `D[C]` has `Σ c ≥ 0`. More generally `w_k − c_k − μ ≤ w_m` is feasible iff
`μ ≥ −λ_min`, and the mirror system `v_m ≤ v_k − c_k + λ` (used on right edges
`β_m`) iff `λ ≥ λ_max`, where `λ_min`, `λ_max` are the minimum and maximum
**cycle means** `(Σ_{cyc} c)/|cyc|` of `D[C]`.
*Proof.* Difference constraints: feasible iff no cycle of positive total weight
in the derived graph; the derived cycle condition is exactly `Σ(c + μ) ≥ 0`
resp. `Σ(λ − c) ≥ 0`. (Shortest-path / Bellman–Ford potentials.) ∎

### 2.3 Theorem 1 — the Tropical Speed Law

> **Theorem 1.** For a glider of period `p` and displacement `d`, with
> `λ_min, λ_max` the extreme cycle means of `D[C]` (`+∞ / −∞` if acyclic):
> `p · min(λ_min, 0) ≤ d ≤ p · max(λ_max, 0)`.

*Proof.* Right side: take `v` for `λ = λ_max` (Lemma W) and
`Ξ(n) = max_m (β_m(n) + v_m)`. The mirror of Lemma S gives
`β_m(n+1) ≤ max(β_m(n), max_{k→m}(β_k(n)+c_k))`, so
`Ξ(n+1) ≤ Ξ(n) + max(λ_max, 0)`. Since `Ξ(n+p) = Ξ(n) + d`, `d ≤ p·max(λ_max,0)`.
Left side is the mirror with `Ψ` and `μ = −λ_min`. ∎

*Special cases.* If every cycle of `D[C]` has `Σ c ≥ 0` then `d ≥ 0`; if every
cycle has `Σ c ≤ 0` then `d ≤ 0`; if every cycle has `Σ c = 0`, or `D[C]` is
acyclic, then `d = 0` — no glider.

### 2.4 Theorem 2 — the Zero-Cycle Theorem

> **Theorem 2.** For a glider, **every** nonempty predecessor-closed
> `C′ ⊆ C` has the property that `D[C′]` contains a directed cycle of weight
> exactly `0`, **or** two directed cycles of strictly opposite sign.

*Proof.* Apply Lemmas M/W/P to `C′` (the recursion of Lemma S is closed on a
predecessor-closed set, and Lemma P keeps `Ψ` finite). If `D[C′]` is acyclic,
Theorem 1 gives `d = 0`. If every cycle has `Σ c > 0`, then `w` exists
(Lemma W) and no cycle can be tight, so by Lemma M(2) `Ψ` never strictly
increases; with `Ψ(n+1) ≥ Ψ(n)` it is constant, and `Ψ(n+p) = Ψ(n) + d` gives
`d = 0`. If every cycle has `Σ c < 0`, mirror with `Ξ`. The remaining
possibilities are exactly "some cycle `= 0`" or "cycles of both signs". ∎

> **Theorem 2′ (Unique-Cycle Corollary).** If some nonempty predecessor-closed
> `C′ ⊆ C` has **at most one** directed cycle, there is no glider.

*Proof.* Zero cycles: Theorem 1 (acyclic). One cycle of sum `s`: `s > 0` or
`s < 0` is killed by Theorem 2; `s = 0` makes `λ_min = λ_max = 0`, and
Theorem 1 gives `d = 0`. ∎

### 2.5 The Out-Degree Law — E2 dies, and so does everything single-target

> **Corollary 2.4 (Out-Degree Law).** If every kind `k ∈ C` has
> `|T_k ∩ C| ≤ 1` — every law amends at most one of the kinds actually in play
> — then there is no free glider. Any window `W`, any offsets, any dimension,
> parity or OR.

*Proof.* `D[C]` then has out-degree ≤ 1: a partial functional graph. Fix any
`m ∈ C` and let `C′` be the set of kinds that reach `m` in `D[C]`; it is
nonempty and predecessor-closed by construction. In a functional graph every
cycle is *terminal* for each of its vertices (the unique out-edge stays on the
cycle), so a cycle lies inside `C′` only if it passes through `m` — and there
is at most one such cycle. Theorem 2′ applies. ∎

Three published questions collapse into this one line:

- **own-kind nomodynamics** (`T_k = {k}`): each `{k}` is predecessor-closed with
  a single self-loop ⟹ no glider. *This re-proves Corollary 1 of the Anchor
  Theorem, and by a completely different route* — no extremal law is used, only
  the tropical potential.
- **E2 reciprocal amendment** (`φ` a 2-cycle) and **every permutation
  constitution of every cycle length `L`** ⟹ no glider. The `L = 3, 4, …`
  universes, never previously hunted, are dead on arrival.
- **every non-permutation fixed single-target constitution** ⟹ no glider,
  closing a gap the predecessor's Lemma 2 left implicit.

> **Corollary 2.5 (speed law for permutations).** Even before the strict
> argument, Theorem 1 already confines a hypothetical `L`-cycle glider: a
> single cycle gives `λ_min = λ_max = ρ_C = (Σ_{k∈C} c_k)/L`, so `d/p` lies
> between `0` and `ρ_C` and must carry `ρ_C`'s sign — and `ρ_C = 0` forces
> `d = 0` outright. Theorem 2 then removes the two remaining cases
> (`ρ_C > 0` and `ρ_C < 0`). (Pre-registered
> prediction **P2** — confirmed, and stronger than predicted: I expected the
> monovariant to leave the same-strict-sign case open, and the *tight-cycle*
> refinement of Lemma M(2) closes it.)

---

## 3. Theorem 3 — supersession admits no free glider (any dimension)

**Supersession (E1)**, the predecessor's canonical state-dependent targeting:
an active law of kind `k` at `i`, with target cell `j = i + c_k`,

- **enacts its own kind `k` at `j`** if `j` is empty, and
- **clears the whole cell `j`** (every kind standing there) if `j` is occupied;

clear-votes at one cell resolve by parity (`super`) or by OR (`super_or`).
This is the one place in the charted lattice where multi-authorship is real and
parity ≠ OR from two placed laws — and where 1.2 M seeds had found nothing.
Two facts, immediate from the definition, kill it outright.

**(F1) Creation is own-kind.** A kind-`m` law can appear at cell `j` at time
`n+1` only if `j` was empty at `n` and an active **kind-`m`** law stood at
`j − c_m`. Hence

  `supp_m(n+1) ⊆ supp_m(n) ∪ (supp_m(n) + c_m)`  for every kind `m`.

**(F2) An occupied cell only ever dies.** Enactments land only on cells empty
at time `n`, so a cell occupied at `n` either keeps its exact kind-mask at
`n+1` or is emptied; and it is emptied only if some **active law of some kind
`k`** stands at `j − c_k`.

*(Both are literal readings of the update; they are asserted as invariants in
the verification battery, §6.)*

> **Theorem 3.** On `ℤ^D`, for any finite kind set, any offsets `(a_k,b_k,c_k)`,
> any `W`, and either clear-resolution, supersession nomodynamics has **no free
> glider**.

*Proof.* Let `S` be a glider with period `p` and displacement `v ≠ 0`. By (F1)
no kind is ever born that was not already present, and a kind whose support
empties stays empty; with `S_{n+p} = σ^v(S_n)` this makes the present-kind set
`C` constant along the orbit, every `m ∈ C` present at every time. Write
`φ(x) = ⟨x, v⟩`.

**Step 1: `⟨c_m, v⟩ > 0` for every `m ∈ C`.** By (F1) every cell of
`supp_m(n+1)` lies in `supp_m(n) ∪ (supp_m(n) + c_m)`. If `⟨c_m,v⟩ ≤ 0`, then
`max φ` over `supp_m` is non-increasing in `n`; but the glider gives
`supp_m(n+p) = supp_m(n) + v`, so `max φ` grows by `|v|² > 0` every `p` steps.
Contradiction.

**Step 2: the rear level never moves.** Let `A(n) = min{ φ(x) : x` occupied at
`n }`. *(≥)* A cell occupied at `n+1` is either occupied at `n`, or (F1) newly
created at `j = i + c_m` with `i ∈ supp_m(n)`, whence
`φ(j) = φ(i) + ⟨c_m,v⟩ > A(n)` by Step 1. So `A(n+1) ≥ A(n)`. *(≤)* Take `x`
occupied at `n` with `φ(x) = A(n)`. By (F2) it survives unless some active law
of some kind `k` stands at `x − c_k`; that law is present, so `k ∈ C` and
`x − c_k` is occupied, giving `φ(x) − ⟨c_k,v⟩ ≥ A(n) = φ(x)`, i.e.
`⟨c_k,v⟩ ≤ 0` — contradicting Step 1. So `x` survives and `A(n+1) ≤ A(n)`.

Hence `A` is constant. But the glider forces `A(n+p) = A(n) + |v|² > A(n)`.
Contradiction. ∎

**Remarks.**

- The proof never touches the resolution rule, so it covers parity clears, OR
  clears, and any other way of adjudicating clear-votes. It never touches the
  guards, so it holds for *any* activity predicate whatsoever. And it never
  touches `D = 1`, so 2-D supersession is dead too.
- It is *not* the Anchor Theorem. The anchor argument fails here — cross-kind
  clearing really does repeal other kinds' eldest laws, exactly as the
  predecessor said. What survives is weaker and sufficient: **the creation
  channel is own-kind even though the destruction channel is not.** Motion
  needs every kind to push forward (Step 1); once every kind pushes forward,
  the rear cell has no possible executioner (Step 2). Supersession gives laws
  the power to repeal each other but not the power to repeal each other
  *backwards*.
- **Corollary (no `c = 0` kind in any moving supersession pattern).** A kind
  with `c_m = 0` targets its own occupied cell, so it can only ever clear and
  never enact: `supp_m` is monotonically non-increasing, and such a kind can
  belong to no glider. This kills the one mechanism I had pre-registered
  (**P1**) as supersession's best hope — a self-clearing tail — because the
  self-clearing kind can never be re-created ahead of the packet.

---

## 4. E3 — the first free glider in nomodynamics

### 4.1 The refuted claim

The predecessor charted E3 (multi-target laws, out-degree ≥ 2) and split it in
two, ruling one half out a priori:

> *"If each law still toggles its own kind among its targets ("riders"), the
> class is **provably glider-dead**: every kind remains its own sole author,
> Theorem 1 applies kind-wise …"* — `glider-question/RESULTS.md` §4, Lemma 2.

**This is false, and the error is a quantifier slip.** "Each law toggles its
own kind among its targets" does *not* imply "each kind is toggled only by its
own laws". If `T_0 = {0,1}`, then kind 1 has two authors — kind 1's law at
`j − c_1` *and* kind 0's law at `j − c_0`. Hypothesis (H1) of the Anchor
Theorem fails, and with it the whole no-go. The riders class is the *easiest*
place in the whole lattice to build a glider.

### 4.2 TANDEM-1 — the minimal specimen

```
kinds     n = 2,  W = 1
rules     kind A = (a,b,c) = (0, −1,  1)      "I stand and my left is vacant"
          kind B = (a,b,c) = (0, −1,  0)
targets   T_A = {A,B}     T_B = {A,B}         (both laws amend both kinds)
seed      one cell holding BOTH kinds:  xnomos.state_of([(1,0),(1,1)])
period    p = 1        displacement d = +1        speed 1 (the maximum)
```

```
t=0   .#.......        # = a cell carrying both kinds
t=1   ..#......
t=2   ...#.....        Phi(S) = sigma^1(S) exactly, from t = 0 on.
t=3   ....#....
```

**Mechanism.** Both laws are active (each stands on an occupied cell whose
left neighbour is vacant). `A`, with `c = +1`, toggles *both* kinds at the
empty cell ahead — enacting the pair one step forward. `B`, with `c = 0`,
toggles *both* kinds at its own cell — repealing the pair where it stands.
Net effect: the two-law bloc relocates one cell to the right, forever.

This is exactly the "caterpillar" the predecessor proved impossible
(*Corollary 3: "no choreography of other kinds, guards, or occupancy can ever
repeal it — the caterpillar drags an immortal tail"*). The corollary is right
about own-kind amendment and wrong about the general case: **the tail is
repealed by the head's partner, not by its own kind.** `B` is the sunset
clause that repeals both statutes; `A` is the enacting clause that re-enacts
both one cell on. Neither law can move alone — each is anchored by Theorem 2′
in isolation — but the pair glides.

**Minimality — corrected.** *My first draft of this paragraph claimed "two
placed laws is the absolute floor … no one-law glider exists in any
fixed-target semantics". That is **false**, and the sub-expedition refuted it
with a certified witness. The argument I gave only rules out `p = 1`; over a
longer period the other kinds it creates can come back and repeal it. The
record is kept and corrected:*

> **Correct statement.** No one-law state is a **period-1** glider: with
> `S = {(i,k)}` the only emission is at `i + c_k`, so removing `(i,k)` needs
> `k ∈ T_k` and `c_k = 0`, which puts the whole next state back at cell `i`,
> forcing `d = 0`. Hence TANDEM-1 is the **minimal period-1 glider**, and two
> placed laws is the floor *at period 1*.

> **The true floor is ONE placed law, at period 2** (certified,
> `verify_glider` in both resolutions, `xnomos.classify` = GLIDER p=2 d=+1):
> ```
> n = 3   rules [(0,1,0), (0,1,1), (0,1,0)]   T = [{1,2}, {0}, {0}]
> seed  a single law of kind 0            p = 2   d = +1   speed 1/2
> t=0 .A...    the lone kind-0 law enacts kinds 1 and 2 on its own cell;
> t=1 .#...    they in turn re-enact kind 0 one cell right and clear the pair.
> t=2 ..A..
> ```
> Note this specimen is also **fully cross** (`k ∉ T_k` for every `k`) — the
> smallest glider found anywhere in this expedition.

TANDEM-1 still attains the maximum speed `|d|/p ≤ W`.

### 4.3 The DRIFTER family — sub-unit speeds need a third kind

At `n = 2, W = 1` the only realisable speed is `1` (§4.6 table: every
`d/p ≠ 1` is UNSAT up to `p = 7`, `N = 14`, complete over all constitutions).
A third kind buys slowness. All certified (`xnomos.verify_glider`, 3 periods):

```
DRIFTER-1/2   n=3  rules [(0,−1,0), (0,−1,0), (0,1,1)]   T=[{0,2},{0,1},{0,1}]
              seed {cell 1: kinds 0,1}          p=2  d=1
   t=0 .#....     the bloc waits one step, then hops:
   t=1 .#....     Phi is not a translation on its own —
   t=2 ..#...     only Phi^2 is.
   t=3 ..#...
   t=4 ...#..

DRIFTER-1/3   n=3  rules [(−1,1,−1), (0,−1,1), (0,−1,0)]  T=[{0,2},{0,1},{1,2}]
              seed {cell 1: kinds 0,1}          p=3  d=1
   t=0 .#.....    it breathes: one cell, two cells, one cell, then hops.
   t=1 .##....
   t=2 .#.....
   t=3 ..#....

DRIFTER-1/4   n=3  rules [(0,−1,1), (0,−1,0), (−1,1,−1)]  T=[{1,2},{0,1,2},{1,2}]
              seed {cell 1: kind 0}             p=4  d=1
   t=0 .A......   a four-phase gait: A -> A# -> # -> # -> A
   t=1 .A#.....
   t=2 .#......
   t=3 ..#.....
   t=4 ..A.....

DRIFTER-1/5   n=3  rules [(0,−1,1), (1,−1,0), (0,1,0)]    T=[{0,2},{0,2},{0,1,2}]
              seed {1:7, 5:7, 8:2, 9:7, 13:5}   p=5  d=1   (a 5-cell convoy)
```

Every DRIFTER has a frame that is **not** a translate of its seed: these are
genuinely phase-changing gliders, not rigid blocks in disguise.

### 4.4 TRIPTYCH — a glider that exists under parity and *not* under OR

The predecessor's Single-Author Lemma made the parity/OR axis vacuous for
own-kind dynamics, and E1 supersession was the only place it was known to
awaken. It awakens in E3 too, and this time *inside the glider phenomenon*:

```
kinds     n = 3,  W = 1
rules     [(0, 1, 0), (0, −1, 1), (0, 1, −1)]
targets   T_0 = T_1 = T_2 = {0,1,2}          (every law amends every kind)
seed      cells 1, 2, 4, each carrying ALL THREE kinds
period    p = 1   displacement d = +1

parity                       OR
t=0  .##.#...                t=0  .##.#...
t=1  ..##.#..     glider     t=1  ...#.#..     diverges at t = 1
t=2  ...##.#.                t=2  ..#.#.#.
```

Machine-measured author multiplicity along this orbit: **2** — two distinct
kinds' laws toggle the same slot in the same step, and the parity cancellation
is load-bearing. (Own-kind nomodynamics can never exceed 1: Single-Author
Lemma.) `xnomos.verify_glider(..., 'parity')` = True over 3 periods and an
independent reference implementation confirms 15; `verify_glider(..., 'or')`
= False. **The resolution axis is not a bookkeeping convention in E3 — it
decides whether the object moves.**

### 4.5 How sharp is the theory? A complete classification at n = 2

Theorems 1/2/2′ give a *necessary* condition on the pair (amendment digraph
`D`, offset vector `c`). `sharpness.py` decides — exactly, by SAT, with the
guards `(a_k,b_k)` left free for the solver — **every** such pair at `n = 2`,
`W = 1`: 9 target matrices × 9 offset vectors = **81 universes, complete
enumeration**, `p ≤ 6`, `N = 14`, both displacement signs.

| | count |
|---|---|
| universes where a glider exists (SAT, certified) | **6** |
| theory and machine agree | 73 / 81 |
| **glider exists where the theorems forbid one** | **0** |
| theory permits, but the box contains no glider | 8 |

The six are exactly:

```
T = [{0,1},{0,1}]   c = (0,1) (1,0) (1,−1) (−1,1) (0,−1) (−1,0)     p = 1, |d| = 1
```

> **Classification (n = 2, W = 1, complete).** A two-kind window-1
> cross-amendment universe admits a free glider **iff both laws amend both
> kinds and `c_0 ≠ c_1`** — and then the glider is TANDEM-1, period 1, speed 1.
> Every other one of the 81 universes is glider-free (exactly, `p ≤ 6`).

That criterion is *precisely* what Theorem 2 predicts here: with `T` full, the
digraph is complete-with-self-loops, its cycles include the two self-loops of
weights `c_0` and `c_1`, and "a zero cycle or two cycles of opposite sign"
reads exactly `c_0 = 0` or `c_1 = 0` or `c_0 c_1 < 0` — i.e. `c_0 ≠ c_1`. So
**at `n = 2` the necessary condition is also sufficient**; the 8 residual gaps
are all asymmetric target matrices (`T = [{1},{0,1}]` and its relatives), where
the theory permits and the machine finds nothing.

### 4.6 The speed spectrum — corrected: it is the DISPLACEMENT that is quantised

*My first draft of this section claimed "`2/3` needs a fourth kind". That is
**wrong**, and the sub-expedition refuted it with a certified `n = 3` witness
(re-verified here by `xnomos.verify_glider` in both resolutions):*

```
rules [(0,−1,1), (0,1,1), (0,1,0)]   T = [{0,1}, {2}, {0,1,2}]
seed  {cell 0: kinds 0,1,2 ; cell 3: kind 2}      p = 3   d = +2
t=0 .#..C...     out-degrees (2, 1, 3) — kind 1 has only ONE target
t=1 ..#.#...
t=2 ...###..     verify_glider(p=3,d=2) = True, parity AND or
t=3 ...#..C.
```

*The error was in my search, not the machine: I had imposed out-degree ≥ 2 on
**every** kind, which excludes this constitution. Under that restriction the
original claim does hold — `p=3, d=2` is UNSAT for all 64 all-out-degree-≥2
`n = 3` target matrices — but that restriction was mine, not the question's.*

The corrected picture is sharper and more interesting. Complete over all
constitutions, `W = 1`, free targets, both signs of `d`, coprime `(p,d)`,
`p ≤ 8`:

| kinds | realisable speeds `|d|/p` | not realisable |
|---|---|---|
| n = 2 | **1 only** | every other coprime `d/p`, `p ≤ 8` |
| n = 3 | 1, 2/3, 1/2, 2/5, 1/3, 2/7, 1/4, 1/5, 1/6, 1/8 | 3/4, 3/5, 4/5, 5/6, 3/7, 4/7, 5/7, 6/7, 3/8, 5/8, 7/8 |
| n = 4, 5 | all of the above **and** every `|d| ≥ 3` case that `n = 3` refuses | — |

Read the middle column again: at `n = 3` the missing speeds are exactly those
with **numerator ≥ 3**. What is quantised is not the *speed* but the
**displacement per period**:

I first wrote this up as a conjecture — *"`|d| ≤ (n−1)·W` for coprime
`(p,d)`"* — and then **refuted it myself** before publishing. Deciding
`(p,d) = (3,2), (4,3), (5,4), (6,5), (7,6)` exactly, free targets, `N = 16`,
both signs of `d`:

| kinds | 2/3 | 3/4 | 4/5 | 5/6 | 6/7 |
|---|---|---|---|---|---|
| n = 2 | no | no | no | no | no |
| n = 3 | **YES** | no | no | no | no |
| n = 4 | **YES** | **YES** | **YES** | **YES** | **YES** |
| n = 5 | **YES** | **YES** | **YES** | **YES** | **YES** |

So the cap is real but it does **not** grow like `n − 1`: it is `1` at two
kinds, `2` at three kinds, and then **vanishes at four**, where every coprime
`(p,d)` tested is realisable. The honest statement:

> **Fact (complete SAT decision, `W = 1`).** `n = 2` realises only speed 1;
> `n = 3` realises exactly the coprime `(p,d)` with `|d| ≤ 2` (`p ≤ 8`);
> `n ≥ 4` realises every coprime `(p,d)` tested (`p ≤ 7`).

The trivial bound is `|d|/p ≤ W`; Theorem 1 sharpens it to the maximum cycle
mean of `D[C]`. **Neither involves the number of kinds at all.** Why two and
three kinds cap the displacement at 1 and 2, and why the cap disappears
entirely at four, is the sharpest question the expedition leaves open.

---

### 4.7 The same test at n = 3 — 9,261 universes, complete

`sharpness.py 3 12 3 parity`: all 343 target matrices × 27 offset vectors,
guards free, `p ≤ 3`, `N = 12`, both signs of `d`.

| | count |
|---|---|
| universes decided | **9,261 (complete enumeration)** |
| glider exists (SAT, auto-certified) | 1,800 (19.4 %) |
| theory and machine agree | 7,035 |
| **glider exists where the theorems forbid one** | **0** |
| theory permits, no glider at `p ≤ 3` in this box | 2,226 |

**Zero violations across 9,342 completely decided universes** (n = 2 and n = 3
together), with the guards quantified over as well. The theorems of §2 have
been tested against the machine on every constitution shape available at
`n ≤ 3, W = 1`, and they hold.

A structural confirmation worth naming: universes like
`T = [{0}, {1,2}, {1,2}]` glide even though kind 0 has out-degree 1 — the
glider simply *does not use kind 0*. That is exactly what the Out-Degree Law
predicts: `{0}` is predecessor-closed with a single self-loop, so no glider may
contain kind 0, while `{1,2}` is rich enough to carry one. The condition is
about the kinds in play, not about the constitution as a whole.

### 4.8 TANDEM-1 lifts — 2-D at any velocity, and every ring

The construction is dimension- and topology-agnostic; only the pair
(*enact one step along `v`*, *repeal in place*) matters.

```
2-D:   rules [ ((0,0), (−1,0), v), ((0,0), (−1,0), (0,0)) ],  T = [{0,1},{0,1}]
       seed = one cell carrying both kinds
       v = (1,0)  -> GLIDER      v = (1,1) -> GLIDER      v = (2,1) -> GLIDER
```

All three certified by `xnomos.verify_glider` in dim 2. A **knight-move
glider** `(2,1)` exists at `W = 2`. So in 2-D cross-amendment nomodynamics the
achievable velocity set contains *every* vector `v` with `‖v‖_∞ ≤ W` — the
diagonal-relay contortions of the own-kind theory are unnecessary.

```
rings:  TANDEM-1 with rules [(0,−1,1), (0,−1,0)] on Z/m rotates one cell per
        step, verified for 3 full laps, on m = 3, 4, 5, 6, 7 — EVERY ring.
```

Compare the predecessor's own-kind census: rotors exist **only on even rings
`m ≥ 6`**, none on odd `m` or at `m = 4` (complete ≤3-law sweeps at `m ≤ 7`).
Cross-amendment erases that arithmetic restriction entirely. The even-`m ≥ 6`
condition was never about rings; it was about own-kind amendment.

### 4.9 Theorem 4 — an existence theorem, and the second minimal family

> **Theorem 4 (Existence).** Fix any dimension `D`, any `v ∈ ℤ^D`, `v ≠ 0`, and
> any `u ≠ 0`. The two-kind constitution
> `rules = [(0, u, v), (0, u, 0)]`, `T_A = T_B = {A,B}`
> has, as a free glider of period 1 and displacement `v`, the single cell
> carrying both kinds. Parity and OR agree on it.

*Proof.* Let `S = {i₀ : {A,B}}`. Each placed law sits on an occupied cell, so
`occ(i₀ + 0) = 1`; and `occ(i₀ + u) = 0` because `u ≠ 0` and `i₀` is the only
occupied cell. Both laws are therefore active. `A` emits a toggle of *both*
kinds at `i₀ + v`; `B` emits a toggle of *both* kinds at `i₀`. Since `v ≠ 0`
the two target cells are distinct, so every slot receives exactly one toggle
and parity ≡ OR. Slot-wise: `(i₀, A)` and `(i₀, B)` flip off; `(i₀+v, A)` and
`(i₀+v, B)` flip on. Hence `Φ(S) = σ^v(S)`, and the argument repeats. ∎

So **cross-amendment gliders exist at every velocity, in every dimension, at
the minimum possible size (2 placed laws) and the maximum possible speed.**
The obstruction the predecessor found was not about geometry at all; it was
about out-degree.

**DOUBLET — the caterpillar, realised.** The other minimal family found by the
complete `n = 2` classification is genuinely two-celled and is exactly the
"caterpillar" that `glider-question/RESULTS.md` Corollary 3 declared void
a priori:

```
kinds     n = 2,  W = 1
rules     kind A = (1, −1,  1)         kind B = (0, −1, −1)
targets   T_A = T_B = {A,B}
seed      TWO adjacent cells, each carrying both kinds: {2:{A,B}, 3:{A,B}}
period    p = 1     displacement d = −1

t=0   ..##...        Only the two "end" laws fire:
t=1   .##....          B at the leading (left) cell enacts the pair one
t=2   ##.....          cell further left;
t=3   #......          A at that same cell repeals the pair at the trailing
                       (right) end.  Head advances, tail is repealed — by the
                       other kind.  A caterpillar exactly as designed.
```

`verify_glider(p=1, d=−1)` = True. Corollary 3 of the predecessor is correct
for own-kind amendment and false in general: *"no choreography of other kinds
… can ever repeal it"* fails the moment a law may amend a kind other than its
own, because then "the other kinds" are precisely the executioners.

---

## 5. The instrument: an exact bounded encoding of the question

`xsat.py` does not simulate seeds. It encodes the **question**, with variables
for the seed *and* for the constitution — the offsets `a_k, b_k, c_k` as
one-hot trits and the amendment target matrix `T` as free Booleans — unrolls
`p` steps of the exact update, and asserts `Φᵖ(S) = σᵈ(S)`, `S ≠ ∅`, `d ≠ 0`.
One UNSAT therefore decides **every constitution in the class at once**.

**Why the bounded model is exact for ℤ.** We model cells `0..N−1` and force the
`W` outermost cells on each side to be empty of every kind **at every time**
`t = 0..p`. Then (i) every law sits in `[W, N−1−W]`, so its guard reads
`i ± W` and its emission `i + c` land inside the model — no rule is truncated;
and (ii) a toggle landing in the margin would *create* a law there (a toggle
into an empty slot is an enactment), contradicting the forcing. So the solver
is compelled to reproduce the true ℤ-dynamics of any pattern whose whole
trajectory fits in the interior, and

> **UNSAT ⟹ no glider of period `p`, displacement `d`, over ANY constitution
> in the class, whose `t = 0..p` trajectory spans at most `N − 2W` cells.**

Translation symmetry is broken exactly and losslessly by forcing the
**leftmost cell ever occupied** during `t = 0..p` to be cell `W`. Reflection
`i ↦ −i` maps the class to itself (`(a,b,c) ↦ (−a,−b,−c)`, targets unchanged)
and `d ↦ −d`, so quantifying over all constitutions makes `d > 0` WLOG; where
a *classification* rather than a no-go is claimed (§4.5, §4.6) both signs of
`d` were searched explicitly. `d` itself is a variable (one-hot over
`1..pW`), so one job decides a whole period at once; `|d| ≤ pW` because a
single step moves either edge by at most `W`.

**The bug this caught.** The first version constrained only
`x[p][j] ↔ x[0][j−d]` for `j` in range, silently letting laws that shift out of
the window vanish. It produced a "glider" within seconds; `xnomos.verify_glider`
rejected it, and the encoder was fixed (the forward direction
`x[0][i] = 0` whenever `i + d` leaves the box is now asserted too). Every SAT
model is now auto-certified inside `xsat.solve`, which **raises** if xnomos
disagrees. Note that the bug could only ever produce *spurious SAT*: a genuine
glider satisfies the weaker constraint too, so no UNSAT was ever at risk.

---

## 6. Verification battery

Nothing in this report is cited from an uncertified run.

**A. Encoder fidelity (`validate.py`).**
- **T1** — constitution *and* seed pinned inside the CNF; unit propagation then
  *computes* the trajectory, which is compared to `xnomos.step` frame by frame,
  cell by cell, kind by kind. Random universes over `n ∈ {1..3}`,
  `W ∈ {1,2}`, all four modes (`parity`, `or`, `super`, `super_or`), ℤ and
  rings. The instance is additionally re-solved with the found trajectory
  blocked, asserting the trajectory is *uniquely determined* by seed +
  constitution. **1,200 trials: 0 mismatches.**
- **T1-exactness** — universes whose true ℤ-trajectory leaves the interior must
  be **refused** by the bounded model (otherwise UNSAT would not be a ℤ no-go).
  Every one of them was refused.
- **T2** — completeness on published specimens: with the constitution left
  free, the instrument **finds** the ℤ/6 ring rotor from scratch and returns
  rule `(0,1,−1)` at cells `{0,2,3}` — a rotation of the published `{1,2,5}`
  specimen — re-verified by `xnomos`; it also reproduces the published rotor
  when pinned, and finds genuine period-2, -3 and -4 oscillators (non-fixed,
  prime period asserted), each re-verified by `xnomos`.
- **T3** — own-kind targeting on ℤ comes back UNSAT for every `(n,p,d)` tried,
  agreeing with the Anchor Theorem it knows nothing about.

**B. Theorem invariants (`invariants.py`).** Adversarial fuzz over random
constitutions and trajectories, `n ∈ {1..5}`, `W ∈ {1,2,3}`, all four modes,
asserting at every step the exact facts the proofs of §2–§3 use:

| invariant | what it underwrites | violations |
|---|---|---|
| Lemma S — support recursion | Theorems 1, 2 | **0** |
| Lemma R — repeal witness | Lemma M(2), the tight-cycle refinement | **0** |
| Lemma M — `Ψ` non-decreasing whenever a feasible weighting exists | Theorem 1 | **0** |
| Lemma M2 — a strict rise of `Ψ` forces a tight cycle | Theorem 2 | **0** |
| F1 — supersession creation is own-kind | Theorem 3, Step 1 | **0** |
| F2 — an occupied cell keeps its mask or empties | Theorem 3, Step 2 | **0** |
| F3 — a cleared cell has an active author at `j − c_k` | Theorem 3, Step 2 | **0** |
| F0 — a `c = 0` kind has non-increasing support | §3 corollary | **0** |

**20,000 random trajectories / 267,201 steps**: 267,201 checks each of Lemma S
and of Lemma R (F3 under supersession), 60,235 of Lemma M, 120 of the rare
Lemma M2 event (a strict rise of `Ψ`, the crux of Theorem 2), 133,378 each of
F0/F1/F2. Plus **23,821** checks of the Twin-Kind Lemma (§8.5). **Zero
violations of anything.**

*(The fuzzer earned its keep: it rejected a first draft of the Lemma R check
that had been applied to supersession, where removal is cross-kind by design —
a scoping error in the test, and a useful reminder that Lemma R is a statement
about fixed-target semantics only.)*

**C. Specimen certificates.** Every glider in §4 is confirmed by **three
independent code paths**: the SAT model itself, `xnomos.verify_glider` over 3
full periods, and a reference `step()` written directly from the specification
in this report (TANDEM-1 over 12 periods, TRIPTYCH over 15). TRIPTYCH's
parity/OR split was measured on both engines, and its author multiplicity
(= 2) instrumented directly.

## 7. Pre-registration scorecard

| # | prediction | outcome |
|---|---|---|
| **P1** | E1 supersession most likely (0.45); E3 second (0.30); E2 least (0.15). P(some glider) = 0.55. | **Ranking inverted.** E1 is *provably* dead — and dead by exactly the mechanism I nominated for it: the `c = 0` self-clearing kind can never be re-created, so it cannot ride along (§3 corollary). E3, which I ranked second, was the answer, and it was *easy* — the first SAT call in the campaign returned a certified glider in 0.04 s. The 0.55 was, by luck, on the right side. |
| **P2** | Weighted tropical monovariant exists iff every φ-cycle has `Σc ≥ 0`; yields a cycle speed law; `ρ_C = 0 ⟹ no glider`; **will not close E2**. | **Confirmed and exceeded.** The monovariant is exactly as predicted (Lemma W), and the speed law is Theorem 1. The last clause is **refuted, in my favour**: the tight-cycle refinement (Lemma M(2)) *does* close E2, and in fact closes every out-degree-≤1 semantics at once. I under-predicted my own tool. |
| **P3** | The uniformly-enabled 𝔽₂ obstruction generalises from `L = 2` to every cycle length via a norm argument. | **Confirmed** (§8 note): `(1+N)^p = σ^d` in `𝔽₂[σ^{±1}][N]/(N^L − σ^s)` has norm `(1+σ^s)^p = σ^{dL}`, impossible. It is now redundant — Theorem 2′ is unconditional, so no enabled-region hypothesis is needed — but the prediction was right. |
| **P4** | UNSAT everywhere reachable, "unless P1's supersession guess is right, witness at 4–6 laws, `p ≤ 6`". | **Half right.** UNSAT everywhere in E1 and E2 (1,328+ bounded questions, §9 table). The witness appeared not in supersession but in E3, and at **2 laws, `p = 1`** — smaller and faster than I allowed for. |
| **P5** | Rakes/puffers absent under E2, **present** under E1 supersession; and at least one bounded one-sided advancing front somewhere in the cross-amendment universes. | **Right about E2, wrong about E1, right about the phenomenon.** Both E2 *and* supersession are empty of them — an independent front-window detector that never uses the `Φᵖ = σᵈ` test found **zero** bounded moving packets in either (§9.6). But the phenomenon is real, in the escape I had ranked second: the **PICKET PUFFER** (§9.6), an E3 two-law engine translating at speed 1 with a `p = 4` periodic front, laying a periodic `###.` wake, population growing 1.507 laws/step, tail welded to the origin forever. I predicted the object and put it in the wrong universe. |
| **P6** | "If I am refuted, I expect it to be here: I expect E2 to be provably glider-free and the proof to be the monovariant." | **Not refuted** — E2 is provably glider-free and the proof is the monovariant. The thing I did not anticipate at all is that the *same* monovariant would also settle every non-permutation single-target semantics, and that the surviving escape would be the one the predecessor had marked "provably dead". |

**Honest summary of the calibration.** I was well calibrated on the
mathematics and badly calibrated on the difficulty. I budgeted the expedition
for a long hunt and a partial theorem; instead the theorem came out complete
and the glider fell out of the instrument's first call. The single most useful
methodological lesson: **the predecessor's one *unproved-but-asserted* claim
(riders are glider-dead) was where the answer was hiding.** A search program
that had taken that claim at face value — as the 3 M-seed campaigns did, by
never sampling multi-target constitutions — could not have found this object
at any scale.

---

## 8. Further notes and structure theory

### 8.1 The 𝔽₂ obstruction, generalised to every cycle length (P3)

The predecessor proved (§4.3) that for a *reciprocal pair* the monodromy in a
uniformly-enabled region satisfies `M² = (1 + σ^s)·I`, `s = c_g + c_h`, killing
enabled-region gliders. That generalises to every cycle length.

Let the permutation cycle be `0 → 1 → … → L−1 → 0` with `t(k) = k+1`. In a
uniformly-enabled stretch the per-kind indicator fields obey
`x_{k+1}′ = x_{k+1} + σ^{c_k} x_k`, i.e. `M = I + N` where `N` is the weighted
cyclic shift sending slot `k` to slot `k+1` with factor `σ^{c_k}`. Then
`N^L = σ^s · I` with `s = Σ_k c_k`, so `M` lives in
`R = 𝔽₂[σ^{±1}][u]/(u^L − σ^s)`. A period-`p`, displacement-`d` glider would
force `(1+u)^p = σ^d` in `R`. Take the norm down to `𝔽₂[σ^{±1}]`:
`N(1+u) = Res_u(u^L − σ^s, 1+u) = 1 + σ^s`, and `N(σ^d) = σ^{dL}`, so

  `(1 + σ^s)^p = σ^{dL}`  in `𝔽₂[σ, σ⁻¹]`.

If `s ≠ 0`, `(1+σ^s)^p` has `2^{s₂(p)} ≥ 2` monomials (Lucas) while `σ^{dL}`
has one; if `s = 0`, `(1+1)^p = 0`. Either way, impossible. **No uniformly
enabled E2 glider exists at any cycle length.** Theorem 2′ now supersedes this
(it needs no enabled-region hypothesis), but the two agree, and the linear
picture explains *where* a glider would have had to live — exactly at the guard
boundary, as in Life. In E3 that is precisely where TANDEM-1 does live: its
guard `¬occ(i+u)` is false the instant a second cell appears behind it, which
is what stops the wake from growing.

### 8.2 Why the resolution axis matters again

The predecessor's Single-Author Lemma made parity ≡ OR identically for
own-kind dynamics, and Lemma 2.2 extended that to all fixed *single*-targeting
(φ a bijection ⟹ one author per slot). Supersession was the only known place
where the axis reopened. E3 reopens it too, and harder: with out-degree ≥ 2 a
slot `(j,m)` has one potential author per kind `k` with `m ∈ T_k`, so
multiplicity up to `n`. TRIPTYCH (§4.4) is a glider under parity whose OR
trajectory diverges at the first step. So:

> In multi-target nomodynamics, **"an odd number of amendments" and "at least
> one amendment" are not merely different bookkeeping — they disagree about
> whether law-packets can travel.**

### 8.3 The necessary condition is NOT sufficient beyond n = 2

At `n = 2` the Zero-Cycle condition is exactly sufficient (§4.5). At `n = 3`,
2,226 of the 9,261 universes are permitted by the theory but contain no glider
at `p ≤ 3`. Are those box artifacts? **No.** A uniform sample of 60 of the
4,026 theory-permitted `(T, c)` pairs at `n = 3` was re-decided out to
`p ≤ 8`, `N = 16` (interior 14 cells), both signs of `d`: **0 of the 60 gained
a glider beyond `p ≤ 3`.** (SAMPLE, rng seed 7; the `p ≤ 3` layer itself is a
COMPLETE enumeration.)

So the gap is real: `D[C]` having a zero cycle or cycles of both signs is
necessary and, from three kinds up, not sufficient. Something about the
*guards* — which the tropical argument deliberately throws away, since Lemmas
S and R hold for any activity predicate — must enter a sharp characterisation.

### 8.4 Fully-cross multi-target — "charted, never hunted", now populated

The predecessor's E3 had two halves: "riders" (some law toggles its own kind),
declared dead — refuted in §4 — and **fully-cross** (`k ∉ T_k` for every `k`),
"charted, not hunted". It is not empty either.

```
QUADRILLE — a fully-cross glider, 4 laws in ONE cell
kinds     n = 4,  W = 1        NO law amends its own kind (machine-checked)
rules     [(0,1,0), (0,1,0), (0,1,−1), (0,1,−1)]
targets   T_0={1,2}  T_1={0,3}  T_2={1,3}  T_3={0,2}
seed      one cell carrying ALL FOUR kinds
period    p = 1     displacement d = −1     glider under BOTH parity and OR

t=0   ..#..        kinds 0 and 1 (c = 0) between them toggle all four kinds
t=1   .#...        at the cell itself  -> the cell is cleared;
t=2   #....        kinds 2 and 3 (c = −1) between them toggle all four kinds
                   one cell left -> the whole quartet re-enacts there.
```

The mechanism is TANDEM-1's, but with the self-targets removed by *pairing*:
`{T_0, T_1}` partitions the kind set and so does `{T_2, T_3}`, so each of the
two cells receives exactly one toggle per kind. No law touches itself; the
quartet still relocates. Certified by `xnomos.verify_glider` in both
resolutions. Smaller fully-cross specimens exist at `n = 3` with `p = 2`
(e.g. rules `[(1,−1,1), (0,1,−1), (0,1,1)]`, `T = [{1,2},{0,2},{0,1}]`, seed
one cell with kinds 0 and 2 — a two-phase gait, `d = +1`).

Scan over fully-cross constitutions (`allow_self_target=False`,
out-degree ≥ 2, `W = 1`, `N = 16`, both signs of `d`, COMPLETE for each `p`):

| n | parity | OR |
|---|---|---|
| 3 | p=1 **UNSAT**; p=2,3,4,6 SAT; p=5 UNSAT | p=1 **UNSAT**; p=2,3,4,6 SAT; p=5 UNSAT |
| 4 | SAT from p=1 | SAT from p=1 |

Fully-cross needs at least 3 kinds (with `k ∉ T_k` and `|T_k| ≥ 2`) and, at
`n = 3`, at least period 2 — one-cell instantaneous relocation without
self-targets first becomes possible at `n = 4` (QUADRILLE).

### 8.5 The Twin-Kind Lemma — why gliders look like single markers

> **Lemma T.** If two kinds `m ≠ m′` have the *same author set with the same
> offsets* — i.e. `{k : m ∈ T_k} = {k : m′ ∈ T_k}` — then
> `supp_m(n) Δ supp_{m′}(n)` is a **constant of the motion**. Consequently in a
> glider `supp_m = supp_{m′}` at every time: twin kinds are rigidly bound.

*Proof.* Under either resolution, the toggle received by slot `(j,m)` is a
function of the active laws of the kinds that target `m`, at cells `j − c_k`.
If `m` and `m′` have the same author set, they receive *identical* toggles at
every cell and every step. So `supp_m(n+1) = supp_m(n) Δ Tog(n)` and
`supp_{m′}(n+1) = supp_{m′}(n) Δ Tog(n)`, and the symmetric difference is
unchanged. For a glider, `supp_m(n+p) Δ supp_{m′}(n+p) =
(supp_m(n) Δ supp_{m′}(n)) + d`; a finite set equal to its own translate by
`d ≠ 0` is empty. ∎

Machine-checked: **23,821 twin-pair invariance checks** across random
universes (`n ≤ 4`, `W ∈ {1,2}`, both resolutions) — **0 violations**.

This explains the shape of the minimal specimens. In the `n = 2` full-target
universe both kinds have author set `{0,1}`, so they are twins: every occupied
cell of a glider carries **both** kinds, and the system collapses to a
single-kind cellular automaton on `X ⊆ ℤ`,

  `X′ = X Δ σ^{c_0}A_0 Δ σ^{c_1}A_1`,  `A_k = {i ∈ X : i+a_k ∈ X, i+b_k ∉ X}`

(and `∪` in place of `Δ` for OR). TANDEM-1 is the orbit of a singleton under
`c = (1,0)`. The "bound pair" is not an accident of the search — it is forced.

---

## 9. The decided frontier and the censuses

### 9.1 SAT frontier — what is now decided outright

Each row: for that class, semantics and window, EVERY constitution and EVERY seed whose t=0..p trajectory fits the interior was decided at once.  UNSAT = complete no-go for the box.

| class | semantics | W | kinds n | box decided (interior cells / period) | verdict |
|---|---|---|---|---|---|
| E1 supersession | super | 1 | 1–6 | 26 cells, p≤18 | **UNSAT** |
| E1 supersession | super | 2 | 1–6 | 20 cells, p≤12 | **UNSAT** |
| E1 supersession | super | 3 | 1–6 | 14 cells, p≤8 | **UNSAT** |
| E1 supersession | super_or | 1 | 1–6 | 26 cells, p≤18 | **UNSAT** |
| E1 supersession | super_or | 2 | 1–6 | 20 cells, p≤12 | **UNSAT** |
| E1 supersession | super_or | 3 | 1–6 | 14 cells, p≤8 | **UNSAT** |
| E2 permutation targeting (cycle types L2, L2+L2, L2x3, L3, L3+L2, L3+L3, L4, L4+L2, L5, L6) | or | 1 | 1–6 | 26 cells, p≤20 | **UNSAT** |
| E2 permutation targeting (cycle types L2, L2+L2, L2x3, L3, L3+L2, L3+L3, L4, L4+L2, L5, L6) | or | 2 | 1–6 | 20 cells, p≤12 | **UNSAT** |
| E2 permutation targeting (cycle types L2, L2+L2, L2x3, L3, L3+L2, L3+L3, L4, L4+L2, L5, L6) | or | 3 | 1–6 | 14 cells, p≤8 | **UNSAT** |
| E2 permutation targeting (cycle types L2, L2+L2, L2x3, L3, L3+L2, L3+L3, L4, L4+L2, L5, L6) | parity | 1 | 1–6 | 26 cells, p≤20 | **UNSAT** |
| E2 permutation targeting (cycle types L2, L2+L2, L2x3, L3, L3+L2, L3+L3, L4, L4+L2, L5, L6) | parity | 2 | 1–6 | 20 cells, p≤12 | **UNSAT** |
| E2 permutation targeting (cycle types L2, L2+L2, L2x3, L3, L3+L2, L3+L3, L4, L4+L2, L5, L6) | parity | 3 | 1–6 | 14 cells, p≤8 | **UNSAT** |
| own-kind (control) | parity | 1 | 1–4 | 22 cells, p≤14 | **UNSAT** |
| own-kind (control) | parity | 2 | 1–4 | 16 cells, p≤10 | **UNSAT** |

Total solver time: 16980 CPU-seconds over 1930 jobs. Non-UNSAT results: 0.

Every row is a **complete no-go**, not a sample: for that class, semantics and
window, all constitutions *and* all seeds fitting the interior were decided at
once. For scale: the predecessor's entire campaign was ≈ 15.3 million
*individual* certified classifications; a single UNSAT row above rules out
every constitution in its class simultaneously — at `W = 1`, `n = 6`,
E2 alone that is `27⁶ ≈ 3.9 × 10⁸` constitutions times every seed in 26 cells.

### 9.2 Hypothesis audit for Theorem 3 — which hypothesis is load-bearing?

Theorem 3 rests on one asymmetry: **creation is own-kind (F1) even though
destruction is cross-kind (F2/F3)**. `hypaudit.py` builds the minimal variant
that breaks F1 and nothing else, with an engine written from scratch and
validated against `xnomos` on the `φ = id` case (**20,000 random states, exact
match, both clear-resolutions**):

> **SUPER-CROSS.** An active law of kind `k` targeting `j = i + c_k` **enacts
> kind `φ(k)`** at `j` if `j` is empty (φ a permutation), and clears the whole
> cell if occupied.

| sweep | scope | gliders |
|---|---|---|
| SUPER-CROSS, `n=2`, `φ` = swap, OR-clear | **COMPLETE**: 729 constitutions × 768 canonical seeds in 5 cells = **559,872** classifications | **0** |
| SUPER-CROSS, `n=2`, `φ` = swap, parity-clear | **COMPLETE**: same box, **559,872** classifications | **0** |

**So permuting the enacted kind is not enough.** Now change exactly one thing
— let an active law enact a **set** of kinds on empty ground instead of one,
keeping the guards, the offsets and the cell-clearing identical:

> **SUPER-MULTI.** An active law of kind `k` targeting `j = i + c_k` enacts
> **every kind in `T_k`** at `j` if `j` is empty, and clears the whole cell if
> occupied.

| sweep | scope | gliders |
|---|---|---|
| SUPER-MULTI, `n=2`, `T_0 = T_1 = {0,1}`, OR-clear | **COMPLETE**: 729 constitutions × 192 canonical seeds in 4 cells = **139,968** classifications | **1,744** |
| SUPER-MULTI, `n=2`, `T_0 = T_1 = {0,1}`, parity-clear | **COMPLETE**: same box, **139,968** classifications | **1,680** |

and TANDEM-1's own structure survives verbatim: `rules [(0,−1,1), (0,−1,0)]`,
enact-set `{0,1}`, one cell carrying both kinds, is a `p = 1`, `d = +1` glider
under supersession clearing too, in **both** resolutions.

This is as clean a controlled experiment as the subject allows. Three
semantics — plain supersession, SUPER-CROSS, SUPER-MULTI — share their guards,
their offsets and their destruction rule exactly, and differ only in the
out-degree of the **creation** channel:

| creation channel | out-degree | gliders |
|---|---|---|
| supersession (enact own kind) | 1 | **none** (Theorem 3, and 1,930 SAT no-goes) |
| SUPER-CROSS (enact `φ(k)`) | 1 | **0** in 1,119,744 complete classifications |
| SUPER-MULTI (enact `T_k`) | 2 | **3,424** certified gliders |

What breaks a no-go is never "cross-kind effects" as such — it is
**out-degree ≥ 2 in the creation channel**. That is the unifying statement of
this expedition:

> **Motion in nomodynamics is bought with out-degree, not with cross-kind
> effects.** A law that amends someone else's kind changes nothing on its own;
> a law that amends *two* kinds at once changes everything.

### 9.3 The TANDEM universe — a complete local census, and no guns

The home universe of the minimal glider, censused completely
(rules `[(0,−1,1), (0,−1,0)]`, `T = [{0,1},{0,1}]`, parity):

| | |
|---|---|
| scope | **COMPLETE**: all seeds in an 8-cell window over 2 kinds, translation-normalised — **49,152 canonical seeds** |
| CYCLE | 43,740 |
| GLIDER | **115** — every one `p = 1`, `d = +1`, all re-verified |
| GROWING (span) | 5,100 |
| EXTINCT | 13 |
| UNRESOLVED at 200 steps | 184 |
| seeds with `card(t=400) > card(t=200)` — the gun/puffer signature | **0** |

So in the TANDEM universe **every** unbounded phenomenon is a glider escaping
from a bounded oscillator; the law population always saturates. No gun, no
puffer, no rake. The smallest "growing" specimen is a period-2 blinker that
has emitted one glider and will emit no more:

```
t=0  .A.#....       A = a lone kind-0 law (the residue)
t=1  .A#.#...       # = a cell carrying both kinds
t=2  .A...#..       the TANDEM departs at speed 1; the blinker
t=3  .A#...#.       at cells 0-1 oscillates forever and emits nothing further
t=4  .A.....#
```

*(This is a pre-registration hit for the second half of **P5** — a bounded
population with one-sided unbounded advance exists in the cross-amendment
universes — and a miss for the first half, which predicted puffers under
supersession: Theorem 3 makes every supersession pattern bounded-or-anchored,
so there are none there either.)*

### 9.4 Independent E3 census (sub-expedition), and two corrections it forced

A parallel sub-expedition censused E3 by simulation and by an independently
driven use of the SAT instrument. Its results **agree with §4.5 exactly where
they overlap and refuted two of my claims**; both refutations are certified,
both are corrected above (§4.2 minimality, §4.6 speed spectrum), and the
original claims are kept on the record with the errors named.

**n = 2, W = 1 — COMPLETE, two independent methods agreeing.** All 729 rule
pairs × 9 target matrices = **6,561 universes**, both resolutions, × all **768**
translation-normalised seeds in a 5-cell window = **5,038,848 classifications
per resolution, 0 unresolved**.

| | |
|---|---|
| universes admitting a glider | **44 / 6,561** under parity — and the **same 44** under OR |
| their target matrix | `T = [{0,1},{0,1}]` for every one; the other 8 matrices are UNSAT (SAT, targets pinned, p ≤ 4, N = 20, both modes) |
| speed histogram | `|d|/p = 1` for **all** 280 distinct glider cycles per mode (140 right, 140 left) |
| period histogram | `p = 1` for all 280 |
| minimum law count | **2** (at period 1) |
| symmetry orbits | 11, each of size exactly 4 under reflection × kind-swap |
| phase-changing n=2 glider | **none** — confirmed twice (complete census; and SAT UNSAT for every coprime `(p,d)`, `2 ≤ p ≤ 8`, at `N = 14, 16, 20`, free targets, both modes) |

This is a clean independent confirmation of §4.5 at a finer grain: my complete
`(T, c)` classification found 6 gliding classes with guards free; refining by
guards, `T`-full + `c_0 ≠ c_1` admits 486 full constitutions and the **guards
cut 486 → 44**. The sub-expedition also proved the `n = 2` case of the
Twin-Kind Lemma independently (40,000 fuzz cases, 0 violations), from the same
observation that `T_0 = T_1 = {0,1}` makes both kinds receive identical toggles.

**Fully-cross (`k ∉ T_k`), n = 3 — COMPLETE over all 27 fully-cross target
matrices**, `p ≤ 4`, `d = 1..p`, `N = 12`, prime period: **4/27 glide under
parity, 11/27 under OR** — and the parity set is a strict subset of the OR set.
All 6 all-single-target matrices come back UNSAT, **including both 3-cycles**:
an independent bug-check of the E2 no-go that passes.

**The two corrections.** (i) The minimum law count over all E3 is **1**, not 2
— a single placed law of kind 0 in the fully-cross universe
`rules [(0,1,0),(0,1,1),(0,1,0)]`, `T = [{1,2},{0},{0}]` is a `p = 2`, `d = +1`
glider. (ii) `n = 3` **does** realise speed `2/3`. Both re-verified here.

**Largest certified minimal period: `p = 9`, from a single placed law** —
`rules [(0,1,0),(0,1,−1),(0,−1,1)]`, `T = [{0,2},{0,2},{0,1,2}]`, seed one law
of kind 1: a nine-phase gait advancing one cell, speed 1/9. A 3-law `p = 9`
specimen is **parity-only** (under OR the same seed is a period-2 oscillator) —
a second, independent instance of the §8.2 phenomenon.

**Mode asymmetry, both directions.** All-multi fully-cross at `n = 4` is
**empty under parity** up to `p ≤ 6` but SAT at `(1,1), (2,1), (4,1)` under OR;
the 3-law `p = 9` glider exists only under parity. Neither resolution dominates
the other.

*(Sub-expedition samples, clearly marked: a random 400-universe zoo trawl at
`n = 3`, and a scan complete over all 19,683 rule triples × 56 two-cell seeds
but over only **8 chosen** target matrices. Everything else quoted here is a
complete enumeration or a completed SAT decision.)*

### 9.5 An instrument bug worth recording

The sub-expedition found, and I confirmed directly, that
`xsat.solve(timeout=...)` was **inert** with the default solver: pysat's
CaDiCaL bindings do not implement `interrupt()`, so the watchdog `Timer`
raised `NotImplementedError` in its own thread, the traceback went silently to
stderr, and the solve ran to completion. Measured on their box: a job with
`timeout=2` ran 272.7 s and returned UNSAT.

The direction of the error matters. A budget that silently fails **open**
cannot manufacture a false UNSAT; it can only let a hard job run longer than
intended. So:

> **Every UNSAT in this report is a completed decision, never a truncated one**
> — the 1,930 frontier jobs and every `sharpness.py` call included. Not one
> `TIMEOUT` was ever returned, and now we know why.

`xsat.py` now detects non-interruptible solvers, says so once, and runs
un-timed rather than pretending a budget is enforced. (`glucose42` and
`minisat22` do support interruption if a real budget is wanted.)

### 9.6 Independent brute-force census — and the PICKET PUFFER

A second sub-expedition attacked both theorems empirically with a bit-parallel
C engine (one 64-bit word per kind, bitwise guards), gated behind a validation
suite: **390,175 exact-agreement checks against `xnomos`** — 24,000 narrow-step
and 24,000 wide-step random (constitution, state) pairs across all four modes,
4,800 `classify` comparisons, and **334,375** (normalised state, anchor) frames
compared at every step, which validates precisely the data the glider detector
keys on. The glider branch itself was exercised on 3,000 runs under a
*test-only* translation semantics (2,489 gliders, period and displacement
exact), since no real glider exists in those universes to trigger it.

| attack | scope | classifications | gliders |
|---|---|---|---|
| **E2 permutation targeting** — L=2 (≤6 laws/8 cells), L=3 (≤5/7), L=4 (≤4 laws/6 cells), 2+2 (≤4/6), all **COMPLETE**; L=5, L=6 sampled 60,000 constitutions each | W=1, budgets 200 steps / card 200 / span 40 | **12,063,649,200** | **0** |
| **E1 supersession** — n=1 (≤6/8), n=2 (≤7 laws/9 cells), n=3 (≤5/7), n=4 (≤4 laws/6 cells) all **COMPLETE**, both `super` and `super_or`; n=4 (≤5/7), n=5, n=6 sampled | W=1 | **12,615,149,336** | **0** |

**≈ 24.7 billion certified classifications, zero gliders.** Both theorems
survived. All **32,546** budget-exhausted holdouts were re-run at 4,000 steps:
32,482 growing, 64 cycles, **0 gliders**. The L=2/L=3/L=4/2+2 blocks were run
in parity *and* OR with **bit-identical histograms** — the Single-Author Lemma
machine-confirmed for permutation constitutions at this scale. For scale: the
E1 census alone exceeds the predecessor's entire supersession campaign by about
four orders of magnitude.

A second, independent detector was used for Task 4 that does **not** use the
`Φᵖ = σᵈ` test — it looks for a bounded packet recurring in a window travelling
with the front. It found **zero bounded moving packets in E2 and zero in
supersession** across every world scanned. That is an independent confirmation
of Theorems 2′ and 3 by a method that could not have inherited a bug from the
glider certifier.

**Named specimen: the PICKET PUFFER** (E3 multi-target, OR resolution) — the
object neither §9.3 nor the theorems reach, and the answer to the second half
of pre-registration **P5**. Re-certified here by independent re-simulation:

```
rules   [(0,1,1), (0,−1,1)]     T_0 = T_1 = {0,1}
seed    {cell 0: kind 0, cell 5: kind 1}      — TWO placed laws

t=0   |A....B.........................|    A = kind 0 only
t=4   |A####B.###.....................|    B = kind 1 only
t=8   |A####B.###.###.................|    # = both kinds
t=12  |A####B.###.###.###.............|
t=16  |A####B.###.###.###.###.........|
t=20  |A####B.###.###.###.###.###.....|
```

| it **does** satisfy | it **does not** satisfy |
|---|---|
| the 28-cell window behind the front is exactly **p = 4 periodic**, `t = 60..180` | `Φᵖ(S) = σᵈ(S)` — `verify_glider` FAILS for every `p ≤ 8`, `|d| ≤ 8` |
| the front advances `hi(t+4) − hi(t) = +4` — **speed 1** | bounded population: `card` grows **+1.507 laws/step** (114 at `t=70` → 218 at `t=139`) |
| the debris it lays is periodic in place — a `###.` picket fence | a free trailing edge: `lo(t) = 0` **forever** |

So it is a **puffer with an anchored tail**: a periodic engine translating at
speed 1 that leaves a permanent periodic wake, welded to its birthplace. It is
exactly the shape the predecessor's ruler fronts had — one edge pinned, one
edge advancing — but with a genuinely *periodic* front rather than a
Sierpinski stutter, and with population growing linearly rather than staying
bounded. 136 structured-debris candidates of this family were found; a
`p = 2, d = +1` variant exists under supersession-style clearing too.

*(The sub-expedition's stated gap: its `wider.py` attack at `W = 2..5` was
written and validated but not run. My SAT frontier covers `W ≤ 3` for both
theorems exactly — §9.1 — so that gap is closed from the other side.)*




---

## 10. Verdict

**The cross-amendment glider question is settled.**

**What is now proved.**

1. **The Out-Degree Law.** If, restricted to the kinds a pattern actually uses,
   every law amends at most one kind, no free glider exists — any offsets, any
   window, any dimension, parity or OR, any guard predicate whatsoever, any
   schedule. *(Theorem 2′ + Corollary 2.4, via the tropical monovariant.)*
   This subsumes the Anchor Theorem's Corollary 1, kills **E2 reciprocal
   amendment and every permutation constitution of every cycle length**
   (L = 3, 4, 5, 6 and products had never been hunted at all), and kills every
   non-permutation single-target constitution as well.
2. **The Supersession No-Go.** E1 supersession admits no free glider, in any
   dimension, under either clear-resolution. *(Theorem 3.)* The proof turns on
   supersession's creation channel being own-kind even though its destruction
   channel is not.
3. **The Tropical Speed Law.** Any glider satisfies
   `p·min(λ_min,0) ≤ d ≤ p·max(λ_max,0)` for the extreme cycle means of the
   amendment digraph on its kinds. *(Theorem 1.)*
4. **Existence at the threshold.** Out-degree 2 suffices, at every velocity and
   in every dimension, with two placed laws and period 1. *(Theorem 4.)*
5. **The Twin-Kind Lemma.** Kinds with identical author sets are rigidly bound
   in any glider. *(Lemma T.)*
6. **A complete classification at n = 2, W = 1**: a glider exists iff both laws
   amend both kinds and `c_0 ≠ c_1` — 6 of the 81 (target matrix, offset
   vector) classes with guards free; refined by guards, **44 of 6,561 full
   constitutions**, every one of period 1 and speed 1 (§9.4).

**What was searched, and how completely.**

- **1,930 bounded existence questions decided exactly by SAT, all UNSAT**,
  covering E1 (n ≤ 6, W ≤ 3, up to 26 interior cells and p ≤ 18) and E2 (cycle
  types L2…L6 and products, up to 26 cells and p ≤ 20), plus an own-kind
  control. Each is a complete no-go over *all* constitutions in its class.
- **9,342 universes completely classified** (all 81 at n = 2 and all 9,261 at
  n = 3, target matrix × offset vector, guards quantified over): **zero
  violations of the theorems**.
- **1,119,744 certified classifications** in the SUPER-CROSS hypothesis audit
  (complete, 2 kinds, 5 cells, both clear-resolutions).
- **49,152 canonical seeds** in a complete census of the TANDEM universe —
  115 gliders, **no gun, no puffer, no rake**.
- **5,038,848 classifications per resolution** in a sub-expedition's complete
  `n = 2` E3 census (6,561 universes × 768 seeds), agreeing with §4.5 and
  fixing two of my claims (§9.4).
- **≈ 24.7 billion certified classifications** in an independent bit-parallel
  C census attacking both theorems — 12.06 bn on E2 (complete through 4 laws /
  6 cells at L = 4 and at 2+2, 6 laws / 8 cells at L = 2) and 12.62 bn on E1
  supersession (complete through 7 laws / 9 cells at n = 2, 4 laws / 6 cells at
  n = 4, both resolutions): **zero gliders**, all 32,546 holdouts chased to
  4,000 steps, and a second detector that never uses the `Φᵖ = σᵈ` test finding
  **zero bounded moving packets** in either universe (§9.6).
- **267,201 invariant checks** along 20,000 random trajectories, plus 23,821
  twin-kind checks and 1,200 encoder-fidelity trials — **zero violations
  anywhere**.

**What refutes the predecessor.** `glider-question/RESULTS.md` §4 asserted that
E3 "riders" are *provably* glider-dead, on the ground that "every kind remains
its own sole author". That inference is invalid — a law amending its own kind
*among others* still gives every other kind a second author — and the class it
dismissed is where the first free glider lives. Corollary 3 of that report
("the caterpillar drags an immortal tail") is likewise true only for own-kind
amendment; DOUBLET is a working caterpillar.

**What refutes me.** Two claims in my own first draft were wrong and are
corrected in place with the errors named: that two placed laws is the floor
(it is one — §4.2), and that speed `2/3` needs four kinds (three suffice; my
search had imposed an out-degree restriction the question does not — §4.6).
Both were caught by the parallel sub-expedition and re-verified here. The
instrument also had a genuine bug — the first shift constraint let laws
shifting out of the window vanish — caught within seconds by the certifier
(§5); and its `timeout` argument turns out to be inert with CaDiCaL, which
means every UNSAT reported here is a **completed** decision rather than a
truncated one (§9.5).

**The sharpest questions left open.**

1. **The displacement cap, and why it vanishes at four kinds.** At `W = 1`
   the realisable displacements are: `|d| = 1` only at `n = 2`; `|d| ≤ 2` at
   `n = 3` (exactly — every coprime `(p,d)` with `|d| ≥ 3` is UNSAT to
   `p ≤ 8`, while `2/3, 2/5, 2/7` all exist); and **at `n = 4` every coprime
   `(p,d)` tested is realisable**, up to `6/7`. I conjectured `|d| ≤ (n−1)W`
   and refuted it myself at `n = 4` (§4.6). Neither the trivial bound
   `|d|/p ≤ W` nor Theorem 1's cycle-mean bound involves the number of kinds
   at all, so the `n = 2, 3` caps ask for a genuinely new invariant —
   presumably one counting how many distinguishable internal phases a packet
   can carry — and the question of what changes at four kinds is the
   successor charter's most concrete target.
2. **A sharp characterisation.** The Zero-Cycle condition is necessary
   everywhere and sufficient at `n = 2`; at `n = 3` it leaves 2,226 permitted
   but empty universes, and sampling shows these do *not* fill in at larger
   period. A sharp criterion must involve the **guards** `(a_k, b_k)`, which
   the tropical argument deliberately discards.
3. **Guns and puffers.** The TANDEM universe has none (complete 8-cell census).
   Does *any* cross-amendment universe contain a gun, a puffer, or a rake — an
   object whose law population grows without bound while a bounded core
   recurs? The theorems of §2–§3 say nothing about unbounded patterns.
4. **General state-dependent targeting.** Theorem 3 covers supersession;
   §9.2 shows permuting the enacted kind does not escape it. Is there a no-go
   for *every* state-dependent targeting whose creation channel has
   out-degree ≤ 1 — i.e. is the Out-Degree Law true for state-dependent
   semantics too? The proof of Theorem 2 needs Lemma R, which state-dependent
   destruction breaks; Theorem 3 got around this by hand for one semantics.

> **The foundational law, restated.** The predecessor's Front Law said *the
> eldest law cannot be repealed*, and traced all of nomodynamics' immobility to
> it. The correct general statement is narrower and sharper:
>
> **A law-packet can travel exactly when some law amends two kinds at once.**
> One target buys oscillation; two buy motion. Cross-amendment is not enough —
> *cross-amendment with fan-out* is.

---

## 11. Code and reproduction

All code lives in this directory and imports the shared engine
`../xnomos.py`. Nothing here depends on a stored result.

| file | what it is |
|---|---|
| `xsat.py` | the SAT instrument: exact bounded encoding of "does a glider exist?", with the constitution's offsets and target matrix as variables. Auto-certifies every SAT model against `xnomos` and raises if they disagree. |
| `validate.py` | encoder soundness battery (fidelity, exactness, completeness on published specimens, own-kind control). |
| `invariants.py` | adversarial fuzz of every structural fact the theorems of §2–§3 use. |
| `frontier.py`, `frontier_big.py` | the no-go campaign (parallel; writes `data/frontier*.json` incrementally). |
| `make_tables.py` | renders the frontier table from the JSON. |
| `sharpness.py` | complete (target matrix × offset vector) classification at n = 2 and n = 3 — is the theory sharp? |
| `hypaudit.py` | hypothesis audit for Theorem 3; independent from-scratch engine, validated against `xnomos`. |
| `demo.py` | the specimen gallery (7 gliders + the PICKET PUFFER + the 2-D and ring lifts), every one re-verified from scratch at display time. |
| `fastcensus.c`, `fastlib.py`, `validate_fast.py`, `census.py`, `nearmiss.py` | the bit-parallel C census and its 390,175-check validation gate (§9.6). |
| `e3_*.py` | the independent E3 census (§9.4). |

```sh
cd /Users/lukacs/claude/math/program/phase6/xamend1d

python3 ../xnomos.py            # shared engine self-tests (7/7)
python3 validate.py 1200        # encoder soundness — MUST pass before citing any UNSAT
python3 invariants.py 20000     # theorem invariants: 267,201 checks, 0 violations
python3 demo.py                 # the specimen gallery, all re-certified

python3 frontier.py             # the moderate no-go campaign  (~2 min, 12 cores)
python3 frontier_big.py         # the full frontier            (~90 min, 11 cores)
python3 make_tables.py          # render the frontier table

python3 sharpness.py 2 14 6 parity   # complete n=2 classification (81 universes)
python3 sharpness.py 3 12 3 parity   # complete n=3 classification (9,261 universes)
python3 hypaudit.py                  # SUPER-CROSS / SUPER-MULTI controlled experiment
python3 validate_fast.py             # C-engine validation gate (390,175 checks)
python3 census.py                    # the ~24.7 bn-classification brute-force census
```

Ready to paste into any demo:

```python
import xnomos
from xnomos import Const, state_of, verify_glider, spacetime

# TANDEM-1 — the first free glider in nomodynamics
C = Const([(0, -1, 1), (0, -1, 0)], [(0, 1), (0, 1)])
S = state_of([(1, 0), (1, 1)])          # one cell, both kinds
assert verify_glider(S, C, 1, 1)        # Phi(S) = sigma(S)
print("\n".join(spacetime(S, C, 6, "parity", 0, 9)))

# SOLO — the smallest glider of all: ONE placed law, fully cross
C = Const([(0, 1, 0), (0, 1, 1), (0, 1, 0)], [(1, 2), (0,), (0,)])
S = state_of([(1, 0)])
assert verify_glider(S, C, 2, 1)        # p = 2, d = +1
```

Data files (all < 1 MB): `data/frontier.json`, `data/frontier_big.json`,
`data/frontier_table.md`, `data/sharpness_n2_parity.json`,
`data/sharpness_n3_parity.json`, plus the run logs.
