# Expedition Y-C — the replicator hunt

*Chapter three, prediction **Y5**: "some code in the citation or multi-target
sector produces a disjoint copy of itself." Confidence recorded in
`CITATION.md` before the run: ≈ 0.4.*

Honesty tiers used throughout: **[E] established** (proved here or cited from a
proof elsewhere in the repo), **[M] measured** (a bounded search or a numerical
observation — decides a box, never a question), **[P] proposal**
(interpretation, conjecture, framing).

---

## 1. PRE-REGISTRATION

*Written and saved before the first search run. Kept verbatim; the scorecard in
§9 is appended afterwards, and nothing above this line was edited after the
searches began.*

### 1.1 What I will call a replicator

The state space: finite sets of **placed laws** `(i,k) ∈ ℤ^D × K`. A state is
written `S`, the global map `Φ`, translation `σ^d`. `card(S)` counts placed
laws, `supp(S) ⊆ ℤ^D` the occupied cells.

**Interaction radius.** `R(C) = max` sup-norm over all offsets `a_k,b_k,c_k`.

> **Lemma S (separation).** If `dist_∞(supp A, supp B) > 2R` then
> `Φ(A ⊔ B) = Φ(A) ⊔ Φ(B)` and the images are again disjoint, in every mode.

Two copies at sup-distance `> 2R` are therefore *causally independent* for one
step: neither can read, block, or write onto the other. I call such copies
**free**. Copies that merely have disjoint supports I call **embedded**.

### 1.2 The rung ladder (pre-registered, strict)

Let `S` be the seed, `p ≥ 1`, and `d₁ ≠ d₂ ∈ ℤ^D`.

- **Rung 1 — periodic doubling.** `card(S_t) → ∞`, and at some `t` the state
  contains two **embedded** copies `σ^{d₁}S, σ^{d₂}S` with disjoint supports.
  No gap, no debris condition. *Cheap.*
- **Rung 2 — clean replicator.** There are `p, d₁ ≠ d₂` with
  `Φ^p(S) ⊇ σ^{d₁}S ∪ σ^{d₂}S`, the two copies **free** (gap `> 2R`), and the
  debris `D = Φ^p(S) ∖ (σ^{d₁}S ∪ σ^{d₂}S)` either empty (**rung 2-exact**) or
  a state that is itself eventually periodic under `Φ` in isolation
  (**rung 2-debris**). The gap requirement is what stops a solid growing block
  from qualifying — see §1.4.
- **Rung 3 — colony.** The number of pairwise-**free** copies of `S` inside
  `S_t` is unbounded in `t`. (Sub-rung **3-emb**: unbounded *embedded* copies.)
- **Rung 4 — constructor.** A code that builds a *specified* target pattern
  read off a blueprint carried in its own body. I do not expect to reach this;
  if I do not, I will say so plainly.

### 1.3 Certificate standard

Every claimed replication event is re-verified by `replib.pstep`, an engine
written from the definition on **frozensets of placed laws**, sharing no code
with `xnomos.step` (which uses `{cell: bitmask}`). Certificates exhibit `p`,
the offsets, the two copies as explicit cell sets, the gap, and the debris.

### 1.4 Anti-cheat clauses

**(a) The solid block.** The colonizer `(0,1,1)` from a solid block of `n` laws
satisfies `Φ^n(S) = S ⊔ σ^n(S)` **exactly** — a "replicator" by the naive
reading. It is excluded by the gap requirement (the two blocks are adjacent,
gap 1 ≤ 2R = 2). Any specimen I report must survive this test, and I will run
the colonizer through the detector to confirm the filter bites.

**(b) The one-law seed.** If `card(S) = 1` then "a copy of `S`" means only "a
law of the same kind somewhere", and rung 2 degenerates: any constitution that
turns one law into two well-separated laws of that kind qualifies. I therefore
require of a **reported specimen** that `|supp(S)| ≥ 2` — the seed occupies at
least two distinct cells, so that a copy has to reproduce a *spatial relation*,
not just a symbol. One-law results will be reported separately and labelled
**degenerate**.

*(Clause (b) added before the first search run, after writing the detector and
noticing the degeneracy; §1.1–1.3 and §1.5 unchanged.)*

### 1.5 What I expect (recorded before searching)

- **Y-C-1.** Rung 1 is reachable and cheap; the Pascal columns will qualify.
  Confidence 0.85.
- **Y-C-2.** Rung 2 is reachable somewhere in the multi-target / citation
  sector. Confidence 0.5. *(The charter's Y5 said 0.4; I am marginally more
  optimistic because out-degree ≥ 2 already buys motion and a fissioning
  glider is the obvious mechanism.)*
- **Y-C-3.** Rung 3 in the **exponential** sense is impossible. The light cone
  gives `card(S_t) ≤ n·(span₀ + 2Rt + 1)^D`, polynomial in `t`; a colony whose
  copies are all free would double every `p` steps. Confidence 0.95 — I expect
  this to become a theorem, and if so the mission's rung 3 must be **rewritten**
  as "unboundedly many copies, necessarily at polynomial rate".
- **Y-C-4.** Rung 4 is out of reach this cycle. Confidence 0.9.
- **Y-C-5 (linearity).** `Φ` is **not** `𝔽₂`-linear: superposition
  `Φ(A Δ B) = Φ(A) Δ Φ(B)` will fail on overlapping supports for generic
  constitutions, because occupancy guards are an OR over kinds. But it will
  hold *automatically* for separated supports (Lemma S), so **any** replicator
  whose copies are free will look additive at the moment of fission. The honest
  question is therefore not "is the replicator additive?" but "**does the
  fission happen in the sparse regime, where additivity is free, or in
  contact, where it is not?**" I expect the first specimens to be sparse, and I
  will hunt specifically for a contact fission. Confidence in the reframing:
  0.8.

---

*(Everything below this line was written after the searches ran.)*

## 2. The object, the definitions, and three theorems

### 2.1 Notation

A **state** `S` is a finite set of placed laws `(i,k) ∈ ℤ^D × K`; `supp(S)` is
its cell set, `card(S)` its number of placed laws, `Φ` the global map (parity,
OR, supersession or supersession-OR), `σ^d` translation. The **interaction
radius** of a constitution is

    R(C) = max over kinds k of max( ‖a_k‖_∞ , ‖b_k‖_∞ , ‖c_k‖_∞ ).

### 2.2 Lemma S (separation) — [E], proved, machine-checked

> If `dist_∞(supp A, supp B) > 2R` then `Φ(A ⊔ B) = Φ(A) ⊔ Φ(B)`, and the two
> images are again disjoint. This holds in **every** mode and with citation
> guards.

