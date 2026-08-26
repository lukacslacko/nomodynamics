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
invisible before. They are independent (§3, §6) and they govern different
phenomena.

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
1. Out-degree ≥ 2 with all in-degrees 1 is impossible for |K| ≥ 1 only if
Σ out = Σ in; in general either axis may be raised alone, and a *single-target*
constitution can perfectly well have a kind of in-degree 2 (two different kinds
both amending a third). That is exactly what the census finds (§6).

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
  (plus a finite set): **α ≤ 1** — |S_t| ≤ |S_0|·|K|·L·(t+1) — in **every
  dimension**;*
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
*Proof.* Pick u₀ with ⟨V_Z,u₀⟩ > 0 for all Z. Theorem 3 forces nd ∈ F + Σ_Z ℕV_Z
for a fixed finite F and every n, so d lies in the cone generated by the V_Z,
whence ⟨d,u₀⟩ > 0. Apply Theorem 4. ∎

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

