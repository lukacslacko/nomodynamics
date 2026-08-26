# XAMEND-2D — The two-dimensional cross-amendment sector
### Expedition X-B, NOMODYNAMICS / Treeline program · 2026-08-26

**Verdict in one line.** The two structural numbers of a constitution —
*out-degree* (how many kinds a law amends) and *in-degree* (how many kinds may
author a given kind) — control the whole sector, and they control **different**
things. Out-degree 1 forces ray confinement (α ≤ 1) and **forbids gliders in
every dimension**; out-degree ≥ 2 opens both, and delivers **α = 2 with
bounding-box fill → 1** (the plane genuinely fills) and **the first free glider
of nomodynamics** — plus a gun, a rake, and a collision algebra. In-degree ≥ 2
is what breaks single-authorship: it is the exact condition for *balanced
constitutions* (which exist only under parity — never under OR, proved and
confirmed on 28.7 M runs) and it is *not* needed for non-2-adic periods, which
turn out to exist even in pure own-kind 2-D once diagonal offsets are allowed.

---

## 0. Headline results

| # | result | status |
|---|---|---|
| 1 | **α = 2 achieved.** `OPP>ABC OEE>B ONN>C` from ONE law fills a solid square: \|S_t\| = (t+1)² exactly, cell support = {(0,0)} ∪ [1,t]², **bounding-box fill → 1**. | proved + certified to t = 200 on an independent engine |
| 2 | **Generalised Ray-Confinement Theorem.** Every *single-target* constitution (own-kind, relay cross-amendment, supersession) confines its support to a fixed finite union of **parallel rays** of direction V = the cycle sum ⟹ α ≤ 1 in every dimension; V = 0 ⟹ bounded ⟹ eventually periodic. | proved (Thm 3 / Cor 3.1) |
| 3 | **THE WRIT OF REMOVAL** — `OEO>AB OEE>AB`, seed A+B at one cell: a **2-law free glider**, Φ(S) = σ^(1,0)(S). The first glider in nomodynamics, in *any* dimension. Diagonal variants Φ(S) = σ^(±1,±1)(S) exist — a direction own-kind 2-D provably cannot take. | certified over 5 periods on `xnomos.py` |
| 4 | **Potential-Anchor Theorem.** No glider exists whenever some u has ⟨d,u⟩ > 0 and ⟨V_Z,u⟩ > 0 for every reachable amendment cycle Z. Corollary: **single-target ⟹ no gliders, any dimension, parity/OR/supersession.** Machine-checked: of 4,782,969 complete 2-kind Moore universes, **0 single-target gliders**; all 8,769 certified gliders possess a **null amendment cycle** (V_Z = 0) — exactly the escape hatch the proof leaves open. | proved + complete enumeration |
| 5 | **A GUN and a RAKE.** `OEO>AB OEE>AB OEO>AB` from one pump law emits a Writ every 2 steps, forever. Adding a north-walking pump gives a rake: one glider dropped per step, \|S_t\| = 2t+2. | certified |
| 6 | **Collision algebra of writs.** Head-on: **even gap ⟹ mutual transparency** (they occupy one cell and pass through); **odd gap ⟹ mutual arrest** into a frozen 4-law block. A single inert law stops a writ dead. | complete gap sweep 1–14, certified |
| 7 | **Balance ⟺ two authors, and only under parity.** Φ(S) = S with an active law requires in-degree ≥ 2 *and* parity. Complete OR census: **0 balanced runs in 28,697,814**. Balanced codes are unbounded in size and can be **100 % active**: a column of n doubly-occupied cells under `OEO>A OEO>A` is fixed forever with all 2n laws active. | proved + z3-maximal witnesses |
| 8 | **The 2-adic period conjecture of own-kind nomodynamics is false.** Period 3 occurs in *pure own-kind* 2-D (`EQN>A TQS>B`, 3 laws) as soon as diagonal offsets are admitted. The full sector's period spectrum includes 3, 5, 6, 7, 10, 12, 14, 18, 20, 21, 24, 28, 30, 36, 40, 48, 56, 72, 96, 112, 192. | certified specimens |
| 9 | **THE ODOMETER** — `OEW>B NQR>AB`, three laws: a width-2 column that **counts in binary**. Card collapses to **four laws** at every t = 2^k and avalanches at t = 2^k − 1; reach ≈ 0.20 (log₂ t)², = 86 cells at t = 2²⁰. Bounded card, unbounded reach ⟹ aperiodic. The slowest clock in the fauna (the Jubilee code's reach is ≈ 1.5√t). | no recurrence in 300,000 hashed steps; 179 survivors of a 3-stage escalation |
| 10 | **Supersession is inert.** Complete 2-kind Moore + 3-kind sample under supersession, 36.7 M runs: **0 gliders**, in every class — as Cor. 4.2 requires. Its class-0 and class-1 tallies are identical entry by entry, because the semantics ignores the target map altogether. | complete enumeration |
| 11 | **The smallest glider is ONE LAW.** `OWO>ABC ORQ>A RER>BC`: Φ⁴(S) = σ^(−1,1)(S) with \|S\| = 1. And the largest certified is 50 laws moving diagonally at the speed of light. | certified |

---

## 1. Pre-registration (verbatim, written before the first census run)

See `PREREG.md`. Scorecard:

| claim | outcome |
|---|---|
| P1a single-target ⟹ α ≤ 1, zero counterexamples | **CONFIRMED** (proved; complete census agrees) |
| P1b multi-target reaches α = 2 by a "sower" | **CONFIRMED** — and beaten: fill → 1, not 1/2 |
| P1c a fractal band of intermediate α exists | **CONFIRMED** (see §5.3) |
| P2a no gliders under single-target | **CONFIRMED** (proved; 0/4.78 M universes) |
| P2b gliders only where cycle sums fail to fit an open half-plane | **CONFIRMED** — every one of 8,769 has a null cycle |
| P2c glider ≈ 25 %, rake ≈ 50 %, translating grower ≈ 70 % | **all three found**; I under-rated the glider badly |
| P3a odd periods appear under multi-target | **CONFIRMED** (3, 5, 7, 21, …) |
| P3b single-target stays 2-adic | **REFUTED** — 2,558 non-2-adic single-target runs, 77 of them *own-kind* |
| P4a balance impossible under single-target | **REFUTED** — 32,214 single-target balanced runs. The right condition is **in-degree**, not out-degree; I had confused the two axes. |
| P4b balance common and can be large | **CONFIRMED** — 51,972 runs, unbounded size, 100 % active |
| P4c balance fragile under perturbation | **CONFIRMED** — survives 9–43 % of single-law additions |
| P5 parity/OR split; higher under multi-target | **CONFIRMED**; and the split is *structural*: OR has no balance at all, parity has no subluminal gliders |

---

## 2. Setting and the two structural numbers

A **constitution** C on ℤ^d: a finite kind set K; each k ∈ K carries a rule
(a_k, b_k, c_k) with offsets in {−1,0,1}^d and a nonempty **target set**
T(k) ⊆ K. A **code** is a finite S ⊆ ℤ^d × K; occ_S(i) = 1 iff some kind
stands at i. A law (i,k) ∈ S is **active** iff occ(i+a_k) ∧ ¬occ(i+b_k). Every
active law emits, for each t ∈ T(k), one toggle of the slot (i+c_k, t).
Toggles at one slot resolve by **parity** (flip iff odd) or **OR** (flip iff
≥ 1). Φ is the synchronous update. Supersession is the variant in which an
active law of kind k enacts kind k at i+c_k if that cell is empty and
otherwise CLEARS the cell.

The **amendment digraph** G has vertex set K and an edge k → m with weight
c_k for each m ∈ T(k). Two numbers:

* **out-degree** |T(k)| — how many kinds one law amends. Own-kind is the case
  T = id. Out-degree 1 = "single-target".
* **in-degree** of m, |{k : m ∈ T(k)}| — how many kinds may *author* m.

Own-kind has out-degree ≡ in-degree ≡ 1, which is why the two axes were
invisible before. They are not the same axis: since Σ_m indeg(m) = Σ_k |T(k)|,
an out-degree ≥ 2 anywhere **forces** an in-degree ≥ 2 somewhere, but not
conversely. So the sector splits into three classes, used throughout:

* **class 0** — all out-degrees and all in-degrees 1 (the *permutation*
  constitutions; own-kind is the identity permutation, reciprocal amendment the
  transposition). Single-authorship holds: parity ≡ OR.
* **class 1** — all out-degrees 1, some in-degree ≥ 2 (single-target but
  multi-author: two kinds amending a third).
* **class 2** — some out-degree ≥ 2 (multi-target; automatically multi-author).

Class 1 is the gap between the two axes, and it is where the old intuition
breaks: it has balanced constitutions and semantics splits but, by Cor. 4.1,
still no gliders and still α ≤ 1.

Notation for constitutions: `abc>T` per kind, offsets
`O`=(0,0) `E`=(1,0) `W`=(−1,0) `N`=(0,1) `S`=(0,−1) `P`=(1,1) `Q`=(−1,1)
`R`=(1,−1) `T`=(−1,−1); targets as kind letters. E.g. `OEO>AB OEE>AB` is
the Writ of Removal. All specimens in this file are in that format and parse
with `xa2d.Const.parse`.

---

## 3. Theorems

### 3.1 Authorship controls linearity, not targeting

**Theorem 1 (Authorship Lemma).** *If every kind has in-degree ≤ 1 then, in
every state, every slot (j,m) receives at most one toggle. Hence parity ≡ OR
identically and no toggle can ever be cancelled.*

*Proof.* The laws that can toggle (j,m) are exactly the laws (j − c_k, k) with
m ∈ T(k). In-degree(m) ≤ 1 leaves one such k, and at most one law of kind k
stands at the single cell j − c_k. ∎

This is the correct generalisation of the Single-Author Lemma
(`nomos2d/RESULTS.md` Lemma 1, `glider-question/RESULTS.md` Lemma 1): own-kind
satisfies it because T = id makes in-degree ≡ 1, **not** because out-degree is
1. A *single-target* constitution can perfectly well have a kind of in-degree 2
— two different kinds both amending a third — and then parity and OR come
apart. That is exactly what the census finds (class 1, §6).

*Machine check (complete enumeration):* under parity and under OR the class-0
verdict tallies are **identical, entry by entry**, across all 6,377,292
class-0 runs of the 2-kind Moore census (extinct 10,274 / fixed 4,782,945 /
cycle 1,099,745 / escape 433,907 / unresolved 50,421 / balanced 0 / glider 0);
class 1 and class 2 differ between the semantics.

**Theorem 2 (Dead Letter, generalised).**
1. *Under **OR** resolution, Φ(S) = S ⟺ no law of S is active — in every
   dimension, for every constitution. There are **no balanced constitutions
   under OR**.*
2. *Under parity, if every kind has in-degree ≤ 1, the same holds.*
3. *Hence a balanced constitution (Φ(S) = S with ≥ 1 active law) requires
   **parity** resolution **and** a kind of in-degree ≥ 2. Its smallest witness
   has 2 placed laws.*

*Proof.* (1) Under OR a slot receiving ≥ 1 toggle flips, hence changes; so one
active law already forces Φ(S) ≠ S. Conversely no active law ⟹ no toggle.
(2) By Theorem 1 multiplicities are ≤ 1, so parity ≡ OR; apply (1). (3) is the
contrapositive; and one law cannot balance because it emits a toggle nothing
cancels, so ≥ 2 laws are needed — attained (§6.1). ∎

*Machine check:* the complete 2-kind Moore census under OR returns **balanced =
0** in 28,697,814 runs; under parity it returns 51,972, **every one** of which
has a kind of in-degree 2.

### 3.2 Confinement: where laws can ever appear

For kinds k, m let the **displacement set** be
  D(k,m) = { c_{k_0} + … + c_{k_{r−1}} : r ≥ 0, k_0 = k, k_{s+1} ∈ T(k_s), k_r = m },
i.e. the set of weights of directed walks k → m in G.

**Theorem 3 (Displacement-monoid confinement).** *For every t and every kind m,*
  supp_m(S_t) ⊆ ⋃_{(i,k) ∈ S_0} ( i + D(k,m) ).

*Proof.* Induction on t. A slot (j,m) can enter S_{t+1} only by receiving a
toggle, which is emitted by an active law (j − c_k, k) ∈ S_t with m ∈ T(k). By
induction j − c_k ∈ i + D(k′,k) for some seed law (i,k′); hence
j ∈ i + D(k′,k) + c_k ⊆ i + D(k′,m). Slots that persist are covered by the
hypothesis, and deletions only shrink the support. ∎

**Corollary 3.1 (Generalised Ray Confinement).** *Suppose every kind has
out-degree 1 (own-kind, single-target cross-amendment, or supersession). Then G
is a functional graph. Let Z be the terminal cycle of the component of k, with
length L and cycle sum V_Z = Σ_{j ∈ Z} c_j. Then D(k,m) is contained in a
finite set together with finitely many arithmetic progressions of common
difference V_Z. Consequently*
* *supp(S_t) lies in a **fixed finite union of parallel rays of direction V_Z**
  (plus a finite set): **α ≤ 1**. Sharply: a law reached after r amendment
  steps cannot exist before time r, and out-degree 1 makes r ↦ (kind, offset)
  a function, so |S_t| ≤ |S_0|·(t+1) — in **every dimension**;*
* *if V_Z = 0 the support is **bounded**, so the orbit lives in a finite state
  space and is eventually periodic.*

*Proof.* With out-degree 1 the walk out of k is unique: k, t(k), t²(k), …, so
D(k,m) = { D_r(k) : t^r(k) = m } with D_r(k) = Σ_{s<r} c_{t^s(k)}. After the
walk enters Z (within |K| steps) each further lap adds exactly V_Z, so the r
with t^r(k) = m form finitely many arithmetic progressions of step L and
D_{r+L} = D_r + V_Z. Finitely many rays of direction V_Z. Each step of Φ moves
nothing further than 1, so at time t only the first O(t) points of each ray are
reachable. ∎

For **supersession** creation is own-kind by definition (an active law of kind
k enacts kind k at i + c_k), so supp_k(S_t) ⊆ seed_k + ℕc_k — the strongest
form of the confinement.

This is the exact generalisation of `nomos2d` Theorem 3 that the mission asked
for, and it explains the §7 teaser there: the relay `ONE→B, OEN→A` has
V = c_A + c_B = (1,1), so it walks a *diagonal* staircase — a direction
own-kind cannot take — while its support is still a bounded-width union of
rays, hence α ≤ 1. **Solid 2-D growth is impossible for out-degree 1, in any
dimension, under parity, OR and supersession.**

### 3.3 The Potential-Anchor Theorem (no gliders)

A **free glider** is a finite nonempty S with Φ^p(S) = S + d, d ≠ 0.

**Theorem 4 (Potential Anchor).** *Let S_0 be a glider with displacement d, R
the kinds reachable in G from kinds(S_0), and 𝒵 the directed cycles of G|R.
Then there is **no** u with ⟨d,u⟩ > 0 and ⟨V_Z,u⟩ > 0 for all Z ∈ 𝒵.*

*Proof.* Suppose such u exists. Weight the edge k → m by w(k→m) = ⟨c_k,u⟩.
Every directed cycle of G|R then has strictly positive weight, so a potential
exists: choose 0 < ε < (min cycle weight)/(max cycle length); with w′ = w − ε
every cycle still has positive weight, hence w′-shortest paths from a
super-source are well defined; put s_m = −dist_{w′}(m), which gives
w(k→m) + s_k − s_m ≥ ε for every edge.

Define the potential of a slot: Ψ(j,k) = ⟨j,u⟩ − s_k. If (j′,m) receives a
toggle it comes from a law (j′ − c_k, k) with m ∈ T(k), and

  Ψ(j′,m) = Ψ(j′ − c_k, k) + ( w(k→m) + s_k − s_m ) ≥ Ψ(j′ − c_k, k) + ε.

So **every act of amendment strictly raises Ψ by at least ε.** Let
Ψ* = min{ Ψ(i,k) : (i,k) ∈ S_0 }. By induction on t: every law of S_t has
Ψ ≥ Ψ*, and every slot of potential ≤ Ψ* is untouched, because a toggle into it
would need an emitter of potential ≤ Ψ* − ε, which does not exist. Hence the
(nonempty) set of seed laws attaining Ψ* is **immortal**: present in S_t for
every t. But S_{np} = S_0 + nd and Ψ(i + nd, k) = Ψ(i,k) + n⟨d,u⟩ → ∞, so the
minimum potential over S_{np} tends to infinity. Contradiction. ∎

This is the Anchor Theorem of `glider-question/RESULTS.md` with the fixed
"leftmost law" replaced by a *potential-graded* anchor. Its hypothesis (H1)
"own-kind effects" is replaced by the much weaker "the amendment cycles all
point the same way".

**Corollary 4.1 (No free gliders under single-target).** *Out-degree 1 ⟹ no
glider, in every dimension, under parity and under OR.*

*Proof.* Let c be an amendment component meeting S_0, V_c its terminal cycle
sum. By Cor. 3.1 its laws live in (finite) ∪ (rays of direction V_c). If
V_c = 0 that region is finite and cannot contain S_0 + nd for all n. So
V_c ≠ 0, and since S_0 + nd must lie in the ray region for every n we get
d ∈ ℝ_{>0}·V_c. Take u = d: then ⟨d,u⟩ > 0 and ⟨V_c,u⟩ > 0 for every present
component. With out-degree 1 every reachable cycle *is* the terminal cycle of a
component, so 𝒵 is covered. Theorem 4 applies. ∎

**Corollary 4.2 (No gliders under supersession).** *Proof.* Creation is
own-kind, so supp_k ⊆ seed_k + ℕc_k; a drifting orbit forces c_k ≠ 0 and
d ∈ ℝ_{>0}c_k for every k ∈ kinds(S_0). Put Ψ(j,·) = ⟨j,d⟩. Creation of a slot
at j′ needs an active law at j′ − c_k (potential lower by ⟨c_k,d⟩ > 0), and —
crucially — *destruction* also does, because supersession clears the cell
i + c_k of an active law at i. So the minimum-Ψ laws can be neither created nor
destroyed; they are immortal, contradicting the drift. ∎

**Corollary 4.3 (Salient-cone no-go).** *If every reachable cycle sum is
nonzero and they all lie in one open half-space, there is no glider.*
*Proof.* Pick u₀ with ⟨V_Z,u₀⟩ > 0 for all Z. Fix a seed law (i,k). For every n
the law (i + nd, k) is in S_{np}, so by Theorem 3 there is a seed law (i′,k′)
with i + nd ∈ i′ + D(k′,k). Every walk weight in D(k′,k) is a tail weight (from
a finite set F, because a walk visiting no cycle has length < |K|) plus a
non-negative integer combination of reachable cycle sums. There are finitely
many seed laws and F is finite, so for large n we have
nd ∈ (bounded set) + cone{V_Z}, whence d ∈ cone{V_Z}\{0} and ⟨d,u₀⟩ > 0.
Apply Theorem 4. ∎

**Corollary 4.4 (Where a glider must live).** A glider needs out-degree ≥ 2 and
a reachable cycle Z with ⟨V_Z,u⟩ ≤ 0 for every u with ⟨d,u⟩ > 0. The minimal
such object is a **null cycle**: an amendment loop returning to its own kind
with zero net displacement.

*Machine check (complete enumeration).* Over all 4,782,969 two-kind Moore
universes × 6 canonical seeds × 2 semantics: **2,804 (parity) + 5,965 (OR)
certified gliders; 0 of them single-target; 100 % of them possess a null
amendment cycle; 0 of them admit a separating u** (checked over all u in
[−8,8]² for each). The theorem is not merely unrefuted — its escape hatch is
the *only* place gliders were found.

### 3.4 Area filling

**Theorem 5 (The Land Grant: α = 2, fill → 1).** *Let*
  A = (O, NE, NE) → {A,B,C},  B = (O, E, E) → {B},  C = (O, N, N) → {C}
*(`OPP>ABC OEE>B ONN>C`), seeded with the single law A at the origin. Then for
every t ≥ 0*
  S_t = {A@(s,s) : 0 ≤ s ≤ t} ∪ {B@(x,y) : 1 ≤ y ≤ x ≤ t} ∪ {C@(x,y) : 1 ≤ x ≤ y ≤ t},
*so |S_t| = (t+1)² exactly, the occupied cells are {(0,0)} ∪ [1,t]², the
bounding box is (t+1)×(t+1) and the fill fraction is (t²+1)/(t+1)² → 1.*

*Proof (sketch; the full induction is four lines per kind).* A at (s,s) is
active exactly at time s, because its b-guard NE is empty then and occupied
ever after; when it fires it enacts A, B and C together at (s+1,s+1). B at
(x,y) with y ≤ x is created at time x and fires once, at time x, enacting B at
(x+1,y) — that cell is empty at time x (nothing else reaches it earlier) and
occupied at time x+1, which blocks B at (x,y) forever. Symmetrically for C in
columns. Hence cell (x,y) with x > y ≥ 1 is filled at time x, cell (x,y) with
y > x ≥ 1 at time y, and (s,s) at time s. Counting: (t+1) A-laws on the
diagonal and t(t+1)/2 B-laws and t(t+1)/2 C-laws gives (t+1)². ∎

*Certificate:* `verify.py` A2 checks |S_t| = (t+1)² and the exact support for
t = 0..200 on `xnomos.py`.

**Corollary 5.1 (The α dichotomy is complete in 2-D).** Trivially
|S_t| ≤ |K|(2t+1)^d, so α ≤ d always. Combining with Cor. 3.1 and Theorem 5:

| out-degree | max α in ℤ² | max bounding-box fill |
|---|---|---|
| 1 (own-kind / relay / supersession) | **1** (theorem) | 0 (measure-zero: a finite union of rays) |
| ≥ 2 | **2** (attained) | **→ 1** (attained) |

The two-kind minimum for α = 2 is the **Sower** `OEE>AB ONN>B` from one law:
|S_t| = (t+1)(t+2)/2, a solid triangle, fill → 1/2. Three kinds buy the
remaining half.

---

## 4. Method and search scope

**Engines.** `xa2d.py` (exact dict engine + dense numpy engine + certificates)
and `xcensus.c` (bitboard census: 64 × 64 board with one guard row, the state
renormalised to min x = min y = 2 every step, avalanche-hashed for exact
FIXED / BALANCED / CYCLE / GLIDER certificates; a separate 256 × 260 and
640 × 650 board for growth-exponent measurement). Everything is exact integer
/ bit arithmetic; there is no floating point in the dynamics.

**Validation chain** (each link is an independent code path):
* `xa2d.py` dict engine ≡ `xnomos.py` — 4,000 random universes × 4 modes
  (parity / OR / super / super_or), state equality: **4,000/4,000**.
* `xa2d.py` numpy engine ≡ dict engine — 400 universes × 25 steps: **400/400**.
* `xcensus` (C) ≡ `xa2d.py` — 8,000 random 2- and 3-kind Moore universes ×
  2 semantics, agreeing on verdict, period, displacement, card and active-law
  count: **8,000/8,000** (repeated at 4,000, 3,000 and 2,000 after every
  subsequent change to the C source).
* α engine ≡ numpy engine — full size sequences |S_t| for t = 0..120 identical
  on 7 designed universes.
* **Every positive claim** in this file is re-certified in `verify.py` by
  `xnomos.py`, which this expedition did not write: **15/15 PASS**.

**Two bugs found and fixed during validation** (recorded because they are the
kind of thing that silently fakes results): (i) the first C board discarded
emissions landing one row outside the current extent, which turned growers into
false cycles; (ii) FNV-1a hashing of a sparse bitboard produced *exact*
collisions — two single-bit differences at the same bit position, separated by
a multiple of 4 multiplications, cancel identically mod 2⁶⁴ — which forged
"period-1" certificates for growing patterns. Both were caught by the
Python↔C duel, not by eyeballing.

**Complete enumerations.**
1. **2-kind Moore census.** All 9³ = 729 rules per kind × 729 × 9 target maps
   = **4,782,969 universes**, × 6 canonical seeds, × 2 semantics =
   **57,395,628 runs**, 300 steps, span cap 60, card cap 900. This is a
   *complete* enumeration of the 2-kind sector over the full Moore offset set
   {−1,0,1}² up to the seed family. (Seeds with only B are redundant because
   the universe set is closed under kind swap.)
2. **2-kind von Neumann census.** 125 × 125 × 9 = 140,625 universes × the same
   6 seeds × 2 semantics = 1,687,500 runs (a strict sub-case, kept as a
   cross-check of the Moore run).
3. **Growth-exponent sweep.** One α measurement per universe that produced any
   escaping run: **573,598 universes** measured on a 256 × 260 board over 120
   steps; every candidate with α ≥ 1.05 (34,584 of them) re-measured on a
   640 × 650 board over 300 steps.

**Samples** (explicitly not complete): the 3-kind sector (§7), the escalation
of the unresolved pool (§8), and the designed-specimen work (§5, §9), which is
construction, not search.


---

## 5. Mission 1 — the growth exponent α

### 5.1 The dichotomy

α is decided by **out-degree alone**, and the decision is complete:

| class | definition | α | fill of the bounding box |
|---|---|---|---|
| **0** | all out-degrees 1, all in-degrees 1 (permutation constitutions; own-kind is the identity case) | ≤ 1 (Cor. 3.1) | 0 |
| **1** | all out-degrees 1, some in-degree ≥ 2 | ≤ 1 (Cor. 3.1) | 0 |
| **2** | some out-degree ≥ 2 | **= 2 attained** (Thm 5) | **→ 1 attained** |

Note Σ_m indeg(m) = Σ_k |T(k)|, so out-degree ≥ 2 *forces* in-degree ≥ 2
somewhere: class 2 ⊂ multi-author. The converse fails — class 1 is exactly the
gap, and it is where the two axes come apart.

### 5.2 Census evidence for α ≤ 1 in classes 0 and 1

Every one of the 4,782,969 complete 2-kind Moore universes that produced an
escaping run had its growth exponent measured once (573,598 universes; a
256 × 260 board, 120 steps, least-squares slope of log|S_t| against log t over
the last two thirds). **Every universe with measured α ≥ 1.15 is class 2:
34,584 of them, and 0 from class 0 or class 1.** The per-class maxima are in
`cen_moore_parity_alpha.txt` (`ALPHA_CLASS` lines).

That is a complete enumeration of the 2-kind sector, and it agrees with the
theorem exactly.

### 5.3 What class 2 actually does

Short-window fits can exceed the trivial bound α ≤ 2 — a pattern trapped in a
*bounded* box can densify steeply for a while — so every candidate with a
stage-1 α ≥ 1.05 was re-run on a 640 × 650 board for 300 steps and split by two
independent tests (`refine2.py`):

* **power law**: |log₂(S₁₅₀/S₇₅) − log₂(S₃₀₀/S₁₅₀)| ≤ 0.15;
* **expanding**: the bounding box at t = 300 has a side ≥ 150.

Only runs passing both carry an asymptotic α; the rest are bounded-box
transients (they belong to §10, the cryptid pool, not here).

### 5.4 The designed area-fillers

**THE LAND GRANT** — `OPP>ABC OEE>B ONN>C`, seed `A@(0,0)` — Theorem 5:
|S_t| = (t+1)² exactly, cell support {(0,0)} ∪ [1,t]², bbox (t+1)×(t+1),
**fill = (t²+1)/(t+1)² → 1**. Measured at t = 300: |S| = 90,601 = 301²,
bbox 301×301, fill 0.993, octave exponent 1.990.

```
   t = 6                       the diagonal sower A walks NE and drops
   .CCCCC#                     B and C on every cell it takes;
   .CCCC#B                     B floods east along its row,
   .CCC#BB                     C floods north along its column,
   .CC#BBB                     and they meet on the anti-diagonal.
   .C#BBBB                     ('#' = two or more laws in one cell)
   .#BBBBB
   A......
```

**THE SOWER** — `OEE>AB ONN>B`, seed `A@(0,0)`, the two-kind minimum:
|S_t| = (t+1)(t+2)/2 exactly, a solid triangle, fill → 1/2, octave exponent
1.986 at t = 300. One law, one out-degree-2 clause.

The best fill found by *search* (as opposed to design) in the 2-kind sector is
0.679 (`OQP>B WEE>AB`, α = 2.04 at 300 steps, bbox 302 × 58) — the searched
strata are dominated by thin slabs; the solid quadrant had to be built.


---

## 6. Mission 2 — the first free glider

### 6.1 THE WRIT OF REMOVAL

```
constitution : OEO>AB  OEE>AB          (kinds A and B, both targeting {A,B})
seed         : A@(0,0)  B@(0,0)        (two laws, one cell)
certificate  : Phi(S) = sigma^(1,0)(S) — verified over 5 periods by xnomos.py
```
```
t=0  .#........      A: a=O b=E c=O -> {A,B}   repeals the pair where it stands
t=1  ..#.......      B: a=O b=E c=E -> {A,B}   re-enacts the pair one cell east
t=2  ...#......
t=3  ....#.....      '#' = both laws in one cell
t=4  .....#....
```

The mechanism in one sentence: **clause A repeals the entire code at its own
cell while clause B re-enacts the entire code next door.** The Anchor Theorem
of the 1-D expedition says *the eldest law cannot be repealed* — under
hypothesis (H1), own-kind effects. Cross-amendment with out-degree 2 breaks
(H1) exactly: the trailing law is repealed by a **different kind**, and the
potential argument of Theorem 4 fails precisely because the loop A → A has
c_A = O, a **null cycle**.

The same two clauses work verbatim in 1-D (`xnomos.Const([(0,1,0),(0,1,1)],
targets=[(0,1),(0,1)], dim=1)`, verified): **the Free Glider Question of
`glider-question/RESULTS.md` is answered affirmatively in the cross-amendment
multi-target sector, in every dimension ≥ 1.** In 2-D one gets more: replacing
c_B by a diagonal offset gives Φ(S) = σ^(±1,±1)(S) — motion in a direction that
own-kind 2-D provably cannot take (`nomos2d` Thm 3 pins every kind to an axis
ray).

### 6.2 The glider zoo (complete 2-kind Moore enumeration)

| | parity | OR |
|---|---|---|
| certified gliders | 2,804 | 5,965 |
| class 0 (permutation) | **0** | **0** |
| class 1 (single-target, multi-author) | **0** | **0** |
| class 2 (multi-target) | 2,804 | 5,965 |
| possessing a null amendment cycle | 2,804 (100 %) | 5,965 (100 %) |
| admitting a separating u (Thm 4 would forbid) | **0** | **0** |
| cards seen | 2, 4, 7 | 2, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15 |
| periods seen | 1, 2, 4 | 1, 2, 4 |
| speeds \|d\|_∞/p | **1 only** | 1 (5,869) and **1/2** (96) |
| distinct displacements | 24 | 19 |

Named specimens (all certified in `verify.py`):

* **card 7, p = 4** `OQW>B ORE>AB`, seed `A@(0,0) B@(1,1)`, core at t₀ = 10,
  d = (4,0). The largest parity glider in the 2-kind sector.
* **card 24, p = 4, d = (4,−4)** `OPR>AB ONQ>A`, seed
  `A@(0,0) A@(1,0) B@(0,1)`, OR semantics, core at t₀ = 19. A 24-law diagonal
  packet.
* **THE BREATHING WRIT** `OEW>AB ONE>A`, seed A+B at one cell, OR semantics:
  p = 2, d = (−1,0) — **subluminal**, half the speed of light. It inflates to
  three cells and collapses back. Under parity the same universe has no glider
  at all: the toggle OR keeps is exactly the one parity cancels.

**Luminality.** Every parity glider found travels at exactly speed 1 (the
offsets bound the speed by 1, so these are *luminal*). Subluminal gliders exist
only under OR, and only at speed 1/2. Whether a subluminal parity glider exists
is open (§11).

### 6.3 THE ASSIZE — a glider gun

```
constitution : OEO>AB  OEE>AB  OEO>AB       (C is a pump; nobody amends C)
seed         : C@(0,0)                       ONE law
```
```
t=0  C...........      C is immortal (in-degree 0) and fires whenever its east
t=1  #...........      neighbour is clear, enacting a fresh A+B pair on its own
t=2  ##..........      cell.  The pair walks off as a Writ; two steps later the
t=3  #.#.........      east is clear again and C fires again.
t=5  #.#.#.......
t=7  #.#.#.#.....      |S_t| = t + 3;  an infinite periodic stream of certified
t=9  #.#.#.#.#...      free gliders, spacing 2, from a single law.
```

### 6.4 THE CIRCUIT COURT — a rake (a gun that walks)

```
constitution : OEO>AB  OEE>AB  ONO>ABCD  ONN>CD
seed         : C@(0,0) D@(0,0)
```
C and D are a *north*-walking Writ; C's target set also contains A and B, so
the cell the pump vacates is left holding a fresh *east*-walking Writ. One free
glider is dropped per step, forever: |S_t| = 2t + 2, and the object is a
diagonal comb of receding gliders.

```
  t=8   #.......      the pump (top), and the writ dropped at height y
        #.......      is at x = t - 1 - y
        .#......
        ..#.....
        ...#....
        ....#...
        .....#..
        ......#.
        .......#
```

### 6.5 What the theorem buys

The hunt was not a sweep of the whole space hoping for luck: Corollary 4.4
says a glider needs a reachable cycle whose displacement sum cannot be
separated from d, and the cheapest such object is a **null cycle** — an
amendment loop that returns to its own kind with zero net displacement. Every
glider in the complete census has one. Designing one is then immediate: give a
kind the effect offset O and let it target itself and its partner.


### 6.6 Supersession: the theorem holds there too

Under **supersession** an active law of kind k enacts *its own* kind at i + c_k
when that cell is empty, and otherwise CLEARS the cell (all kinds); clear votes
resolve by parity. Creation is therefore own-kind whatever the target map says,
so Corollary 3.1 gives ray confinement and Corollary 4.2 forbids gliders.

Complete 2-kind Moore census under supersession (28,697,814 runs) plus a
1,000,000-universe 3-kind sample (8,000,000 runs):

| | supersession |
|---|---|
| gliders | **0 / 36,697,814** |
| classes 0 and 1 tallies | **identical entry by entry** (targets are ignored by the semantics — an internal consistency check) |
| balanced | 45,513 (2-kind) + 26,926 (3-kind) |

Supersession *does* have balanced constitutions, by a different mechanism: a
fixed point needs every active law to point at an already-occupied cell (so no
enactment fires) with the clear-votes cancelling in pairs. This needs two laws
of **different kinds** whose effect cells coincide, and it is independent of the
amendment digraph — which is why the class-0 and class-1 tallies coincide
exactly. Theorem 2 (balance ⟺ parity + in-degree ≥ 2) is a statement about the
cross-amendment semantics, not about supersession.


---

## 7. Interaction physics of the new fauna

All of §7 is exact and reproducible (`python3 gallery.py`); the constitution
`OEO>AB OEE>AB OWO>CD OWW>CD` carries an **east** Writ (A,B) and a **west**
Writ (C,D) in one universe.

**7.1 Head-on collision — the parity of the gap decides.** Complete sweep of
initial gaps 1…14:

| gap | outcome |
|---|---|
| even (2,4,6,8,10,12,14) | **mutual transparency**: the two packets occupy the *same* cell for one step (all four kinds stacked) and pass through each other undamaged, receding forever at combined speed 2 |
| odd (1,3,5,7,9,11,13) | **mutual arrest**: they halt adjacent as a frozen 4-law block, `[A B][C D]`, with **zero** active laws — plain gridlock, not balance |

This is the 2-D cross-amendment analogue of the own-kind *right-of-way
doctrine* (`nomos2d` §4): a tie means interpenetration. Here it is exact and
parity-graded — the writs are transparent to each other exactly when they can
meet on a cell rather than on a bond.

**7.2 Writ versus dead letter.** A single law of a kind nobody amends and whose
guard never passes (`OOO>E`, an inert *dead letter*) stops a Writ dead: the
writ marches up to it and freezes adjacent, at every offset tested (2…6).
Occupancy is the only currency, so **an unenforceable statute is a wall.**

**7.3 Gun output is a genuine glider train.** In `OEO>AB OEE>AB OEO>AB` the
emitted packets are pairwise non-interacting: spacing 2, all luminal, and the
stream is exactly periodic with period 2 at the pump.

---

## 8. Mission 3a — the period spectrum, and the death of the 2-adic conjecture

`nomos2d/RESULTS.md` records as an *observed regularity* that every exact cycle
in own-kind 2-D has period a power of 2, over ~140,000 seeds. That census used
the **von Neumann** offset set. It is false in the Moore window.

**Own-kind period 3** — `EQN>A TQS>B`, seed `A@(0,0) B@(1,1)`. Both kinds amend
only themselves: this is pure own-kind nomodynamics, in-degree ≡ out-degree ≡ 1,
parity ≡ OR. Certified: Φ³(S₁) = S₁, and Φ(S₁) ≠ S₁, Φ²(S₁) ≠ S₁.

```
 t=1     t=2     t=3     t=4=t=1
 .....   .....   .....   .....
 .....   .....   .A...   .....
 ..B..   .AB..   .AB..   ..B..
 .AB..   .A...   .AB..   .AB..
 card 3  card 3  card 5  card 3
```

Complete Moore census, class 0 (permutation constitutions = own-kind and
reciprocal amendment): **1,911 non-power-of-2 cycles**, of which 77 are
strictly own-kind (T = identity) with periods 3, 6, 12. So the 2-adic
regularity is an artefact of the von Neumann window, not of the algebra.

**The full period spectrum found** (2-kind Moore complete census, both
semantics, 6 canonical seeds):

| | periods observed |
|---|---|
| parity | 2, 3, 4, 5, 6, 7, 8, 12, 14, 16, 18, 24, 28, 30, 32, 36, 48, 56, 64, 72, 96, 112, 128, **192**, 256 |
| OR | 2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 18, 20, **21**, 24, 28, 30, 32, 36, 40, 48, 56, 64, 72, 96, 128, 256 |

with 9,379 (parity) / 4,927 (OR) non-power-of-2 cycles. Rarities, all
certified in `verify.py`:

| period | constitution | seed | card |
|---|---|---|---|
| 5 | `EWP>AB SWT>AB` | A@(0,0) A@(1,0) B@(0,1) | 3 |
| 7 | `ORP>B WES>B` | A@(0,0) A@(1,0) B@(0,1) | 5 |
| 21 (OR) | `OPE>B OSQ>AB` | A@(0,0) A@(1,0) B@(0,1) | 5 |
| 112 | `NTR>AB SPN>AB` | A@(0,0) A@(1,0) B@(0,1) | 111 |
| **192** | `OQP>B RTW>AB` | A@(0,0) A@(1,0) B@(0,1) | 3 |

**THE SESQUICENTENNIAL CLOCK** (`OQP>B RTW>AB`, three placed laws, period 192)
is the longest period in the complete 2-kind sector and the sharpest
counterexample to 2-adic clockwork: 192 = 2⁶·3.


### 8b. The 3-kind glider zoo — where the theorem's second escape hatch lives

The 2-kind sector is too small to separate the two ways Theorem 4 can fail.
A 2,000,000-universe **random sample** of 3-kind Moore constitutions
(reproducible splitmix64 stream, 8 canonical seeds, 16,000,000 runs per
semantics) gives:

| | parity | OR |
|---|---|---|
| gliders | 870 | 1,565 |
| class 0 / class 1 | **0 / 0** | **0 / 0** |
| with a null cycle | 866 | — |
| **without** a null cycle (opposed cycle sums) | **4** | — |
| admitting a separating u | **0** | **0** |
| speeds \|d\|_∞/p | 1, 1/2, 2/5, 1/3, 1/4, **1/6** | — |
| cards | 1, 2, 3, 4, 5, 6, 7, 9, 10, 13, 14, 18, **50** | — |

Both escape hatches of Corollary 4.4 are realised:

* **null cycle** (866/870) — e.g. the Writ family;
* **opposed cycle sums** (4/870) — e.g. `OPS>BC NRQ>A PRP>A`, cycle sums
  {(−1,0), (+1,0)}: no u can be positive on both, so no potential exists, and
  a glider is free to appear. Certified: Φ⁴(S) = σ^(−2,0)(S).

Three specimens worth naming (all certified in `verify.py`):

* **THE ONE-LAW GLIDER** `OWO>ABC ORQ>A RER>BC`, seed `A@(0,0)`:
  Φ⁴(S) = σ^(−1,1)(S) with **|S| = 1**. At every fourth step the entire code
  is a *single law*, one cell up and one cell left of where it was. The
  smallest glider the theory permits. Speed 1/4.
* **THE GRAND ASSIZE** `PQW>B ONE>AC ONP>ABC`, seed `A@(0,0) B@(0,0) C@(0,0)`,
  core at t₀ = 22: p = 4, d = (4,4), **card 50** — a fifty-law diagonal
  spaceship at the speed of light.
* **speed 1/6** `ONO>AB OEW>AC WTE>A`, seed A+B at one cell: p = 6,
  d = (−1,0), card 2. So *subluminal parity gliders exist* once there are
  three kinds; the 2-kind luminality is an artefact of the small sector.


---

## 9. Mission 4 — balanced constitutions in 2-D

A **balanced constitution** is a code with Φ(S) = S although some law is still
active: all the amendments enacted cancel by parity. `nomos2d` gives one 2-D
witness (§5 item 5); this section is the census and the extremal specimens.

### 9.1 The exact condition (Theorem 2)

Balance requires **parity** resolution and **in-degree ≥ 2** (two kinds that
can author the same kind). It does *not* require multi-target. Complete
enumerations:

| census | runs | balanced (parity) | class 0 | class 1 | class 2 | balanced (OR) |
|---|---|---|---|---|---|---|
| 2-kind Moore, 6 seeds (complete) | 28,697,814 | 51,972 | **0** | 32,214 | 19,758 | **0** |
| 2-kind vN, all 255 codes in a 2×2 box (complete) | 35,859,375 | 290,664 | **0** | 189,080 | 101,584 | **0** |
| 3-kind Moore, 2 M universes (sample) | 16,000,000 | 27,048 | **0** | 4,173 | 22,875 | **0** |

**Zero** balanced codes in class 0 and **zero** under OR, across 81.4 M runs of
each semantics — the theorem's two hypotheses are both necessary and both are
confirmed by exhaustion. Note that most balanced codes are **class 1**, i.e.
*single-target*: the phenomenon has nothing to do with multi-target, which is
precisely where the pre-registration (P4a) was wrong.

### 9.2 Minimal witness — 2 laws, one cell

`OEO>A OEO>A`, laws A and B stacked at one cell. Both kinds carry the rule
(a,b,c) = (O,E,O) and both amend **A**. Both are active whenever the east
neighbour is empty; each toggles the slot ((0,0),A); the two toggles cancel.
Two placed laws, and Theorem 2 says one is impossible — so this is minimal.

### 9.3 Balance is unbounded and can be 100 % active

**THE PERPETUAL SESSION.** For the same constitution, *every* code in which
each occupied cell carries both kinds is a fixed point, and a law at i is
active iff i + E is empty. So a column of n doubly-occupied cells is fixed
forever with **all 2n laws active**:

```
   #        n = 20:  |S| = 40,  active laws = 40,  Phi(S) = S  (certified)
   #        every law is permanently amending; every amendment is
   #        permanently annulled by its twin.
   #        "a parliament in permanent session that never passes anything"
   #
```

So balanced constitutions are **not** rare curiosities: they exist at every
size, with activity fraction 1, and they form a positive-density subset of
codes in such universes.

### 9.4 Non-local balance, and how far apart the chambers can be

The two cancelling authors of a slot (j,m) stand at j − c_k and j − c_{k′}, so
they are exactly |c_k − c_{k′}| apart — at most 2 in the Chebyshev norm, since
offsets are bounded by 1. Of the 36,964 distinct universes that produced a
balanced code in the complete Moore census, **32,696 (88 %) have c_A ≠ c_B**,
so their balance is necessarily *non-local*.

**THE TWO CHAMBERS** `ONN>A OSS>A` — the z3-maximal balanced code in a 6 × 6
box has card 29 with 24 active laws and cancellation distance 2:

```
   BBBBBB      A-laws (bottom row) amend the middle row from below;
   ......      B-laws (top row) amend the same cells from above.
   A##A#A      Every enactment meets its mirror and dies.  The two
   #BBBB#      chambers never see one another; they meet only in the
   ......      amendments they cancel.
   AAAAAA
```

### 9.5 Maximal balanced codes (z3)

For a fixed constitution, "is there a code in an n × n box that is fixed with
many active laws?" is a Boolean satisfiability question: variables x[cell,kind],
constraint "every slot receives an even number of toggles", objective "maximise
the number of active laws". `balance.py` solves it with z3 `Optimize`.
Maxima in a 7 × 7 box (each verified afterwards by `xnomos.py`):

| constitution | card | active laws |
|---|---|---|
| `OPP>AB OPP>AB` | 59 | 56 |
| `OEO>A OEO>A` | 56 | 56 |
| `OPP>AB OEP>AB` | 56 | 56 |
| `OEO>AB OWO>AB` | 56 | 56 |
| `OSS>A OES>A` (the nomos2d witness) | 50 | 50 |
| `OEE>AB OWW>AB` | 42 | 42 |
| `ONN>A OSS>A` (6 × 6 box) | 29 | 24 |

### 9.6 Perturbation

Adding one law at a uniformly random empty cell of the bounding box (300 trials
per constitution, only cells not already carrying that kind):

| constitution | balance survives |
|---|---|
| `OEE>A OWW>A` | 96/221 = 43 % |
| `ONN>A OSS>A` | 91/228 = 40 % |
| `OPE>A OTW>A` | 31/231 = 13 % |
| `OEN>A OWS>A` | 22/247 = 9 % |

Balance is **fragile but not brittle**: a single arbitrary amendment breaks it
about 60–90 % of the time. (Recorded against P4c, which guessed 50/50.)


---

## 10. Other fauna: puffers, translating growers, and what a writ leaves behind

**THE ITINERANT COURT** (a puffer) — `OEO>ABC OEE>AB OOO>C`, seed A+B at one
cell. The Writ's repealing clause A now also enacts a **dead-letter kind C** on
the cell it vacates. The head moves at the speed of light and lays down a
permanent inert trail: |S_t| = t + 2.

```
  t=0  #...........      C is inert (its guard a=b=O never passes) and nobody
  t=1  C#..........      amends it, so the trail is permanent terrain.
  t=3  CCC#........      A moving front leaving debris: a puffer whose wake is
  t=6  CCCCCC#.....      a wall the writ itself could never cross (see 7.2).
```

**Translating growers.** The Sower and the Land Grant are translating growers
in the strict sense: their *front* (the A-ray, resp. the A-diagonal) advances
at speed 1 and the body behind it is a fixed shape scaled by t. The Assize gun
is the degenerate case where the body is a periodic train.

**The rake versus the puffer.** The rake (`§6.4`) is strictly stronger: its
wake is made of *free gliders*, so a single 4-kind constitution seeded with two
laws produces an unbounded, non-interacting glider train laid along a diagonal.


---

## 11. Mission 3b — cryptids: THE ODOMETER

### 11.1 The escalation cascade

The complete 2-kind Moore parity census leaves 297,344 runs *unresolved*: alive
after 300 steps, still inside a 60 × 60 box, with no recurrence. Escalated in
three stages (`escalate.sh`, exact canonical hashing of every state throughout;
a run is "escape" when its span exceeds 60 or its card exceeds 900):

| stage | steps | input | escape | cycle | **still unresolved** |
|---|---|---|---|---|---|
| B | 3,000 | 297,344 | 287,497 | 20 | **9,827** |
| C | 30,000 | 9,827 | 9,564 | 0 | **263** |
| D | 300,000 | 263 | 84 | 0 | **179** |

**179 codes with no recurrence in 300,000 fully-hashed steps** (152 distinct
constitutions). These are not long transients: their reach grows, only very
slowly.

### 11.2 THE ODOMETER

```
constitution : OEW>B  NQR>AB
seed         : A@(0,0)  A@(1,0)  B@(0,1)        (three laws)
```

A column of width 2–3 that **counts in binary**. Measured to t = 2²⁰ (the exact
dict engine; independently re-hashed on `xnomos.py` to t = 2¹⁶ with no exact
recurrence):

| t | 2¹⁰−1 | 2¹⁰ | 2¹²−1 | 2¹² | 2¹⁴−1 | 2¹⁴ | 2¹⁶−1 | 2¹⁶ | 2¹⁸−1 | 2¹⁸ | 2²⁰−1 | 2²⁰ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| card | 57 | **4** | 75 | 6 | 111 | **4** | 138 | **4** | 147 | **4** | 255 | **4** |
| height | 20 | 20 | 26 | 26 | 38 | 38 | 47 | 47 | 50 | 50 | 86 | 86 |
| width | 2 | 2 | 3 | 3 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |

The signature is unmistakable: at every **t = 2^k − 1** the code swells to a
carry avalanche spanning its whole extent, and at **t = 2^k** it collapses to
**four laws** — a total jubilee — and starts again. The width never exceeds 3.

The reach grows **poly-logarithmically**: height ≈ 0.20·(log₂ t)² fits the
range k = 10…20 to within 8 % (20, 26, 38, 44, 47, 50, 74, 86 at
k = 10, 12, 14, 15, 16, 17, 19, 20). Compare the Jubilee code of `nomos2d`,
whose reach is ≈ 1.5√t: **the Odometer is a very much slower clock** — the
slowest in the fauna — and a purer counter: its epoch is exactly the binary
carry, and its quiescent state is exactly four laws.

Because the reach is unbounded, the orbit can never recur: **the Odometer is
aperiodic** (given the measured growth). It is bounded in card, unbounded in
reach — the same cryptid class as the Jubilee code, reached from a completely
different mechanism (a cross-amendment relay `A → B → {A,B}` rather than an
own-kind chain).

### 11.3 The family

Of the 179 survivors, **83** have their card maximum at some t = 2^k − 1 and a
minimum at some t = 2^k — strict 2-adic odometers. The other 96 peak at
t = 3·2^k − 1 and similar (e.g. 3071 = 3·2¹⁰ − 1, 4087, 4094): a **mixed-radix
family** of odometers, which own-kind nomodynamics — locked to powers of two —
never produced. The dominant rule shapes are `OEW`/`OWE` (a sunset clause) paired
with a diagonal relay (`NQR`, `STP`, `PNS`, `NPT`, …).


---

## 12. Verdict — what is decided, what is measured, what is open

Labels: **[E]** established (proved here or previously, with a proof in §3);
**[I]** interpretation of data; **[O]** original proposal / conjecture.

### Decided (proved)

* **[E] Generalised Ray Confinement** (Thm 3, Cor. 3.1). Out-degree 1 ⟹ the
  support of every code lies in a fixed finite union of parallel rays whose
  direction is the amendment cycle sum ⟹ **α ≤ 1** in every dimension, under
  parity, OR *and* supersession; cycle sum 0 ⟹ bounded ⟹ eventually periodic.
  This subsumes `nomos2d` Thm 3 and explains its §7 diagonal staircase.
* **[E] Potential-Anchor Theorem** (Thm 4) and **no gliders under
  single-target** (Cor. 4.1) and **under supersession** (Cor. 4.2), in every
  dimension. The Anchor Theorem's "eldest law" is replaced by a
  potential-graded anchor; its hypothesis (H1) is weakened from "own-kind
  effects" to "all reachable amendment cycles point the same way".
* **[E] α = 2 with fill → 1 is attained** (Thm 5, the Land Grant). Together
  with the trivial bound α ≤ dim this **closes the growth-exponent question in
  2-D**: the maximum is exactly 1 for out-degree 1 and exactly 2 for
  out-degree ≥ 2.
* **[E] Free gliders exist** — the Writ of Removal, in every dimension ≥ 1;
  and a gun, a rake, a puffer, and a 50-law diagonal spaceship.
* **[E] Authorship Lemma** (Thm 1): in-degree ≤ 1 ⟹ parity ≡ OR. The right
  generalisation of the Single-Author Lemma is about **in-degree**, not
  out-degree.
* **[E] Dead Letter under OR** (Thm 2): balanced constitutions cannot exist
  under OR-toggle in any dimension for any constitution; under parity they
  require a kind of in-degree ≥ 2, and 2 placed laws suffice.
* **[E] Balance is unbounded and can be totally active**: for `OEO>A OEO>A`,
  every code with both kinds on every occupied cell is fixed, with an
  activity fraction that can be 1.

### Measured (complete enumerations, exact counts stated)

* **[I]** Over the complete 2-kind Moore census (4,782,969 universes × 6
  seeds × 2 semantics) and the complete 2-kind von Neumann census (140,625
  universes × all 255 codes in a 2×2 box × 2 semantics) and a 2,000,000-universe
  3-kind sample (× 8 seeds × 2 semantics) — **162.8 M certified classifications
  in all** — there is **not one** glider outside class 2 and **not one**
  balanced code outside classes 1–2 or under OR.
* **[I]** Every universe with a measured growth exponent ≥ 1.15 (34,584 of the
  573,598 measured) is class 2; none is class 0 or 1.
* **[I]** 8,769 of the 2-kind gliders and 866 of the 870 3-kind parity gliders
  possess a **null amendment cycle**; the remaining 4 use **opposed cycle
  sums**. Both are exactly the escape hatches Cor. 4.4 leaves open, and **no**
  glider anywhere admits a separating u.
* **[I]** The period spectrum is not 2-adic. Non-power-of-2 periods occur in
  every class, including **pure own-kind** (class 0) with Moore offsets:
  periods 3, 6, 12 there, up to 192 in class 2. The `nomos2d` regularity is an
  artefact of the von Neumann window.

### Open

1. **[O] Is a subluminal parity glider possible with two kinds?** None exists
   in the complete 2-kind Moore or von Neumann censuses (all 7,788 parity
   gliders are luminal), but three kinds give speeds 1/2, 2/5, 1/3, 1/4, 1/6.
   Conjecture: the minimum speed of a k-kind glider is 1/f(k) for some
   f growing with k, and every rational speed in (0,1] is eventually realised.
2. **[O] Is the null cycle / opposed-cycle-sums condition (Cor. 4.4)
   *sufficient* as well as necessary?** Theorem 4 is a no-go; there is no
   matching existence theorem. The 4 opposed-sum gliders show the second hatch
   is non-empty, but its density is 4/870 — why so much rarer?
3. **[O] Sharpen Theorem 4 for null cycles.** When some ⟨V_Z,u⟩ = 0 the
   potential exists with ≥ 0 instead of > 0, so the minimum-potential *layer*
   is invariant and evolves autonomously, driven only by null-cycle edges. Is
   the glider's motion always confined to that layer? A positive answer would
   give a structure theorem for gliders — the analogue of "a Life glider is a
   4-phase object" — rather than just an existence result.
4. **[O] Can α = 2 be attained with two kinds at fill → 1?** The Sower reaches
   fill 1/2 with two kinds; the Land Grant needs three for fill → 1. The
   L¹ light cone makes 1/2 look like the two-kind ceiling — is that a theorem?
5. **[O] Universality.** With a gun, a rake, a wall (dead letters), and a
   collision algebra whose outcome depends on the parity of the gap, the
   ingredients of a glider-logic computation are present. Is 2-D
   cross-amendment nomodynamics Turing-complete? Nothing here settles it, but
   for the first time the question is not obviously hopeless.
6. **[O] The 2-adic clock.** Periods 3, 5, 7, 21, 192 exist, but powers of 2
   still dominate by four orders of magnitude (3,859,579 period-2 cycles versus
   6,328 period-3). Is there a quantitative law behind the suppression?


---

## 13. The verification battery

`verify.py` re-certifies **every** positive claim of this expedition using
`/Users/lukacs/claude/math/program/phase6/xnomos.py` — the shared reference
engine, written by a different expedition — and nothing else. The C census
engine and `xa2d.py` are used to *find*; they are never trusted to *confirm*.

Certificate forms:
* **GLIDER** — the orbit is run to its periodic core (S_{t₀}, p, d) and then
  Φ^{p}(S) = σ^{d}(S) is re-checked over 5 full periods, plus a check that no
  shorter period q < p recurs modulo translation.
* **CYCLE** — Φ^{p}(S_{t₀}) = S_{t₀} over 3 periods, plus minimality of p.
* **BALANCED** — Φ(S) = S and the active-law set is nonempty.
* **GROWTH** — |S_t| equals the claimed closed form for every t ≤ 200, and for
  the Land Grant the exact *cell support* is compared set-by-set as well.
* **GUN** — the pump cell's law-set is p-periodic and |S_t| is exactly linear
  through t = 200.
* **COLLISION** — the outcome for each gap is checked against the parity rule.

```
$ python3 verify.py
[PASS] G1  Writ of Removal (E)          Phi^1 = sigma^(1,0), 5 periods, card 2
[PASS] G1' Writ of Removal (OR)         Phi^1 = sigma^(1,0), 5 periods, card 2
[PASS] G2  diagonal Writ (NE)           Phi^1 = sigma^(1,1), 5 periods, card 2
[PASS] G2' diagonal Writ (NW)           Phi^1 = sigma^(-1,1), 5 periods, card 2
[PASS] G3  4-law glider                 Phi^1 = sigma^(1,0), card 4
[PASS] G4  p=4 card-7 glider            Phi^4 = sigma^(4,0), core t0=10
[PASS] G4' p=4 card-7 mirror            Phi^4 = sigma^(0,4), core t0=10
[PASS] G5  subluminal (OR, speed 1/2)   Phi^2 = sigma^(-1,0), card 2
[PASS] G6  ONE-LAW glider (speed 1/4)   Phi^4 = sigma^(-1,1), card 1
[PASS] G7  no null cycle (opposed sums) Phi^4 = sigma^(-2,0), card 1
[PASS] G8  card-50 diagonal spaceship   Phi^4 = sigma^(4,4), core t0=22, card 50
[PASS] G9  subluminal parity, speed 1/6 Phi^6 = sigma^(-1,0), card 2
[PASS] G10 card-18, p=1, diagonal       Phi^1 = sigma^(-1,-1), core t0=5
[PASS] G11 1-D Writ of Removal          Phi(S) = sigma^1(S) in dimension 1
[PASS] C1  own-kind period 3            Phi^3(S_1) = S_1, card 3
[PASS] C2  reciprocal period 3          Phi^3(S_1) = S_1, card 2
[PASS] C3  period 5                     Phi^5(S_0) = S_0, card 3
[PASS] C4  period 7                     Phi^7(S_1) = S_1, card 5
[PASS] C5  period 192                   Phi^192(S_0) = S_0, card 3
[PASS] C6  period 112 (card 111)        Phi^112(S_92) = S_92
[PASS] M1  THE ASSIZE (glider gun)      pump 2-periodic, |S_t| linear to t=200
[PASS] M2  THE CIRCUIT COURT (rake)     |S_t| = 2t+2 for t = 0..200
[PASS] M3  writ collision algebra       gaps 1..10 obey the parity rule
[PASS] B1  two-chamber (2 laws, minimal) fixed with 2 active laws
[PASS] B2  PERPETUAL SESSION (40 laws)  fixed with 40 active laws (100 %)
[PASS] B3  TWO CHAMBERS (non-local)     fixed with 12 active laws
[PASS] A1  THE SOWER   |S_t| = (t+1)(t+2)/2  for t = 0..200
[PASS] A2  THE LAND GRANT |S_t| = (t+1)^2 and exact support, t = 0..200

verification battery: 28/28 PASS (independent engine: xnomos.py)
```

Engine-level cross-validation is in `validate_c.py`: 3,000 random 2- and
3-kind Moore universes × **four** semantics (parity, OR, supersession,
supersession-OR) with the C engine and the Python engine agreeing on verdict,
period, displacement, card and active-law count — 3,000/3,000 in each of the
four, re-run after every change to the C source.

---

## 14. Files, data, and repro commands

| file | what |
|---|---|
| `PREREG.md` | the pre-registration, verbatim, written before the first census run |
| `RESULTS.md` | this document |
| `xa2d.py` | Python engine: exact dict engine, dense numpy engine, certificates, constitution text format, self-tests against `xnomos.py` |
| `xcensus.c` | the C engine — 64×64 bitboard census with renormalisation and avalanche hashing; a 256×260 and 640×650 board for growth exponents; `--mode 9` single-experiment and `--mode 10` parallel batch modes; parity / OR / supersession / supersession-OR |
| `validate_c.py` | C ↔ Python duel over random universes × 4 semantics |
| `verify.py` | **the certificate battery** — every positive claim re-checked on `xnomos.py` |
| `balance.py` | z3 search for maximal balanced constitutions |
| `refine_alpha.py`, `refine2.py` | two-stage growth-exponent refinement |
| `gallery.py` → `gallery.txt` | the specimen gallery with ASCII frames |
| `escalate.sh`, `runcensus.sh`, `run2.sh`, `SUPER_RUN.sh`, `runall.sh` | run scripts for the censuses and the cascade |
| `cen_*.txt` | census summaries (tallies, class breakdown, period histograms, α histograms, exemplar finds) |
| `data/*.gz` | the per-run dumps: gliders, balanced codes, non-power-of-2 cycles, unresolved runs, α measurements, and the escalation stages (gzipped; each well under 5 MB) |

### Repro

```sh
# 0. engines and their cross-checks
python3 xa2d.py                       # engine self-tests vs xnomos.py
clang -O3 -march=native -pthread -o xcensus  xcensus.c -lm
clang -O3 -march=native -pthread -DAW=10 -DAH=650 -DATMAX=300 -o xalpha2 xcensus.c -lm
clang -O3 -march=native -pthread -DTBITS=20  -o xdeep   xcensus.c -lm
python3 validate_c.py 3000            # C == Python on 3000 universes x 4 semantics

# 1. the certificate battery (the only thing a positive claim rests on)
python3 verify.py                     # 29/29 PASS

# 2. complete 2-kind Moore census, both semantics  (~45 s each, 12 threads)
./xcensus --mode 0 --sem 0 --steps 300 --dump data/mp2 > cen_moore_parity.txt
./xcensus --mode 0 --sem 1 --steps 300 --dump data/mo2 > cen_moore_or.txt

# 3. complete 2-kind von Neumann census over all 255 codes in a 2x2 box
./xcensus --mode 1 --seeds 1 --sem 0 --steps 300 > cen_vn255_parity.txt
./xcensus --mode 1 --seeds 1 --sem 1 --steps 300 > cen_vn255_or.txt

# 4. 3-kind sample (2,000,000 reproducible random universes x 8 seeds)
./xcensus --mode 2 --n 2000000 --seeds 2 --sem 0 --steps 300 --dump data/k3p > cen_3kind_parity.txt

# 5. supersession
./SUPER_RUN.sh

# 6. growth exponents: stage 1 over the whole census, then two refinements
./xcensus --mode 0 --sem 0 --steps 300 --alpha 1 --dump data/ap2 > cen_moore_parity_alpha.txt
python3 refine_alpha.py 1.05          # -> data/alpha_refined.json
python3 refine2.py                    # -> data/alpha_stage2.json

# 7. the cryptid cascade (stages B/C/D, 3k / 30k / 300k steps)
./escalate.sh

# 8. maximal balanced constitutions
python3 balance.py 7

# 9. the gallery
python3 gallery.py > gallery.txt
```

Python 3.11, numpy 2.4, z3; clang -O3; 12 threads throughout. Every census is
seeded deterministically (`splitmix64` keyed by the universe index for the
3-kind sample), so all counts above are exactly reproducible.