*Proof.* (i) *Activity.* A law `(i,k)` with `i ∈ supp A` reads only `i+a_k` and
`i+b_k`, both within `R` of `supp A`. If either lay in `supp B` we would have
`dist(supp A, supp B) ≤ R < 2R+1`. So every guard of `A` is evaluated on cells
where `A ⊔ B` agrees with `A`; the active set of `A` is unchanged by `B`, and
symmetrically. (ii) *Writes.* Every write from `A` lands within `R` of
`supp A`, every write from `B` within `R` of `supp B`; these two neighbourhoods
are disjoint (otherwise `dist ≤ 2R`), and neither meets the other's support.
Hence each written cell's toggle-multiset, OR-mask, or clear/enact vote is
computed from one side only. ∎

**Why this matters for the mission's linearity question.** For separated
supports `Φ(A ⊔ B) = Φ(A) Δ Φ(B)` *automatically*. Long-range superposition is
therefore not evidence of additivity — it is a triviality of locality. The only
informative superposition test is at **contact**. Machine-checked: 400 random
constitutions × 4 modes, zero violations (`verify_replication.py` §1).

### 2.3 Theorem A (polynomial population bound) — [E], proved

> For any constitution with `n` kinds in `ℤ^D`, radius `R`, and any finite seed
> whose support has bounding box of side `s₀`,
>
>     supp(S_t) ⊆ supp(S₀) + [−Rt, Rt]^D ,   card(S_t) ≤ n·(s₀ + 2Rt + 1)^D .

*Proof.* A toggle, an OR-hit and a supersession enactment all land at `i + c_k`
for some placed law at `i`, i.e. within `R` of `supp(S_t)`; supersession clears
only remove. So `supp(S_{t+1}) ⊆ supp(S_t) + [−R,R]^D`. Induct, and bound the
laws per cell by `n`. ∎

**Corollary A1 (no exponential colony) — [E].** The number of pairwise disjoint
translated copies of a fixed seed `S` inside `S_t` is at most
`card(S_t)/card(S) = O(t^D)`. **Rung 3 in the mission's literal "exponential"
reading is empty in every dimension, for every constitution, in every mode.**
The achievable strong form is *unboundedly many copies, necessarily at
polynomial rate* — and that is how I read rung 3 from here on.

**Corollary A2 (every free fission must self-collide) — [E].** Suppose
`Φ^p(S) = σ^{d₁}S ⊔ σ^{d₂}S` with the copies free, and suppose that at every
generation the `2^k` copies stayed pairwise free through the next `p` steps.
Lemma S would then give `card(Φ^{kp}S) = 2^k·card(S)`, contradicting Theorem A
as soon as `2^k > n(s₀+2Rpk+1)^D / card(S)`. **So a nomodynamic replicator can
never keep doubling at a fixed period: within `O(log t)` doublings the children
must come into contact, or the fission must stop being exact.**

This is not an abstract worry — it is exactly what the specimens do. THE
ENGROSSMENT's clean doublings occur at `t = 4, 12, 28, 60, 124, 252`, i.e.
`t = 4(2^k − 1)`: **the doubling period itself doubles**, and `Φ^8(S)` is two
free copies, not four, because the first fission's children collide.

### 2.4 The additivity tests used on every specimen

Let `L` be the **unconditional linear map**: every placed law fires regardless
of its guard, toggles resolved by parity. `L` is `𝔽₂`-linear by construction.

- **(N1) path test.** How many `t ≤ T` have `Φ^t(S₀) ≠ L^t(S₀)`? Zero means the
  guard never bites on the orbit and the trajectory *is* the additive CA.
- **(N2) splitting test — the decisive one.** For every splitting
  `S₀ = A ⊔ B` into two nonempty parts, is
  `Φ^p(S₀) = Φ^p(A) Δ Φ^p(B)`? If some splitting fails, the doubling of `S₀` is
  **not** a superposition of the doublings of its parts, and the Fredkin
  argument does not apply. I call such a replicator **non-additive**.
- **(N3) random-pair test.** `Φ(A Δ B) = Φ(A) Δ Φ(B)` on random overlapping
  small states.
- **(N4) control.** Far-apart superposition, which must hold by Lemma S.

---

## 3. The specimens

Every certificate below is produced by `xnomos.step` and independently
re-checked by `replib.pstep`, an engine written from the definition on
frozensets of placed laws. `python3 verify_replication.py` re-derives all of it
in ~20 s (28 checks).

### 3.1 THE ENGROSSMENT — rung 3, non-additive. **The headline.**

*2-D · 2 kinds · Moore offsets · **occupancy guards only** (chapter one/two
semantics — no citation needed) · parity · seed of 4 placed laws in 2 cells.*

```python
from xnomos import Const, state_of
ENGROSSMENT = Const([((0,-1), (-1,1), (1,1)),      # kind A
                     ((0,-1), (0,1),  (1,0))],     # kind B
                    [(0,1), (0,1)], dim=2)          # each amends BOTH kinds
SEED = state_of([((0,0),0), ((0,0),1), ((0,1),0), ((0,1),1)])   # a vertical
MODE = "parity"                                                 # A|B domino
```

Reading the guards aloud: *"While some law stands due south of me and none
stands to the north-west (resp. north), amend both kinds to my north-east
(resp. east)."*

**Certificate — rung 2-exact.** `R = 1`, so free means gap `> 2`.

```
   Φ⁴(S) = S ⊔ σ^(4,4)(S)     EXACTLY — no debris at all
   copy 0 : {(0,0), (0,1)}   each cell carrying A and B
   copy 1 : {(4,4), (4,5)}   each cell carrying A and B
   gap    : 4  >  2R = 2                     card 4 → 8
```

Spacetime (`#` = both kinds in one cell), `t = 0 … 4`:

```
   t=0         t=1         t=2         t=3         t=4
   .........   .........   .........   .........   .........
   .........   .........   .........   .........   .....#...
   .........   .........   .........   ....#....   .....#...
   .........   .........   ...#.....   ...##....   .........
   .........   ..#......   ...#.....   ..##.....   .........
   .#.......   .##......   .#.......   .##......   .#.......
   .#.......   .#.......   .#.......   .#.......   .#.......
   card 4      card 8      card 8      card 16     card 8
```

**Colony — rung 3.** At every `t = 4m` the state is *exactly*
`2^popcount(m)` free copies of the seed and nothing else. Verified for all
`m ≤ 65`:

| t | 4 | 8 | 12 | 16 | 20 | 24 | 28 | 60 | 124 | 252 |
|---|---|---|---|---|---|---|---|---|---|---|
| free exact copies | 2 | 2 | 4 | 2 | 4 | 4 | 8 | 16 | 32 | **64** |

Unbounded, so rung 3 in the (only possible, by Corollary A1) polynomial sense.

**Non-additivity — the point.** [M], and decisive:

- **(N1)** `Φ^t(S₀) ≠ L^t(S₀)` for **every** one of `t = 1…140`. The guard
  bites from the start: only **2 of the 4** placed laws of the seed are active
  at `t = 0`.
- **(N2)** superposition fails for **8 of the 10** splittings of the seed. The
  witness is as blunt as it gets — split one single law off and the child is
  never born at all:

```
    A = {B@(0,1)}            B = {A@(0,0), B@(0,0), A@(0,1)}
    Φ⁴(A ⊔ B)            = {(0,0):AB, (0,1):AB, (4,4):AB, (4,5):AB}
    Φ⁴(A) Δ Φ⁴(B)        = {(0,0):AB, (0,1):AB}
```

- **(N3)** 503 of 4000 random overlapping pairs violate superposition — but
  see §6.1: N3 is a fact about the constitution, not about the replicator.
- **(N4)** the far-apart control holds, as Lemma S requires.

So: **the copy is not the superposition of the copies of the parts.** This is
not Fredkin's additive self-reproduction; the four laws of the seed must act
*together*, and the guard is load-bearing at every step.

*(Curiosity, [M]: the copy count still obeys `2^popcount`, the classic additive
signature. **The `2^popcount` law is therefore not diagnostic of additivity** —
it survives into a demonstrably non-additive system.)*

### 3.1a THE SPLIT DECISION — p = 2, a true binary fission, colony `t/2 + 1`

*2-D · 2 kinds · Moore offsets · **citation guards** · OR resolution · seed of
4 placed laws in 2 cells.* Found in the 2-D citation census; the cleanest
replicator of the expedition.

```python
SPLIT = Const([((0,0), (-1,-1), (0,-1)),      # kind A: writes {A,B} SOUTH
               ((0,0), (1,0),   (0,1))],      # kind B: writes {A,B} NORTH
              [(0,1), (0,1)], dim=2,
              guards=[(1, 0),                 # A: "kind B stands HERE and no
                                              #     kind A stands south-west"
                      (1, None)])             # B: "kind B stands HERE and
                                              #     nothing stands east"
SEED = state_of([((0,0),0), ((0,0),1), ((2,0),0), ((2,0),1)])
MODE = "or"
```

**Certificate — the parent does not survive; it becomes two children.**

```
   Φ²(S) = σ^(0,−2)(S)  ⊔  σ^(0,+2)(S)      EXACTLY, debris ∅, gap 4 > 2R = 2
```
```
   t=0            t=1            t=2            t=3            t=4
   ......         ......         ......         ......         .#.#..
   ......         ......         ......         .#.#..         ......
   ......         ......         .#.#..         .#.#..         ......
   ......         .#.#..         ......         .#.#..         ......
   .#.#..         .#.#..         ......         ......         .#.#..
   ......         .#.#..         ......         .#.#..         ......
   ......         ......         .#.#..         .#.#..         ......
   ......         ......         ......         .#.#..         ......
   card 4         card 12        card 8         card 24        card 12
```

**Colony — rung 3, and monotone.** At *every* even time the state is **exactly**
`t/2 + 1` free copies of the seed and nothing else:

| t | 2 | 4 | 6 | 8 | 10 | … | 198 |
|---|---|---|---|---|---|---|---|
| free exact copies | 2 | 3 | 4 | 5 | 6 | … | **100** |

No 2^popcount collapse: the copies pile up steadily, spaced 4 apart on a
vertical line. The mechanism is worth naming — **OR resolution is what stops
the Fredkin cancellation.** Under parity a fission cascade annihilates its own
middle and the population falls back to `2^popcount`; under OR the coincident
enactments merge instead of cancelling, and the binomial spread survives
intact.

Non-additive: **8 of 10** splittings of the seed violate superposition, and
`Φ ≠ L` on 136 of 139 steps.

### 3.1b THE QUORUM — the minimal non-additive replicator: **two placed laws**

*2-D · 2 kinds · Moore offsets · occupancy guards · **supersession-OR** · seed
of 2 placed laws in 2 cells.* Supersession is the E1 semantics: an active law
enacts its own kind on empty ground, and otherwise clears the whole cell.

```python
QUORUM = Const([((-1,-1), (0,-1), (1,-1)),
                ((0,0),   (0,-1), (1,-1))], [(0,1), (0,1)], dim=2)
SEED   = state_of([((0,0),1), ((1,1),0)])      # B at (0,0), A at (1,1)
MODE   = "super_or"        # targets are inert under supersession: creation is
                           # own-kind, so only the offsets and guards matter
```
```
   t=0        t=1        t=2        t=3        t=4
   ..A....    ..A....    ..A....    ..A....    ..A....
   .B.....    .B.A...    .B.....    .B.A...    .B.....
   .......    ..B....    ....A..    ..B.A..    .......
   .......    .......    ...B...    ...B.A.    .......
   .......    .......    .......    ....B..    ......A
   .......    .......    .......    .......    .....B.
   card 2     card 4     card 4     card 8     card 4
```

Certificate: `Φ⁴(S) = S ⊔ σ^{(4,−4)}(S)` exactly, gap 4 > 2R = 2, debris `∅`;
32 exact free copies by `t = 252`; **both** splittings of the seed violate
superposition, which is the maximum a two-law seed can do. Two placed laws is
the smallest a replicator can be under clause 1.4(b), so this is minimal in the
strongest available sense within the searched box.

### 3.2 THE PRECEDENT — rung 2-exact on **ℤ**, non-additive, citation sector

*1-D · 2 kinds · window 1 · **reciprocal amendment** (a permutation
constitution, cycle type [2]) · citation guards · parity (≡ OR here, by the
Single-Author Lemma).*

```python
PRECEDENT = Const([(-1,-1,1), (-1,-1,1)], [(1,), (0,)], dim=1,
                  guards=[(None,1), (0,1)])
SEED = state_of([(0,0), (1,0), (2,0), (2,1)])       # "AA#"
MODE = "parity"
```

*"While some law stands to my left and **no law of kind B** stands there,
enact kind B to my right"* — and B says *"while a law **of kind A** stands to
my left and no law of kind B stands there, enact kind A to my right."*

```
   t= 0 |.AA#............|  card 4   ← seed
   t= 1 |.AAA#...........|
   t= 2 |.AA#A#..........|
   t= 3 |.AAAB##.........|
   t= 4 |.AA#.B#.........|
   t= 5 |.AAA#B#.........|
   t= 6 |.AA#AA#.........|
   t= 7 |.AAABAA#........|
   t= 8 |.AA#..AA#.......|  card 8   ← Φ⁸(S) = S ⊔ σ⁵(S), EXACT, gap 3 > 2R = 2
```

Certificate: `p = 8`, `d₁ = 0`, `d₂ = +5`, debris `∅`, gap 3, re-checked on the
independent engine. `Φ ≠ L` at all 200 steps; **10 of 10** seed splittings
violate superposition. This is a genuinely non-additive replicator **on the
line**, and it needs citation: the whole `xnomos` occupancy-guard box on ℤ
(§4.1) contains none.

It does **not** reach rung 3: the two copies interact and the orbit falls into
a cycle of period 128, re-passing the two-copy state at `t = 8, 136, 264, 392`.
That is Corollary A2 made visible.

### 3.3 THE MOOT — rung 3, **fully additive**: the Fredkin control

*2-D · 2 kinds · occupancy guards · parity.* Designed, not found: the guard
`b = north` can never fail because the orbit never leaves the line `y = 0`, so
`Φ` **is** the additive CA `x ↦ x·(1 + σ + σ^{-1})` (elementary Rule 150) on
the alphabet {cell carries A and B}.

```python
MOOT = Const([((0,0),(0,1),(1,0)), ((0,0),(0,1),(-1,0))], [(0,1),(0,1)], dim=2)
SEED = state_of([((0,0),0), ((0,0),1), ((2,0),0), ((2,0),1)])
```
```
   t=0 |..........#.#..........|   t=8 cells {−8,−6}, {0,2}, {8,10}
   t=8 |..#.#.....#.#.....#.#..|   = THREE free exact copies, debris ∅
```

`Φ = L` at all 200 steps; superposition never fails. Reaches **85** exact free
copies by `t = 508`. Everything about it is the classical additive
self-reproduction, and it is reported as such.

### 3.4 THE PASCAL COLUMN — rung 3, additive, **degenerate seed**

Chapter one's own-kind grower `Const([((0,0),(1,0),(0,1))], dim=2)` from a
single law satisfies `S_{2^k} = {(0,0)} ⊔ {(0,2^k)}` exactly, and reaches 16
free copies by `t = 60`. `Φ = L` throughout. Because `|supp(S)| = 1`, my
pre-registered clause 1.4(b) rules it **degenerate**: "a copy of the seed" here
means only "a law of the same kind". Recorded, not counted as the headline.
(The repo's notes said only that "size dips to 2 at `t = 2^k`"; that the two
laws are two disjoint free copies of the seed is, as far as I can tell, not
stated anywhere before this expedition.)

### 3.5 The 1-D phantom-citation replicator — rung 3 on ℤ, additive

Three kinds; kind 2 is a **phantom** — never seeded and never a target — and
the other two cite it in their vacancy clause, which therefore can never fail:

```python
PHANTOM = Const([(0,0,1), (0,0,-1), (0,0,0)], [(0,1), (0,1), (2,)], dim=1,
                guards=[(None,2), (None,2), (None,None)])
SEED = state_of([(0,0), (0,1), (2,0), (2,1)])
```

Certificate: `Φ⁸(S) = σ^{-8}S ⊔ S ⊔ σ^{8}S`, gaps 6 and 6, debris `∅`; 43 exact
free copies by `t < 300`. `Φ = L` throughout — the citation has made the guard
vacuous, and what is left is again the additive CA. **This is what "citation
buys replication on the line" looks like in its cheapest form, and it is worth
naming as cheap.** THE PRECEDENT (§3.2) is the version that is not.

### 3.6 THE ENGROSSING CLERK — the rung-4 property, in the citation sector

*2-D · 8 kinds · occupancy **and** citation guards · parity.* The first object
in this program that **reads**.

```python
X,Y,U,V,A,B,P,Q = range(8);  O,N,E = (0,0),(0,1),(1,0);  INERT = (O,O,O)
CLERK = Const([INERT]*4 + [(O,N,O), (O,N,E), (O,N,N), (O,N,N)],
              targets=[(X,),(Y,),(U,),(V,), (A,B,P,Q),(A,B,P,Q), (U,),(V,)],
              dim=2,
              guards=[(None,None)]*4 + [(None,None),(None,None),
                                        (X,None),      # P CITES kind X here
                                        (Y,None)])     # Q CITES kind Y here
# seed: blueprint over kinds X,Y on row 0; the clerk {A,B,P,Q} on its first cell
```

`X, Y, U, V` are **dead letters** — rule `(O,O,O)` asks for occupancy and
vacancy of the *same* cell, so they are never active: inert terrain. `A` clears
the clerk from its own cell, `B` re-enacts it one cell east; `P` and `Q` are
the citation clauses, each firing only if a law **of a named kind** stands in
the clerk's own cell, and each writing a **different** kind one row north.

```
   t=0  .......      t=2  .UV....      t=4  .UVVU..
        .#YYX..           .XY#X..           .XYYX#.
```
blueprint `0110` (X,Y,Y,X) → built row `UVVU`. Verified on both engines for
blueprints `0, 1, 01, 10, 0110, 1001, 111000, 0101010101, 1101001110`:
**the built pattern is a function of the blueprint, not of the constitution.**

That is exactly the defining half of rung 4 — *build a specified target from a
blueprint carried in the body* — for the target class "one row of symbols". It
is **not** rung 4 as a whole: the constructor is not universal over target
shapes, and the blueprint does not describe the clerk. Labelled **rung 4
(partial)** and nothing more.

### 3.7 THE SCRIBE — unbounded heritable copying (18 kinds, citation)

Add end markers `L`, `Z` and a mirror-handed clerk. The right-handed clerk
walks the blueprint copying every symbol **by name** one row up; on citing `Z`
in its own cell it halts (a citation in a *vacancy* clause) and enacts a
**left**-handed clerk on the fresh row, which walks back and does the same.

```
 t= 0  |.#XYYZ..|     t=10  |.#XYYZ..|     t=18  |...YYZ..|
                            |.LXYYZ..|           |.L#YYZ..|
                            |.LXYYZ..|           |.LXYYZ..|
                                                 |.LXYYZ..|
                                                 |.LXYYZ..|
```

Generation `k` occupies row `k` and carries an **exact** copy of the original
blueprint, for every `k`; verified for 7 blueprints × 6 generations on both
engines. The number of exact copies of the blueprint grows without bound.

Honest accounting: the *blueprint* is copied unboundedly (rung 3-**embedded**:
the rows are adjacent, so the copies are not free), while the *machine* is
never duplicated — exactly one clerk exists at any time, each birth coinciding
with its parent's death. So THE SCRIBE is a **puffer whose head is a
blueprint-carrying machine and whose wake is exact copies of the blueprint**,
not a replicator in the sense of §1.2. It is reported because it is the closest
this expedition came to von Neumann's architecture, and because saying where it
falls short is the point.

---

## 4. The published fauna, run through the detector

`python3 fauna.py`. "embedded" = largest family of support-disjoint translated
copies of the seed (rung 1); "free exact" = largest family of causal components
each an exact translate (rung 2/3). `Φ≠L` counts steps where the guarded map
differs from the unconditional linear one.

| specimen | sector | card growth | embedded | free exact | Φ≠L | rung |
|---|---|---|---|---|---|---|
| colonizer, 4-law block | ch.1 | 4→44 | 11 | **0** | 37/40 | 1 |
| colonizer, 1 law | ch.1 | 1→41 | 41 | **0** | 35/40 | 1 |
| **Pascal column** | ch.1 own-kind | 1→8 | 64 | **16** | 0/70 | 3 (degenerate seed) |
| Jubilee Code | ch.1 own-kind | 3→6 | 0 | 0 | 200/200 | 0 |
| sunset clause | ch.1 | 1→1 | 2 | 0 | 39/40 | 0 |
| LAND GRANT | ch.2 multi-target | 1→1681 | 41 | **0** | 35/40 | 1 |
| SOWER | ch.2 | 1→861 | 41 | **0** | 35/40 | 1 |
| CIRCUIT COURT (rake) | ch.2 | 2→98 | 0 | 0 | 0/48 | 0 |
| ASSIZE (gun) | ch.2 | 1→51 | 0 | 0 | 46/48 | 0 |
| ITINERANT COURT (puffer) | ch.2 | 2→50 | 0 | 0 | 47/48 | 0 |
| 1-D RAKE | ch.2 | 2→130 | 0 | 0 | 0/64 | 0 |
| 1-D GUN | ch.2 | 1→67 | 0 | 0 | 62/64 | 0 |
| PICKET PUFFER | ch.2, OR | 2→106 | 19 | **0** | 63/64 | 1 |
| TANDEM-1 glider | ch.2 | 2→2 | 0 | 0 | 0/40 | 0 |
| **THE MOOT** | this expedition | 4→60 | 84 | **21** | 0/140 | 3, additive |
| **THE SPLIT DECISION** | this expedition | 4→284 | 210 | **71** | 137/140 | **3, non-additive** |
| **THE QUORUM** | this expedition | 2→16 | 128 | **32** | 140/140 | **3, non-additive** |
| **THE PRECEDENT** (1-D) | this expedition | 4→11 | 2 | **2** | 140/140 | **2, non-additive** |
| **THE ENGROSSMENT** | this expedition | 4→32 | 128 | **32** | 140/140 | **3, non-additive** |

Three things to read off this table.

1. **The mission's own suspicion was right and needed saying.** The Pascal
   columns do qualify — at rung 3, no less — but with a one-law seed, and with
   the guard never biting once. Dressed honestly they are Fredkin additive
   self-reproduction in a 2-D own-kind law, nothing more.
2. **The area-fillers are rung 1 and not rung 2.** LAND GRANT contains 41
   disjoint copies of its own seed at `t = 40` and **zero** free ones: a solid
   square contains translates of any sub-block, which is precisely the cheat
   clause 1.4(a) was written to catch. Same for SOWER and for the colonizer.
   *The published growers are not replicators.*
3. **Guns, rakes and puffers are rung 0.** A rake lays copies of its *payload*,
   never of its *head*; the detector, which only ever looks for copies of the
   seed, records 0. This is the sharp form of the mission's hypothesis that "a
   rake that lays copies of its own head is a replicator": no such rake exists
   among the published specimens.

---

## 5. The search — exact scope

Every number below is a **box statement**. Per the width correction: a bounded
search decides a box, never a question, and none of these say "impossible".

### 5.1 ℤ, occupancy guards — **complete**, and **empty**

`sweep1d.py --span 3 --steps 60 --cardcap 300 --modes parity,or,super,super_or`

| | |
|---|---|
| kinds | 2 |
| offsets | `a,b,c ∈ {−1,0,1}` — all 27 rules per kind, all 729 pairs |
| targets | `T₀,T₁ ∈ {{0},{1},{0,1}}` — all 9 combinations |
| guards | occupancy (`g=h=any`) |
| constitutions | **6 561, complete** |
| modes | parity, OR, supersession, supersession-OR (all 4) |
| seeds | all codes of span ≤ 3 with both end cells occupied and ≥ 2 cells: **45** |
| budget | 60 steps, card cap 300, exact-recurrence cut |
| total runs | **1 180 980** |
| **hits: any `t ≤ 60` at which ≥ 2 causal components are exact translates of the seed** | **0** |

The zero is for the *debris-allowed* version too: not one state in the box
splits into two causally separated components both equal to a translate of the
seed, with or without further debris components.

**My rung 2 is stricter than the mission's literal statement, deliberately.**
Under the literal reading — `Φ^p(S) ⊇ σ^{d₁}S ∪ σ^{d₂}S`, supports disjoint,
gap > 2R, debris empty-or-periodic — the same 1-D box yields **46 086** hits.
Every one of them is the clause-1.4(a) artefact: a growing solid block of
identical laws contains a translate of any sub-block of itself at any spacing
you like, and the "debris" between the two copies is just more block (minimum
debris 2, never zero, and never periodic — it grows). Requiring the copies to
be whole *causal components* is what kills this, and it is the only formulation
I found that does.

### 5.2 ℤ, citation guards — **complete**, and full

`sweep1d.py --span 2 --steps 60 --cardcap 300 --modes parity,or --cite`. The
same constitutions as §5.1 but with every citation guard: `(g,h) ∈ {any,0,1}²`
per kind, **81 guard pairs per constitution**, so 729 × 9 × 81 = 531 441
constitutions × 2 modes = **1 062 882 tasks, complete**; seeds of span ≤ 2 with
both ends occupied (9 of them); 9 565 938 runs.

| | |
|---|---|
| hits (≥ 2 exact-translate causal components) | **72 832** |
| of which debris-free — **rung 2-exact** | **71 784** |
| distinct (constitution, mode) with an exact hit | 70 008 |
| exact hits whose constitution **cites a kind** | **71 784** |
| exact hits with **pure occupancy guards** | **0** |

That last pair of rows is the cleanest result of the census, because both are
measured **inside one box**: the occupancy corner of the citation box —
`g = h = any` throughout, which is exactly chapters one and two — contributes
**zero** of the 71 784 replicators, and every other corner contributes. In this
box, **citation is the enabling ingredient of replication on the line.**
Prediction Y5 named the citation sector; on ℤ it is not merely a place where
replicators happen to be, it is the only place in the box where they are.

Two cautions kept explicit. (i) At span ≤ 2 only ~1 % of the exact hits are
non-additive (sampled 128, `p ≤ 16`): the overwhelming majority are the cheap
vacuous-guard construction of §3.5. The non-additive 1-D specimen THE PRECEDENT
needs a **span-3** seed and was found in a separate, partial span-3 run
(360 000 of 1 062 882 tasks dispatched in enumeration order, 52 489 hits,
`data/sweep1d_cite.txt`) which was abandoned unfinished — its figures are a
prefix, not a box. (ii) §5.1 and §5.2 differ in seed span (3 vs 2) as well as
in guards; the span-3 occupancy box is the larger of the two and is still
empty, so the contrast is not an artefact of the seed set.

### 5.3 ℤ², random sampling of the Moore box

`sweep2d.py`. Constitutions drawn uniformly: each kind's `(a,b,c)` from the 9
Moore offsets (729 rules per kind), target set a uniform nonempty subset of the
kinds, mode uniform from the list, guards occupancy or (with `--cite`) uniform
over `{any}∪K` in both positions. Seeds: **all** mask assignments on nine fixed
cell-shapes (single cell; the three dominoes; the two spaced dominoes; two
trominoes; the square) — **183 seeds** at 2 kinds. Budget 40–48 steps, card cap
400, exact-recurrence cut.

| run | kinds | modes | constitutions sampled | seeds each | runs | rung-2 exact hits | of which guard-driven |
|---|---|---|---|---|---|---|---|
| `data/t2d.txt` | 2 | parity, OR | 4 000 | 183 | 732 000 | 1 900 (1 299 with ≥2-cell seeds) | 710 |
| `data/s2d_occ.txt` | 2 | all 4 | 60 000 | 183 | 10 980 000 | 41 166 | 29 076 |
| `data/s2d_cite.txt` | 2 + citation | parity, OR | 60 000 | 183 | 10 980 000 | 30 345 | 16 769 |

("guard-driven" = `Φ^t ≠ L^t` for some `t ≤ p`; the stricter splitting test is
sampled below.) A 3-kind run was started and abandoned as too slow to finish
within this cycle; nothing is reported from it.

Rung-2 exact replicators are **common** in 2-D. Distinct (constitution, mode)
pairs carrying at least one: **10 931 of 60 000** occupancy-guarded (about 1 in
5.5) and **7 737 of 60 000** citation-guarded (1 in 7.8); 34 599 of the 41 166
occupancy hits have a ≥2-cell seed. That is the opposite of what the complete
1-D occupancy box says. Put §5.1, §5.2 and §5.3 side by side and the shape of
the answer is: **on ℤ, replication needs citation (occupancy box: 0 of
1 180 980 runs; citation box: 71 784 replicators, every one of them citing);
in ℤ² it needs neither citation nor an exotic resolution — plain occupancy
guards and parity already give it, in about one sampled constitution in five.**
Dimension is what makes replication ordinary; citation is what makes it
possible at all on the line.

How many of them are genuinely non-additive (splitting test N2, on the seed's
own splittings, at the first exact event) — measured on random subsamples,
`p ≤ 16`:

| population | sampled | non-additive |
|---|---|---|
| `s2d_occ.txt`, parity/OR | 182 | 23 (**13 %**) |
| `s2d_occ.txt`, supersession / supersession-OR | 183 | 3 (2 %) |
| `s2d_cite.txt`, constitutions that actually cite a kind | 201 | 34 (**17 %**) |
| `t2d.txt` (parity/OR), scored exhaustively by `rank.py` | 1 299 | 371 (**29 %**) fail N2 *and* differ from `L` at the event |

Non-additive replication is therefore not a freak: it is a **substantial
minority** of the 2-D replicators, in the founding occupancy-guard semantics,
under ordinary parity resolution. Supersession is the sector where replication
is most common and least often non-additive.

---

## 6. The linear / non-linear question

The mission asked for a theorem of the shape *"replication in nomodynamics is
exactly additive replication unless out-degree ≥ 2 / citation is used."*
**That conjecture is refuted, and the reason it is tempting is itself worth
stating.**

### 6.1 What is true — [E]

- **Given occupancy, the per-kind dynamics is `𝔽₂`-linear** (Single-Author
  Lemma, `README.md`; Cryptic Unipotency, `xtheory/RESULTS.md` T6). The
  nonlinearity of nomodynamics lives *entirely in the guard*: `occ(i)` is an OR
  over kinds, and the active set is an AND-NOT of two occupancy bits.
- **Superposition at range is free** (Lemma S, §2.2). Any two sub-codes farther
  apart than `2R` superpose exactly, in every mode. So the fact that a
  replicator's two copies evolve independently after fission says **nothing**
  about additivity.
- **Unconditional superposition is false**, and grossly so. Measured here on
  4 000 random overlapping pairs each (`linearity_report(..., seed=1)`):
  colonizer `(0,1,1)` **2 046** failures; sunset `(0,−1,1)` 2 046; TANDEM-1
  1 894; MIRROR 1 604; PICKET PUFFER (OR) 1 936; THE ENGROSSMENT 503; THE
  SPLIT DECISION 412; **THE MOOT 505**. There is no `𝔽₂`-linearity theorem in
  this program that is not conditioned on frozen occupancy, and there could not
  be.

  That last entry is the one to stare at. **THE MOOT's constitution is
  thoroughly non-linear as a map, and its replicator is nevertheless perfectly
  additive**, because the orbit of *that seed* never leaves the region where
  every guard passes. So a random-pair superposition test (N3) tells you about
  the constitution and says nothing about the replicator; only N1 and N2, which
  look at the orbit and at the seed's own splittings, decide whether a given
  replication event is Fredkin's phenomenon or not. Reporting N3 alone would
  have made every specimen here look "nonlinear", which would have been
  worthless.

### 6.2 What is refuted — [M], with certificates

The interesting question is not "is `Φ` linear" (it is not) but "**is the
replication event itself explained by additivity?**" — i.e. does the seed's
doubling reduce, by superposition, to the doubling of its parts? For a Fredkin
replicator it does, and that is the whole content of "additive
self-reproduction". Result:

| specimen | dim | sector | guard bites? | `Φ = L`? | splitting test | verdict |
|---|---|---|---|---|---|---|
| Pascal column | 2 | own-kind | never | yes, 0/70 | — (1-law seed) | **additive** |
| THE MOOT | 2 | multi-target | never | yes, 0/200 | 0 / 10 fail | **additive** |
| 1-D phantom citation | 1 | citation | never | yes, 0/200 | 0 / 10 fail | **additive** |
| **THE SPLIT DECISION** | 2 | citation, OR | yes | no, 136/139 | **8 / 10 fail** | **non-additive** |
| **THE QUORUM** | 2 | supersession-OR | yes | no | **2 / 2 fail** | **non-additive** |
| **THE PRECEDENT** | 1 | citation, out-degree 1 | yes | no, 200/200 | **10 / 10 fail** | **non-additive** |
| **THE ENGROSSMENT** | 2 | multi-target, occupancy | yes | no, 140/140 | **8 / 10 fail** | **non-additive** |

The witness for THE ENGROSSMENT (§3.1) is the sharpest object this expedition
produced: remove one placed law from the four-law seed, evolve the two pieces
separately for four steps, XOR them — and **the child is simply absent**. The
copy is manufactured by the four laws acting jointly; it is not the sum of
anything.

Note also what *does* survive the transition: the copy count of THE ENGROSSMENT
is `2^popcount(t/4)`, the textbook Fredkin/Pascal signature — in a system where
superposition fails at every step. **`2^popcount` is a signature of the
light-cone-plus-doubling geometry, not of `𝔽₂`-linearity.** Anyone diagnosing
"additive replication" from a population curve should stop.

### 6.2b What is, and is not, new here about additive replication

Stated plainly, because the mission asked for it plainly.

**Not new.** Self-reproduction in additive cellular automata is classical:
Fredkin's replication in `𝔽₂`-linear rules, Amoroso–Cooper, Ostrand's
generalisation, the Pascal-mod-2 / Sierpinski population law `2^popcount(t)`.
THE MOOT (§3.3) is elementary **Rule 150** wearing law-space clothes; the
Pascal column (§3.4) is the same phenomenon in the own-kind sector; the
phantom-citation replicator (§3.5) is Rule 150 again, on ℤ, with a guard
disabled by construction. That these exist inside nomodynamics is a fact about
the *embedding* of additive CA into law-space, not a fact about self-amending
law. The repo already recorded the population law; what it had not recorded is
that the two surviving laws at `t = 2^k` are two disjoint free copies of the
seed. That is a small addition, and it is additive replication and nothing
more.

**New.** (i) A replicator whose replication event is *not* a superposition of
its parts (THE ENGROSSMENT, THE PRECEDENT), certified by the splitting test
with an explicit witness in which removing one law of four aborts the child
entirely. (ii) The measurement that such replicators are a substantial minority
of all 2-D replicators rather than a curiosity. (iii) The complete 1-D
occupancy box being empty while the 1-D citation box is not. (iv) Theorem A
and Corollaries A1–A2. (v) The observation that the `2^popcount` population law
is *not* diagnostic of additivity, which retires the obvious shortcut for
telling the two apart.

### 6.3 Where additivity does come from, when it comes — [P]

Every additive specimen found here is additive for the same reason: some cell
in every law's *vacancy clause* is unreachable, so the guard can never fail
and `Φ` collapses to `L`. Three ways to arrange it, in increasing cheapness:

1. the orbit stays on a lower-dimensional slice and the vacancy offset points
   off it (THE MOOT, the Pascal column: `b` = east/north of a line-supported or
   column-supported orbit);
2. the vacancy clause cites a kind that is present nowhere in the orbit;
3. the vacancy clause cites a **phantom** kind, one that is never seeded and is
   nobody's target (§3.5) — the guard is then vacuous by construction and the
   system *is* an additive CA wearing nomodynamic clothes.

**Proposed statement, [P]:** *a nomodynamic replicator is additive iff its
orbit is guard-free — every placed law active at every step. Additive
replication in nomodynamics is exactly the image of Fredkin's phenomenon under
the embedding of unguarded additive CA into law-space.* The forward direction
is immediate (guard-free ⟹ `Φ = L` on the orbit ⟹ additive). The converse is
not proved here and is the natural next theorem.

---

## 7. Verdict

**Highest rung actually reached: RUNG 3** — an unbounded colony of pairwise
free, exact, debris-free copies — reached in both an additive form (which is
the known Fredkin phenomenon) and a non-additive one (which is not).

- **Rung 1** — reached, and cheap, exactly as the mission suspected. The Pascal
  columns qualify; so do LAND GRANT, SOWER and the PICKET PUFFER; so does a
  plain colonizer block. Rung 1 is not evidence of anything: a growing solid
  region contains translates of any sub-block of itself.
- **Rung 2 (exact)** — reached, with certificates on two engines, by **THE
  ENGROSSMENT** (`Φ⁴(S) = S ⊔ σ^{(4,4)}S`, gap 4 > 2R = 2, debris ∅, 2-D,
  occupancy guards, parity), by **THE QUORUM** (the same at
  `σ^{(4,−4)}` from a seed of *two* placed laws, under supersession-OR), by
  **THE SPLIT DECISION** (`Φ²(S) = σ^{(0,−2)}S ⊔ σ^{(0,2)}S` — a true binary
  fission in which the parent does not survive, citation guards, OR), and by
  **THE PRECEDENT** on ℤ (`Φ⁸(S) = S ⊔ σ⁵S`, gap 3 > 2R = 2, debris ∅,
  citation guards). All four are non-additive.
- **Rung 3** — reached: **THE SPLIT DECISION** is exactly `t/2 + 1` free exact
  copies at every even `t` (100 of them at `t = 198`), THE ENGROSSMENT reaches
  64 at `t = 252` (`2^popcount(t/4)`), THE MOOT 85.
  Reached in the *only* sense in which it can be reached: the mission's
  "exponential colony" is **provably empty in every dimension** (Corollary A1),
  and no fixed-period doubling can survive (Corollary A2). The two specimens
  show the two ways out. THE ENGROSSMENT keeps doubling but its doubling period
  doubles too (`t = 4(2^k − 1)`, the copies colliding in between). THE SPLIT
  DECISION never doubles at all: it adds exactly one copy every two steps, so
  the colony is linear in `t` from the start and never has to break down.
- **Rung 4** — **not reached**, as pre-registered. What was built is its
  defining half: **THE ENGROSSING CLERK**, an 8-kind citation machine that reads
  a blueprint written in its own body and constructs a *different, decoded*
  target pattern determined by that blueprint (verified for 9 blueprints on two
  engines). And **THE SCRIBE**, 18 kinds, copies an arbitrary blueprint
  faithfully for generation after generation without bound. Neither ever holds
  two complete copies of its own machinery at once: in THE SCRIBE exactly one
  clerk exists at any time, each birth coinciding with its parent's death. That
  is precisely the gap between a transcriber and a von Neumann constructor, and
  it is not closed here.

**On the mission's central warning.** Additive replication is a known
phenomenon and the Pascal columns are an instance of it — and I found that
instance, confirmed it is additive by direct test (`Φ = L` at every step, zero
guard-blocks), and set it aside as **degenerate** under my own pre-registered
one-law clause. What is new here is not the additive replicator. It is:

1. that the guarded, non-additive sector contains replicators at all
   (§3.1, §3.2 — with the splitting-test witnesses);
2. that they are common in 2-D (13 %–29 % of rung-2 hits in the sampled boxes)
   and, in the complete window-1 occupancy box, **absent on the line**;
3. that `2^popcount` growth is not a signature of additivity;
4. Theorem A and its two corollaries, which change what rung 3 can mean.

### 7.0 Why THE SCRIBE stalls, exactly — and what rung 4 would cost

It is worth being precise about the obstruction, because it is structural and
not a shortage of cleverness.

**Observation C — [E].** Every law writes within `R` of itself, so a child
assembled by *writing into an adjacent region* sits at sup-distance ≤ R from
its parent and the two are not free at the moment of construction (Lemma S's
threshold is `2R`). They can only become free later, by one of them moving away
— and moving a finite pattern `k` cells takes at least `k/R` steps of genuine
transport. **So a constructor that builds its child next door reaches rung 2
only if parent or child subsequently travels.** Replication with a causal gap
requires **transport** on top of copying; copying alone never suffices. In THE
SCRIBE neither the parent's blueprint nor the child's ever moves, so the two
stay one row apart forever and the pair is never free — which is exactly what
the detector reports.

That is the whole distance between §3.6–3.7 and rung 4. THE SCRIBE has the
information half of von Neumann's architecture (an arbitrary heritable tape,
copied faithfully, with the copying machinery regenerated each generation) and
none of the transport half. THE ENGROSSMENT has the transport half (its child
appears four cells away, free) and none of the information half (its "genome"
is four fixed laws). **A rung-4 object in nomodynamics is these two glued
together: a blueprint-carrying packet that travels.** Chapter two says the
travelling requires out-degree ≥ 2, chapter three says the reading requires
citation; nothing found here forbids the combination, and I did not build it.
That is the sharpest open problem this expedition leaves.

### 7.1 The strongest single claim

> There is a two-kind, window-1, occupancy-guarded, parity-resolved
> constitution on ℤ² and a four-law seed `S` such that `Φ⁴(S)` is **exactly**
> `S` together with a causally separated translate of `S`, with no debris; and
> for 8 of the 10 ways of splitting `S` into two parts,
> `Φ⁴(S) ≠ Φ⁴(A) Δ Φ⁴(B)`. **Self-reproduction in nomodynamics is not confined
> to the additive sector.**

### 7.2 What would falsify or sharpen this

The converse of §6.3 — *additive ⟹ guard-free orbit* — is unproved. If it is
false, some replicator is additive for a reason other than a vacuous guard, and
the clean dichotomy dissolves. And §5.1's emptiness is a **box** result: a
window-1, 2-kind, span-3, 60-step box on ℤ. The chapter-two MIRROR warning
(gliders of span 616 invisible to every published box) applies here verbatim.

---

## 8. Scorecard against the pre-registration

| prediction | conf. | outcome |
|---|---|---|
| **Y5** (`CITATION.md`, frozen before chapter three): *a replicator exists in the citation or multi-target sector* | 0.4 | **CONFIRMED.** Both sectors, in fact: THE ENGROSSMENT (multi-target, no citation) and THE PRECEDENT (citation, out-degree 1). |
| **Y-C-1** rung 1 cheap; Pascal columns qualify | 0.85 | **CONFIRMED**, and they overshoot to rung 3 — with a one-law seed, so excluded by my own clause 1.4(b). |
| **Y-C-2** rung 2 reachable | 0.5 | **CONFIRMED, and badly under-confident.** Rung 3, not rung 2; ~1 in 5.5 sampled 2-D constitutions carries one. |
| **Y-C-3** exponential rung 3 impossible | 0.95 | **CONFIRMED and upgraded to a theorem** (Cor. A1), with a quantitative companion (Cor. A2) that the specimens visibly obey. The mission's rung 3 had to be rewritten. |
| **Y-C-4** rung 4 out of reach | 0.9 | **CONFIRMED.** Its blueprint half was built; the self-describing half was not. |
| **Y-C-5** the linearity question is really "sparse or in contact" | 0.8 | **Reframing CONFIRMED; the expectation inside it REFUTED.** I wrote "I expect the first specimens to be sparse". The first *designed* specimen (THE MOOT) was indeed sparse and additive — but the found population is 13–29 % non-additive, which I did not expect, and the headline specimen replicates *in contact*, with only half its laws active at `t = 0`. |

Kept as written: I predicted rung 2 at 0.5 and got rung 3 comfortably; I
predicted non-additive replication would be the hard case and it turned out to
be an ordinary case. Both misses were in the optimistic direction, which is
worth recording as a bias.

---

## 9. Reproducing

Python 3.11, no dependencies beyond the standard library.

```sh
python3 verify_replication.py        # 28 checks, ~20 s  -- THE point of entry
python3 verify_replication.py -v     # ... with spacetime frames
python3 replib.py                    # the two engines agree, 400 x 4 runs
python3 fauna.py                     # the published fauna vs the detector
python3 constructor.py               # THE ENGROSSING CLERK, 9 blueprints
python3 scribe.py                    # THE SCRIBE, 6 generations x 8 blueprints
python3 analyze.py                   # dossier format, on the Pascal column
```

The censuses (long):

```sh
# 5.1  complete 1-D occupancy box            (~25 s on 12 cores)   -> 0 hits
python3 sweep1d.py --span 3 --steps 60 --cardcap 300 \
        --modes parity,or,super,super_or --out data/sweep1d.txt

# 5.2  complete 1-D citation box        (~7 min on 12 cores)  -> 71 784 exact
python3 sweep1d.py --span 2 --steps 60 --cardcap 300 --modes parity,or \
        --cite --out data/sweep1d_cite2.txt
# ... and the abandoned span-3 prefix that produced THE PRECEDENT
python3 sweep1d.py --span 3 --steps 60 --cardcap 300 --modes parity,or \
        --cite --out data/sweep1d_cite.txt

# 5.3  2-D samples
python3 sweep2d.py --trials  4000 --kinds 2 --modes parity,or --steps 40 \
        --out data/t2d.txt
python3 sweep2d.py --trials 60000 --kinds 2 --steps 48 --seed 1 \
        --modes parity,or,super,super_or --out data/s2d_occ.txt
python3 sweep2d.py --trials 60000 --kinds 2 --steps 48 --seed 2 --cite \
        --modes parity,or --out data/s2d_cite.txt

# scoring a hit file against the strict definition + both additivity tests
python3 rank.py data/s2d_occ.txt.gz --top 20 --T 130
```

| file | contents |
|---|---|
| `replib.py` | the independent frozenset engine `pstep`, `certify`, causal components, the superposition tests |
| `analyze.py` | full dossier on one candidate: trajectory, certificate, guard audit, additivity audit, frames |
| `sweep1d.py` / `sweep2d.py` | the censuses |
| `rank.py` | scores a hit file: first exact event, colony size, `Φ` vs `L`, splitting test |
| `fauna.py` | the published fauna vs the detector (§4) |
| `constructor.py` | THE ENGROSSING CLERK (§3.6) |
| `scribe.py` | THE SCRIBE (§3.7) |
| `verify_replication.py` | re-checks every claim in this file |
| `data/` | hit files, gzipped (`zcat` them, or pass the `.gz` path straight to `rank.py`); the header line of each records its exact scope |

### Errata / cautions

- **Two compasses exist in this repo.** `xamend2d/xa2d.py` uses `N=(0,1)`;
  `verify.py` and `note/figs.py` use `N=(0,−1)`. §4's chapter-two specimens are
  entered with the `xa2d` table; the Jubilee Code with the `verify.py` table
  (the one matching its published crest list). Specimens defined here are given
  as literal offset tuples and are compass-free.
- Rung labels in §4 are **detector output**, not claims by the original
  expeditions: none of them claimed a replicator.
