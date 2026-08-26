# Nomic Rings under Cross-Amendment
### Expedition X-C — period spectrum, rotor algebra, ring↔line correspondence
*(document opens with the pre-registration, written before the first big run)*

---

## 0. PRE-REGISTRATION (written 2026-08-26, before any sweep)

Predictions, with the reasoning that generated them. Kept verbatim whatever the
data says.

**P1 (odd periods exist).** Own-kind ring periods are locked to powers of 2 by
𝔽₂-linearity + unipotency. Under an L-cycle permutation constitution the
monodromy over L steps involves σ^s, s = Σ_cycle c, whose order m/gcd(s,m) can
be odd; I expect **odd periods ≥ 3 to appear already at L = 2 and small m
(m ≤ 8)**, and to be *common*, not exotic.

**P2 (rotors on odd rings).** Own-kind: rotors exist on every even m ≥ 6 and on
no odd ring. Cross-amendment adds a second "hand" that can carry the packet, so
I predict **rotors on odd rings do appear** — first at m = 5 or 7, L = 2.
Confidence 0.7.

**P3 (parity ≡ OR under permutation targeting).** Single-Author survives for
injective t, so parity and OR should be identical dynamical systems on rings
too. I expect **0 divergences** in a lockstep duel over every seed swept.
Confidence 0.99.

**P4 (balance is parity-only, and needs non-injective targeting).**
Under OR a fixed point still forces every emission to vanish ⟹ every law
blocked ⟹ no balanced code, on every ring. Under parity + injective t the same
(Single-Author). So **balanced constitutions on ℤ/m exist exactly for
non-injective targeting under parity (and possibly under supersession)**, and
I expect an exact transfer-matrix count. Confidence 0.9.

**P5 (rotation speed of a cycle).** For an L-cycle constitution the natural
displacement is **s = Σ_cycle c per L steps**. Concretely I predict: for
*homogeneous* cyclic constitutions (all L kinds carrying the same rule
(a,b,c)) the natural object is a **screw rotor** Φ(S) = rot_c(τ(S)), τ = the
cyclic relabel of kinds, whence Φ^L(S) = rot_{Lc}(S) — rotation Lc = s per L
steps exactly. Confidence 0.6 that such screw rotors exist at all; 0.85 that
IF a rotor family exists for a homogeneous constitution its speed is s/L.

**P6 (new resonance families).** The own-kind Sunset Parliament reached 15, 63,
341 at m ≡ 2 (mod 4). I expect cross-amendment maxima at a given m to
**exceed** the own-kind maxima (bigger state space, richer polynomial algebra),
with periods that are orders of elements of 𝔽₂[σ]/(σ^m−1) — specifically I
predict periods divisible by ord_m(2)-type numbers and by m/gcd(s,m).

**P7 (ring rotors do NOT unroll into ℤ gliders).** The Anchor Theorem is dead
for fixed-point-free permutation constitutions, so a ℤ glider is not excluded
by it — but I still expect the finite support of a ring rotor, released on ℤ,
to degenerate into an anchored front or a growing blob. Confidence 0.75 that
**no cross-amendment ring rotor unrolls to a finite ℤ glider**. (If one does,
that is the headline and refutes the sibling expedition's evidence-grade no-go
conjecture.)

**P8 (supersession is the wild one).** Supersession breaks linearity outright;
I expect the **largest and least structured** period spectrum there, including
odd periods on rings at 1 kind, and rotors on odd rings.

**P9 (dead-letter reduction).** In an L-cycle, if any kind's rule is one of the
15 unconditional dead letters (b = 0 or a = b) then it never emits, so the next
kind in the cycle is immortal and the cycle degenerates to a feed-forward
chain. I predict all interesting phenomena live in the 12^L "all-live"
sub-census.

*(Results follow below; sections are filled in as the runs complete.)*

---

## 0b. SCORECARD against the pre-registration

| # | prediction | verdict |
|---|---|---|
| P1 | odd periods appear at L=2 and small m, and are common | **CONFIRMED, and stronger than predicted.** Odd period 3 at **m=3** (L=3), at **m=4** (L=2 non-injective). For m ≥ 8 the two-kind non-injective class realises **every** period 1..m. |
| P2 | rotors appear on odd rings, first at m=5 or 7 | **CONFIRMED — but the size guess was badly wrong, and the shape is a surprise.** No odd-ring rotor exists at m = 3,5,7,11,13,17 at all. The first is **m = 9 with three kinds**, **m = 15 with two**; every odd-ring rotor found anywhere is a **third-turn** (r = ±m/3), so 3 must divide m. |
| P3 | permutation targeting ⟹ parity ≡ OR on rings | **CONFIRMED.** 0 divergences; Single-Author holds verbatim on ℤ/m. |
| P4 | balance is parity-only and needs non-injective targeting | **CONFIRMED and made exact.** B(m)=0 under OR, super_or, and every injective target map (26,244 exact counts, 0 violations); exists under parity+non-injective and under supersession with ≥2 kinds; minimum **2 laws**. |
| P5 | rotation speed of an L-cycle is Σ c per L steps | **REFUTED.** Of the L-cycle rotors, 964 satisfy r·L ≡ s·p (mod m) and **4212 do not**. Σc predicts nothing — but the *right* invariant of L turned up anyway: it is the **odd part of L**, and it governs the period spectrum, not the rotation (§2.3). |
| P6 | cross-amendment maxima exceed the own-kind maxima at equal m | **CONFIRMED at equal state space and equal rule pool** (the honest control): 3 own-kind kinds vs 3 kinds in a 3-cycle gives 2→8, 2→8, 4→20, 6→**81**, 6→54 at m=3..7; at m=12 it is 23→**144**. New resonance family: **powers of 3** (27, 45, 81 at m=6), explained by the Cycle-Length Law (§2.3). |
| P7 | ring rotors do not unroll into ℤ gliders | **CONFIRMED.** 17,746 rotor classes released as finite ℤ codes: 0 gliders (48 holdouts survive a 10× budget as anchored ruler fronts). |
| P8 | supersession has the largest, least structured spectrum | **REFUTED for 1 and 2 kinds.** With one kind, supersession **is** own-kind nomodynamics (Lemma S below) — identical spectra at every m ≤ 20. With two kinds it is *weaker* than own-kind two-kind (maxp 23 vs 80 at m=10): clearing whole cells destroys long orbits. |
| P9 | everything interesting lives in the all-live 12^L sub-census | **REFUTED.** The m=4 and m=6 rotors need a dead-letter kind as immovable scaffolding: `X:(-1,-1,-1)` is an unsatisfiable statute that never fires yet is load-bearing (it supplies occupancy). Dead letters are structural, not inert. |

---

## 1. Setting, engines, and what "complete" means here

A **constitution** is a finite kind set K = {0..n−1}; kind k carries a rule
(a_k,b_k,c_k) ∈ {−1,0,1}³ and a target t(k) ∈ K. A **code** is a set of placed
laws (cell, kind) on ℤ/m. occ(i) = "some law of any kind stands at i". Law
(i,k) is **active** iff occ(i+a_k) and ¬occ(i+b_k). Every active law emits one
toggle of kind t(k) at cell i+c_k. Resolution per (cell, kind) slot:

* `parity` — the slot flips iff it receives an odd number of toggles;
* `or` — the slot flips iff it receives ≥ 1;
* `super` / `super_or` — **supersession**: the target map is ignored; an active
  law enacts *its own* kind at the target cell if that cell is empty, else it
  votes to CLEAR the whole cell; clear-votes resolve by parity / by OR.

Rotation: rot_r(S)[i] = S[i−r] — every law moves r cells forward. τ is the
cyclic relabelling of kinds (an automorphism exactly when the constitution is
homogeneous and cyclic). A **rotor** is a code with Φ^p(S) = rot_r(S), r ∉ the
stabiliser of S. A **screw rotor** is Φ^p(S) = rot_r(τ^j(S)).

> **Certificate hygiene.** A rotationally symmetric code satisfies
> Φ^p(S) = rot_r(S) for free. Every rotor claim below quotients the stabiliser
> out: rot_r(S) ≠ S is checked, otherwise every rot_{m/2}-symmetric blinker
> would register as a rotor. (This bites: it removes about a third of naive
> hits at m = 6.)

**Engines.** `sweep.c` (C, bitmask, one m-bit integer per kind) enumerates the
*entire* state space 2^(n·m) for a constitution, builds the functional graph,
and reports the exact multiset of cycle lengths, min-cardinality witnesses,
rotor classes, fixed points, balanced fixed points and Gardens of Eden.
`xring.py` is the same semantics in Python and is checked step-for-step against
the shared reference engine `../xnomos.py` (dict of cell → kind-mask, written
by a different expedition, sharing no code): 4,000 random configurations × 6
steps × 4 semantics, **0 mismatches**. Every positive claim below is
re-certified through the xnomos path.

**Scope.** 122,238 complete state-space censuses covering **3.50 × 10¹⁰ codes**,
every one of them classified exactly — not sampled. Where a claim rests on
sampling or on SAT decision it says so and gives the bound.

---

## 2. THE PERIOD SPECTRUM

### 2.1 The tables (complete enumerations)

Maximal period attained anywhere in the class, over the complete state space of
every constitution in it:

| class (all rule combinations in the class) | m=3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12* |
|---|---|---|---|---|---|---|---|---|---|---|
| own-kind, 1 kind (27) | 2 | 2 | 4 | 4 | 4 | 4 | 8 | 15 | 8 | 8 |
| own-kind, 2 kinds (729) | 2 | 2 | 4 | 6 | 6 | 8 | 8 | 80 | 12 | 23* |
| own-kind, 3 live kinds (1728) | 2 | 2 | 4 | 6 | 6 | — | — | — | — | — |
| **2-cycle permutation** (reciprocal, 729) | **4** | **6** | **8** | **14** | **16** | **30** | **30** | **80** | **64** | **144\*** |
| **2 kinds, both amending kind 0** (729) | **4** | **6** | **8** | **14** | **16** | **30** | 18 | 65 | **64** | **144\*** |
| **3-cycle permutation, live** (1728) | **8** | **8** | **20** | **81** | **54** | — | — | — | — | — |
| 3-cycle permutation, all (19683) | 8 | 8 | 20 | — | — | — | — | — | — | — |
| supersession, 1 kind (27×2) | 2 | 2 | 4 | 4 | 4 | 4 | 8 | 15 | 8 | 8 |
| supersession, 2 kinds (729×2) | 2 | 2 | 4 | 5 | 4 | 8 | 8 | 23 | — | — |
| supersession, 3 live kinds (1728) | 2 | 3 | 6 | 7 | 10 | — | — | — | — | — |

\* the m=12 column for the two-kind classes uses the 144 live-live rule pairs
only (2^24 states per constitution); it is an apples-to-apples comparison
across the three target maps, but a *sub*-census of the 729.

Own-kind, 1 kind, continued (this reproduces Expedition N-C's **Sunset
Parliament** by an independent code path — complete 2^m state spaces, all 27
kinds): m=12..20 → 8, 8, 8, 8, 8, 16, **63**, 16, **30**.

**The honest control.** The three-kind rows use the *same* rule pool (the 12
live kinds), the *same* state space 2^(3m) and the *same* semantics; the only
difference is the target map, identity versus 3-cycle. Cross-amendment
multiplies the maximal period by 4× (m=3,4), 5× (m=5), **13.5×** (m=6), 9×
(m=7). The gain is not a state-space artefact.

### 2.2 Which periods are attainable — the spectrum fills in

Complete period sets (every period realised by some code of some constitution
in the class):

```
own-kind 1 kind   m= 4 : {1,2}            m=9  : {1,2,4,8}       m=11 : {1,2,4,8}
own-kind 2 kinds  m= 4 : {1,2}            m=9  : {1,2,4,6,8}     m=11 : {1,2,4,6,8,12}
2-cycle perm      m= 4 : {1,2,4,6}        m=9  : {1,2,4,6,8,12,16,18,30}
both->kind 0      m= 4 : {1,2,3,4,6}      m=9  : {1,...,10,12,16,18}
                  m=11 : {1,2,3,4,5,6,7,8,9,10,11,12,14,16,18,20,28,32,64}
3-cycle perm      m= 6 : {1,...,10,12,13,14,15,16,18,20,22,24,27,30,32,45,60,81}
```

**The m=12 champion.** With the same 144 live-live rule pairs and the same
2^24-state space, own-kind targeting tops out at period **23** with 12 distinct
periods; both cross-amendment target maps reach period **144** with **36**
distinct periods — 6.3× the maximum, 3× the spectrum. The 144-cycle needs only
**eight laws**:

```
constitution:  X : (0,-1,1) amends X     Y : (0,-1,0) amends X     [parity, Z/12]
seed:          | Y . X . Y . X X Y . X X |            period 144
```
and the period set there is {1,…,16} ∪ {18,20,24,26,28,30,32,36,39,40,42,46,48,
61,62,63,64,80,96,144} — including the odd periods 39, 61 and 63.

**Finding (complete enumeration).** For the two-kind non-injective class,
**every integer 1 ≤ p ≤ m is attained on ℤ/m for m = 6 and m ≥ 8** (checked
m ≤ 11; m=7 misses 5 and 7). Own-kind never does: at m=11 own-kind two-kind
realises 6 periods, the non-injective class realises 19.

**Odd periods.** Own-kind: the first odd period > 1 anywhere on a ring is 3 at
m=6, then nothing odd until 15 at m=10. Cross-amendment: period 3 already at
**m=3** (3-cycle, 2 laws) and at **m=4** (two kinds, non-injective, 3 laws);
period 5 at **m=4** (3-cycle). At m=10 the non-injective class realises the odd
periods {3,5,7,9,13,15,21,23,31,65}.

**New resonance family.** Own-kind resonances are Mersenne-flavoured
(15 = 2⁴−1 at m=10, 63 = 2⁶−1 at m=18, 341 = (2¹⁰−1)/3 at m=22, always at
m ≡ 2 mod 4). The 3-cycle class at m=6 produces **27, 45, 81** — powers of 3 —
from four laws. And 81 = 3⁴ cannot come from the linear layer at all: a
semisimple element of GL(18,2) has order dividing lcm{2^d − 1 : d ≤ 18}, whose
3-part is only 3³ = 27, and unipotent parts contribute only powers of 2. So the
81-cycle is *forced* to be an occupancy phenomenon — which is exactly what §2.3
measures (its occupancy word has period 81 on the nose).

### 2.3 Where the periods come from — mechanism, proved and measured

**Theorem 2.1 (own-kind unipotency, window 1).** *Freeze any occupancy
O ⊆ ℤ/m. The own-kind per-kind operator is D = σ^c ∘ diag(g) with
g = 1_{A}, A = {i : O[i+a]=1, O[i+b]=0}. Then*
* *c = 0 ⟹ D² = D, so I+D is idempotent;*
* *c = ±1 ⟹ D^m = 0, so I+D is unipotent and its order divides 2^⌈log₂ m⌉.*

*Proof.* D^j = σ^{jc}∘diag(∏_{r<j} g(· − rc)). A ≠ ℤ/m always: A = ℤ/m would
force O ≡ 1 (from the occupancy guard) and O ≡ 0 (from the vacancy guard). For
c = ±1, gcd(c,m) = 1, so {i − rc : r < m} = ℤ/m; hence for every i some
i − rc ∉ A and the product mask is empty: D^m = 0. For c = 0, D = diag(g) is a
projection. ∎ *(This supplies the gcd step missing from `rings/RESULTS.md` §3.)*
Machine check: **220,968 (kind, m, occupancy) triples, m ≤ 12, 0 violations.**

**Corollary.** Every own-kind cycle on which the occupancy never changes has
period a power of 2. Complete check: over all 27 kinds and m ≤ 9 the only
constant-occupancy period is **1**; over all 144 live two-kind own-kind
constitutions, m ≤ 7, the only ones are **{1, 2}**.

### THE CYCLE-LENGTH LAW — the exact algebraic account

This is the sharpest structural result of the expedition, and it answers the
mission's algebraic question directly.

**Theorem 2.2 (block-cyclic monodromy).** *(proved)* *For an L-cycle
permutation constitution, the frozen-occupancy step is M = I + N with N
block-cyclic, (NX)_{k+1} = σ^{c_k}(g_k · X_k); and N^L is block-diagonal, its
k-th block equal to σ^s ∘ diag(mask), s = Σ_{cycle} c_k.* So on any N-invariant
subspace where the transported mask acts as the identity and σ^s acts
trivially, N satisfies y^L = 1, and the operator algebra contains

  𝔽₂[y]/(y^L − 1) = 𝔽₂[y]/((y^{L′} − 1)^{2^v}),  L = 2^v · L′, L′ odd,
  𝔽₂[y]/(y^{L′} − 1) ≅ ∏_i 𝔽_{2^{d_i}},  d_i = ord of 2 mod the i-th divisor.

*and M = 1 + y.* On the trivial factor (y ↦ 1) M ↦ 0. On a factor 𝔽_{2^d}
(y ↦ ζ ≠ 1) M ↦ 1 + ζ, a **unit of odd order dividing 2^d − 1**. On the
nilpotent directions M − 1 is nilpotent and contributes only powers of 2.

**Consequently:** *L a power of two ⟹ L′ = 1 ⟹ the algebra is local, 1 + y is
nilpotent, and every frozen-occupancy period is a power of 2. An odd factor
L′ > 1 unlocks odd orders, the largest being 2^{ord_{L′}(2)} − 1.* Own-kind is
L = 1 and reciprocal amendment is L = 2 — **both powers of two.** That is why
the two most-studied sectors of nomodynamics are both locked to powers of 2,
and it is not a coincidence but a fact about 𝔽₂[y]/(y^{2^v} − 1).

**Measured** (`linorder.py`: the exact multiplicative period q(M) of the
frozen-occupancy operator, over every occupancy of every constitution in the
class — 1-, 2- and 3-kind classes exhaustive, L ≥ 4 sampled):

| L | odd part L′ | ord_{L′}(2) | predicted max odd order 2^d − 1 | measured q(M) values |
|---|---|---|---|---|
| 1 (own-kind) | 1 | — | — | {1, 2, 4} |
| 2 (reciprocal) | 1 | — | — | {1, 2, 4, 8} |
| **3** | 3 | 2 | **3** | {1, 2, **3**, 4, **6**, 8, **12**} |
| 4 | 1 | — | — | {1, 2, 4, 8} |
| **5** | 5 | 4 | **15** | {1, 2, 4, 8, **15**} |
| **6** | 3 | 2 | **3** | {1, 2, 4, **6**, 8, **12**, 16} |
| **7** | 7 | 3 | **7** | {1, 2, 4, **7**, 8} |

Every prediction lands. The L = 5 entry is the prettiest: ord₅(2) = 4, so the
algebra contains 𝔽₁₆, and the operator realises the *full* multiplicative order
**15 = 2⁴ − 1** — the same 15 that the own-kind Sunset Parliament had to climb
to m = 10 to reach, here obtained on a **three-cell ring** because it comes from
the amendment cycle rather than from the ring. Likewise L = 7 realises
7 = 2³ − 1 on ℤ/3. And the non-injective two-kind class stays at {1, 2, 4}:
sharing a target does not lengthen the amendment cycle, so it buys balance
(§5) but not linear resonance.

> **The Cycle-Length Law.** *The odd part of the amendment cycle is the odd
> part of the clock.* A constitution in which amendment closes after L steps
> carries a hidden copy of 𝔽₂[y]/(y^L − 1); when L is a power of two that ring
> is local and the constitution can only tick in powers of two, however large
> the parliament. Give the amendment cycle an odd factor and finite fields
> appear, with them units of odd order, and with them odd periods.

### What the champions actually do

The linear layer is not, however, where the *long* cycles come from. Decomposing
every champion cycle as p = q · ord(T), q = the occupancy period and T the 𝔽₂
monodromy over q steps:

| class | m | p | laws | q | ord(T) |
|---|---|---|---|---|---|
| own-kind 1 kind | 18 | 63 | 10 | 63 | 1 |
| own-kind 2 kinds | 10 | 80 | 11 | 80 | 1 |
| 2-cycle perm | 8 | 30 | 5 | 30 | 1 |
| 2-cycle perm | 11 | 64 | 5 | 64 | 1 |
| non-injective | 10 | 65 | 8 | 65 | 1 |
| 3-cycle perm | 6 | **81** | 4 | 81 | 1 |
| supersession 2 kinds | 10 | 23 | 8 | 23 | 1 |

In **every** champion q = p and ord(T) = 1: the long period lives entirely in
the occupancy trajectory. So nomodynamics has two independent clocks — a
**linear clock** governed exactly by the Cycle-Length Law, and a **combinatorial
clock** in the occupancy word — and the record-holders run on the second. The
81-cycle on ℤ/6 could not have run on the first: a semisimple element of
GL(18,2) has order whose 3-part divides 3³ = 27, and unipotent parts contribute
only powers of 2, so 3⁴ = 81 is out of reach of any frozen-occupancy operator on
that space. *(Interpretation.)* Cross-amendment buys its record periods by
making the occupancy word wander further — more laws can be repealed per step,
and by more authors — while the Cycle-Length Law tells you what the algebra
alone would allow.

**Lemma S (supersession collapse).** *With a single kind, supersession IS
own-kind toggling.* With n = 1 a cell is occupied iff kind 0 stands there, so
"enact if empty, clear if occupied" is exactly "toggle kind 0", and the clear
resolution is vacuous. Hence the n = 1 rows of the tables coincide identically
at every m ≤ 20, under both clear resolutions — and inherit the Sunset
Parliament unchanged. *(This is why P8 failed: supersession is not a variant at
all until there are two kinds.)*

**And the clear-resolution axis is dynamically vacuous even then.** At every
m ≤ 10 the two-kind supersession class has identical maximal periods and
identical period sets under `super` and `super_or` (complete enumeration, 729
rule pairs under each). What the axis does change is *balance*: 4,337,972
balanced codes under `super`, **zero** under `super_or` (§5.1). The resolution
rule is a statement about simultaneous cancellation, not about dynamics.

---

## 3. ROTORS UNDER CROSS-AMENDMENT

### 3.1 Two theorems that reorganise what "a rotor" means

**Theorem 3.1 (light cone).** *With window-1 guards and |c| ≤ 1, S_{t+1}(j)
depends only on S_t(j−2 … j+2).* (A law emitting into j sits at j−c, one cell
away; its guards read one cell further.) Machine check: 4,000 random
single-cell perturbations at distance > 2 from j — **0** changed cell j.

**Corollary (barber poles).** *If a rotor has min(r, m−r) > 2p then no signal
travels with the pattern: the apparent rotation is a phase velocity of a
spatially quasi-periodic code, not transport.* Call these **barber poles**, and
the ones with min(r, m−r) ≤ 2p **transporting**. Both are realised; over the
whole census the 17,670 spatial rotor classes split **10,693 transporting to
6,977 barber-pole**. *This
reclassifies the founding specimen*: the ℤ/6 three-law hop-3 rotor of
`glider-question/RESULTS.md` §4.2 has min(3,3) = 3 > 2·1 — it is a **barber
pole**, a period-2 blinker whose two phases happen to be half-turns of each
other. The genuinely-carried objects are the rot-2-per-3-steps "legislative
wave" of ℤ/10 and the cross-amendment specimens below.

**Theorem 3.2 (tiling lift).** *If Φ^p(X) = rot_r(τ^j(X)) on ℤ/m (m ≥ 3) then
the q-fold tiling X^{(q)} on ℤ/(qm) satisfies Φ^p(X^{(q)}) = rot_r(τ^j(X^{(q)}))
for every q ≥ 1 — same period, same rotation.* *Proof:* the update is a
window-2 local map (Thm 3.1) and every cell of the tiling has the same
5-neighbourhood as its preimage; the tiling of a rotation is the rotation of a
tiling. ∎ Machine check: **all 17,746 rotor classes lifted to ℤ/2m and ℤ/3m —
35,492 confirmations, 0 failures.** This explains the "extra" rotor classes at
composite m (e.g. every rot-3 rotor at m=12 and 18 is the ℤ/6 rotor tiled).

### 3.2 The census — where rotors live

Number of distinct spatial rotor classes (p, r ≠ 0, screw j) found in the
complete state space of every constitution of the class:

| class | m=3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12..20 even | 12..19 odd |
|---|---|---|---|---|---|---|---|---|---|---|---|
| own-kind, 1 kind | 0 | **0** | 0 | 4 | 0 | 2 | 0 | 6 | 0 | 10,8,6,12,16 | **0** |
| own-kind, 2 kinds | 0 | **0** | 0 | 290 | 0 | 204 | 0 | 418 | 0 | — | — |
| own-kind, 3 live kinds | 0 | **0** | 0 | 1914 | 0 | — | — | — | — | — | — |
| 2-cycle permutation | 0 | **88** | 0 | 466 | 0 | 484 | 0 | 590 | 0 | — | — |
| 2 kinds → kind 0 | 0 | **76** | 0 | 422 | 0 | 408 | 0 | 554 | 0 | — | — |
| 3-cycle permutation, live | 0 | **576** | 0 | 2896 | 0 | — | — | — | — | — | — |
| supersession, 2 kinds | 0 | **32** | 0 | 246 | 0 | 168 | 0 | 370 | — | — | — |
| supersession, 3 live kinds | 0 | **768** | 0 | 2452 | 0 | — | — | — | — | — | — |

At m=12 over the 144 live-live pairs: own-kind 295 spatial rotor classes,
2-cycle 506, non-injective 519.

Two facts jump out.

**(A) Cross-amendment lowers the minimal rotor ring from 6 to 4.** Own-kind
nomodynamics has *no* rotor at m=4 (complete: 27 kinds × 16 states; 729
two-kind constitutions × 256 states; 1728 three-kind × 4096). Cross-amendment
has 88 classes there. The smallest is three laws (specimen **Q-4** below).

**(B) Odd rings look forbidden — until you look past where enumeration can
reach.** Every complete enumeration listed above returns zero spatial rotors on
every odd ring. But the enumerable range stops just short of where the first
ones live: m = 9 needs three kinds (2^27 states per constitution, 1728
constitutions — out of reach) and m = 15 needs two (2^30 per constitution).
SAT reaches both. See §3.4 — this is the expedition's headline.

### 3.3 The gallery

Frames are one line per step; a cell shows the kinds standing there. Every
certificate below was produced by re-running the specimen through the
`xnomos.py` reference engine for three full periods (`specimens.py`).

```
### Q-4 — the smallest rotor ring in nomodynamics (own-kind needs m >= 6)
constitution: X:(-1,1,-1)->Y   Y:(0,-1,0)->X          [parity, ring Z/4]
Phi^1(S) = rot_2(S)   laws = 3   TRANSPORTING (2 <= 2p = 2)
  t=0  |XY .  Y  . |
  t=1  |Y  .  XY . |
  t=2  |XY .  Y  . |

### Q-4b — the same ring, a three-step relay (period-6 orbit)
constitution: X:(0,-1,0)->Y   Y:(0,-1,1)->X           [parity, ring Z/4]
Phi^3(S) = rot_2(S)   laws = 3   TRANSPORTING (2 <= 2p = 6)
  t=0  |XY .  X  . |      t=3  |X  .  XY . |
  t=1  |X  X  XY . |      t=4  |XY .  X  X |
  t=2  |XY X  XY . |      t=5  |XY .  XY X |

### R-6 — a four-law wave at rot 2 per step
constitution: X:(-1,-1,-1)->Y   Y:(0,1,-1)->X         [parity, ring Z/6]
Phi^1(S) = rot_2(S)   laws = 4   TRANSPORTING (2 <= 2p = 2)
  t=0  |Y X Y . Y .|
  t=1  |Y . Y X Y .|
  t=2  |Y . Y . Y X|

### K-6 — THE KIND RELAY: three kinds hand the packet forward
constitution: X:(0,1,-1)->Y  Y:(0,1,-1)->Z  Z:(0,1,-1)->X   [parity, Z/6]
Phi^1(S) = rot_2 o tau(S)   laws = 4   TRANSPORTING (2 <= 2p = 2)
  t=0  |Z . X . Y X|
  t=1  |Z Y X . Y .|
  t=2  |Z . X Z Y .|
  t=3  |Z . X . Y X|     (tau^3 = id, rot_6 = id: one lap in three steps)

### D-3 — the doctrinal rotor: the code stands still, the KINDS rotate
constitution: X:(0,-1,0)->Y  Y:(0,-1,0)->Z  Z:(0,-1,0)->X   [parity, Z/3]
Phi^1(S) = rot_0 o tau^2(S)   laws = 2   no spatial motion
  t=0  |XY .  . |
  t=1  |XZ .  . |
  t=2  |YZ .  . |
  t=3  |XY .  . |

### C-3 — PERIOD 7 FROM TWO LAWS ON THE THREE-CELL RING
constitution (a 7-cycle of amendment, so the odd part of L is 7):
   X:(0,-1,0)->Y   Y:(0,-1,1)->Z   Z:(-1,1,0)->W   W:(-1,1,0)->V
   V:(0,1,-1)->U   U:(0,-1,1)->T   T:(0,1,-1)->X            [parity, Z/3]
Phi^7(S) = S, minimal.  laws = 2.  Own-kind on Z/3: period set {1,2}, full stop.
  t=0  |XY .    .   |      t=4  |XYU V    .   |
  t=1  |X  Z    .   |      t=5  |X   ZVT  .   |
  t=2  |XY ZW   .   |      t=6  |YU  ZWVT .   |
  t=3  |X  V    .   |      t=7  = t=0

### O-15 — THE FIRST ROTOR ON AN ODD RING
constitution: X:(-1,1,1)->X   Y:(0,1,-1)->X           [parity, ring Z/15]
Phi^1(S) = rot_5(S)   laws = 12   barber pole (5 > 2p = 2)
  t=0  |.  XY .  Y  .  X  XY .  Y  .  X  XY X  Y  . |
  t=1  |X  XY X  Y  .  .  XY .  Y  .  X  XY .  Y  . |
  t=2  |X  XY .  Y  .  X  XY X  Y  .  .  XY .  Y  . |
  t=3  = t=0                     (a rigid third-turn of the ring)
```

**C-3 is the Cycle-Length Law made flesh.** Two laws, three cells — the
smallest ring there is — and a period of **7**, where own-kind nomodynamics on
ℤ/3 can only blink or freeze. The 7 does not come from the ring at all; it comes
from 𝔽₈ ⊂ 𝔽₂[y]/(y⁷ − 1), the field the amendment cycle drags in behind it. The
same trick at L = 5 gives period 5 on ℤ/3, and the frozen-occupancy operator
there attains the full order 15.

**K-6 is the qualitatively new mechanism the mission asked for.** Every law is
the *same* rule (0,1,−1) — "while my right-hand seat is vacant, amend the cell
on my left" — but each kind amends the *next* kind, so the packet advances two
cells per step **and changes its own legal identity as it goes**; after three
steps the identity permutation closes at the same moment the ring does. Two
cells per step is exactly the light-cone speed of Theorem 3.1: this packet is
carried at the maximum speed the axioms allow. No own-kind constitution has an
analogue, because own-kind laws cannot repeal each other's kind.

**D-3 is a species with no own-kind counterpart at all**: with c = 0 nothing
can move in space, yet the *content* of the seat circulates through the
amendment cycle forever. Two laws, any ring, odd or even. Call it a
**doctrinal rotor** — the statute stays, the doctrine turns over.

### 3.4 Odd rings: the sharpest negative, and its exception

*Complete enumerations, zero spatial rotors on every odd ring tested:*

| class | odd m enumerated completely | states |
|---|---|---|
| own-kind, 1 kind, all 27 | 3,5,7,9,11,13,15,17,19 | 27 × Σ2^m |
| own-kind / 2-cycle / non-injective, 2 kinds, all 729 each | 3,5,7,9,11 | 3 × 729 × Σ4^m |
| supersession (both resolutions), 2 kinds, all 729 | 3,5,7,9 | 1458 × Σ4^m |
| own-kind / 3-cycle / supersession, 3 live kinds, all 1728 each | 3,5,7 | 3 × 1728 × Σ8^m |
| 3-cycle, all 19683 | 3,5 | 19683 × Σ8^m |

*Sampled hunt* (`hunt.c`): **21,600,000 random codes** on odd rings
m ∈ {5,7,…,21} × n ∈ {2,3,4} kinds × all four semantics × 400 random
constitutions per cell, each run to its cycle and tested — **0 rotors**. The
identical sampler on even rings (3,840,000 seeds) found **3,917 rotors in 193
distinct (m,n,mode,p,r) classes**, so the instrument is not blind.

**And yet odd-ring rotors exist — this is the headline of the expedition.**
The question is decidable rather than merely samplable: "∃ X ≠ 0 with
Φ^p(X) = rot_r(X) and rot_r(X) ≠ X" is a propositional formula in p·n·m
variables with only local clauses, so z3 settles it in milliseconds for ring
sizes far beyond any enumeration, and such an X is automatically recurrent
(Φ^{p·ord(r)}X = X). `satrotor.py` runs that decision. Validated first on even
rings, where it reproduces the enumerated classes exactly.

| SAT campaign | scope | rotors |
|---|---|---|
| own-kind, 1 kind, all 27 rules, parity + supersession | odd m ≤ 31, p ≤ 6, 4,860 decisions | **0** |
| 2 live kinds, 3 target classes, 4 semantics | odd m ≤ 17, p ≤ 3, 27,648 decisions | **20 — all at m = 15** |
| 3 live kinds, 3 target classes, parity | odd m ≤ 13, p ≤ 2, 62,208 decisions | **322 — all at m = 9** |
| even-ring controls | m ≤ 12, 2,484 decisions | 1,100 |

Every one of the 20 + 322 was re-verified over three full periods by the
xnomos engine. And **every single odd-ring rotor found, without exception, is
a THIRD-TURN**: its rotation is r ≡ ±m/3, so Φ^p acts on the code as the rigid
rotation by one third of the ring and the whole orbit is one rotation orbit of
length 3p.

Following the family outwards (`oddscan.py`, the four rule pairs that carry it
at m=15, p=1):

| m | 9 | 15 | 21 | 25 | 27 | 33 | 35 |
|---|---|---|---|---|---|---|---|
| 3 \| m ? | yes | yes | yes | no | yes | yes | no |
| rotors (2 kinds) | 0 | 4 (r=5,10) | 4 (r=7,14) | 0 | 4 (r=9,18) | 4 (r=11,22) | 0 |

**The Third-Turn Law (original proposal, evidence-grade).**
*On an odd ring a rotor exists only as a third-turn, hence only when 3 | m, and
only when the supercell ℤ/(m/3) has room for the pattern: with two kinds that
needs m/3 ≥ 5 (so m = 15 is the smallest), with three kinds m/3 ≥ 3 suffices
(so m = 9). Odd rings with no factor 3 — 5, 7, 11, 13, 17, 25, 35 — carry no
rotor at all.*

Minimum law counts at m = 15 (z3 cardinality-minimised): **12** laws for the
non-injective p=1 rot-5 rotor, **10** for the 2-cycle p=2 rot-5 rotor. At m = 9
with three kinds the witnesses are of similar density.

So the picture is:

> **Odd rings are not forbidden — they are expensive, and they can only be
> turned by thirds.** Own-kind nomodynamics never turns an odd ring at all
> (0 rotors in complete state spaces up to m = 19 and in 4,860 SAT decisions up
> to m = 31). Cross-amendment can, from m = 9 with three kinds and m = 15 with
> two, and always as a barber pole: r = m/3 per step is far outside the light
> cone, so what rotates is a *phase* of a nearly-(m/3)-periodic code, not a
> carried packet. On an even ring the cheap symmetry is the half-turn — three
> laws suffice. On an odd ring the cheapest available is the third-turn, and it
> costs ten to twelve.

**Open (sharpened, and now the single best question I own).** Is there a
*transporting* rotor on any odd ring — one with min(r, m−r) ≤ 2p? Every
odd-ring witness so far is a barber pole. If the answer is no, the theorem
would read: **causal transport of a law-packet around a ring requires an even
ring**, and the Anchor Theorem's shadow would extend from ℤ to every odd ℤ/m.

---

## 4. THE RING↔LINE CORRESPONDENCE

**Theorem 4.1 (unrolling).** *For m ≥ 3 the set of spatially m-periodic states
of ℤ is invariant under Φ_ℤ, and Φ_ℤ restricted to it is conjugate to Φ_{ℤ/m}
under the obvious identification.* *Proof:* the update is local with radius 2
(Thm 3.1) and m ≥ 3 > 2·1, so every cell of the periodic lift sees exactly the
neighbourhood its ring preimage sees; periodicity is therefore preserved. ∎

**Corollary 4.2 (every ring rotor is a ℤ wave train).** A rotor on ℤ/m unrolls
to a spatially m-periodic, temporally p-periodic travelling wave on ℤ of
apparent velocity r/p — with **infinite support**, which is exactly why it does
not contradict the Anchor Theorem (which assumes a finite law-packet). And the
"apparent velocity" is genuinely only apparent when the rotor is a barber pole:
a spatially periodic pattern's phase velocity is unbounded, which is how a
window-1 system can display motion at speed m/2 per step. Machine: every rotor class travels correctly on a 6-fold tiling.

**Theorem 4.3 (wrapping).** *Let S be a code on ℤ. As long as the ℤ-orbit's
support stays inside a window of m−2 consecutive cells, the ℤ orbit and the
ℤ/m orbit of the same code agree cell for cell.* Machine: 4,000 random
(constitution, code) pairs, all four semantics, checked every step until the
support touched the seam — **4,000/4,000 agree**.

Together 4.1 and 4.3 say precisely what a ring is: **the line plus a seam**.
The Anchor Theorem holds on ℤ because each kind has an extremal law that
nothing can target. On ℤ/m the front eventually reaches its own rear; the
moment it does, the anchor becomes a target, and motion becomes possible. *The
ring is the line whose front eats its own anchor.*

**Corollary 4.4 (the finite chunk does NOT glide).** Releasing a ring rotor's
laws as a finite code on ℤ gives, over the whole gallery of **17,746 rotor
classes**: 15,419 CYCLE, 1,955 GROWING, 293 FIXED, 23 BALANCED, 8 EXTINCT, 48
holdouts — and **zero gliders**. The 48 holdouts survive a 10× budget (6,000
steps, span 3,000) still unresolved: they are ruler fronts, the anchored
aperiodic species of `glider-question/RESULTS.md` §5.2. Pre-registration P7
confirmed; the sibling expedition's cross-amendment no-go conjecture is *not*
refuted from this direction.

**The m → ∞ limit — a dichotomy.** Ring rotors split into two families with
opposite limits:

* **Fixed-r families** (r = 2, 3, 4, … independent of m) are spatially periodic
  by construction — by Theorem 3.2 they *are* tilings of a fixed small rotor —
  and they converge to a genuine infinite wave train on ℤ. Their law count
  grows linearly with m.
* **Half-turn families** (r = m/2, the base own-kind family {0,1,m/2+1} and the
  cross-amendment specimens with r = m/2) keep exactly 3 laws but their
  *diameter* grows like m/2. As m → ∞ the three laws separate without bound and
  the object dissolves into independent anchored fronts on ℤ: there is no
  limit. Their rotation is pure barber pole (m/2 > 2p for p small), i.e. it was
  never transport in the first place.

So: **the ring rotors that survive the limit are exactly the ones that were
never compact**, and the compact ones (3 laws, any m) are exactly the ones
whose "motion" was a global phase. The Anchor Theorem obstructs the limit in
precisely the sense that a finite packet cannot move — and both branches of the
dichotomy respect it.

---

## 5. CONSTITUTIONAL ALGEBRA ON RINGS

### 5.1 Balance: the exact trichotomy

**Theorem 5.1 (Balance = multi-authorship).** *On ℤ/m, for any constitution:*

1. *Under `or`, S is fixed ⟺ every law in S is blocked.* (x_t ⊕ OR-of-emissions
   = x_t forces the OR to be 0, hence every emission 0, hence no active law.)
   **No balanced code exists, under any target map, on any ring.**
2. *Under `super_or`, the same.* (Fixedness forces emit_k ∧ occ = 0 and
   emit_k ∧ ¬occ = 0, hence emit_k = 0.)
3. *Under `parity` with an injective (permutation) target map, the same* — this
   is the **Single-Author Lemma** on the ring: for each target kind there is
   exactly one source kind, so the XOR is a single term.
4. *Under `parity` with a non-injective target map, or under `super` with
   n ≥ 2 kinds, balanced codes exist. The minimum is exactly **two placed
   laws**, achievable on every ring m ≥ 4.*

*Minimality proof:* one active law emits exactly one toggle (or one
enact/clear), which always changes the state; two suffice, below. ∎

**Corollary 5.2 (why supersession needs a second kind).** With one kind,
supersession is own-kind toggling (Lemma S), so it inherits the Dead Letter
Theorem: **0 balanced codes** over all 27 kinds and every m ≤ 20, both clear
resolutions — verified by complete enumeration.

Machine verification of 1–3: exact transfer-matrix counts (below) for **all 729
two-kind rule pairs × 4 balance-free semantics × m = 4…12 = 26,244 exact
counts, 0 violations**, agreeing with the complete state-space sweeps.

**The minimal balanced code on a ring** (2 laws, ℤ/4 — and the same shape on
every larger ring):

```
constitution:  X : (-1, 1, -1)  amends X          both chambers legislate
               Y : ( 0,-1,  0)  amends X          about kind X

code on Z/4:   | Y  X  .  . |      Y at cell 0, X at cell 1
   X at 1 : occ(0)=1 and occ(2)=0  -> ACTIVE, emits toggle of X at cell 0
   Y at 0 : occ(0)=1 and occ(3)=0  -> ACTIVE, emits toggle of X at cell 0
   the two toggles cancel:  Phi(S) = S with 2 active laws.  BALANCED.
```

Two laws, both alive, both firing, forever, and nothing ever changes. This is
the object the Dead Letter Theorem forbids in own-kind nomodynamics, and it
needs exactly one extra ingredient: **two authors for one slot**.

**Which constitutions admit balance.** Exactly **70 of the 729 two-kind rule
pairs** under non-injective parity targeting — and all 70 have *both* rules
live (b ≠ 0 and a ≠ b); the 16 admissible guard-pairs are drawn from the four
live guards (−1,1), (0,−1), (0,1), (1,−1); the offset difference c₀−c₁ is
unconstrained (30 pairs with c₀=c₁, 20 with each other difference). The count
70 is reproduced independently by the transfer matrix and by the complete
state-space sweep at every m = 3…11.

### 5.2 Exact counts by transfer matrix

Fixedness is a 5-window local condition (only laws at j−1, j, j+1 can emit into
j; their guards read j−2 … j+2), so the number of fixed codes on ℤ/m is
tr(T^m) for a transfer matrix on 4-cell contexts over the alphabet 2^K. With
F(m) = # fixed, Z(m) = # all-blocked ("dead letter") and B(m) = F−Z = # balanced:

**The two-chamber veto** `X:(0,1,1)→X, Y:(0,−1,−1)→X` (parity):

| m | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|
| F | 152 | 534 | 1875 | 6584 | 23120 | 81187 | 285092 | 1001114 |
| Z | 98 | 309 | 973 | 3063 | 9642 | 30352 | 95545 | 300766 |
| **B** | **54** | **225** | **902** | **3521** | **13478** | **50835** | **189547** | **700348** |

B(20) = 72,148,602,339, and **B/F → 0.888** at m=20.

**Twin chambers** `X:(0,1,1)→X, Y:(0,1,1)→X`: B(6)=854, B(20)=42,838,027,374,
B/F(20) = 0.925.
**Supersession pair** `X:(0,−1,1), Y:(0,1,−1)` under `super`: B(6)=72,
B(20)=1,706,312,688, B/F(20) = 0.158.

Validated against brute force for m = 4…8 on seven constitutions across all
four semantics: **0 mismatches**.

> **The reversal.** In own-kind nomodynamics *every* fixed code is a dead
> letter — stability is gridlock, and that was the sharpest structural fact of
> `rings/RESULTS.md`. Under shared authorship the ratio inverts: on ℤ/20 under
> the two-chamber veto **89 % of all fixed codes are balanced** — alive,
> firing, and going nowhere. Deadlock stops being the absence of activity and
> becomes its equilibrium.

### 5.3 Gardens of Eden and the fixed fraction

Complete state spaces, 144 live two-kind rule pairs per cell, in-degree
computed exactly:

| m | GoE fraction, own-kind | GoE fraction, cross-amendment | GoE, supersession | fixed fraction own / cross |
|---|---|---|---|---|
| 3 | 0.3132 | **0.2415** | 0.3125 | 0.5195 / 0.5488 |
| 5 | 0.4144 | **0.3268** | 0.4669 | 0.2926 / 0.3211 |
| 7 | 0.5149 | **0.4113** | 0.5801 | 0.1716 / 0.1976 |
| 9 | 0.5986 | **0.4832** | 0.6702 | 0.1026 / 0.1249 |

**Cross-amendment makes legal history *more* writable.** At every ring size the
Garden-of-Eden fraction drops by ~10–12 percentage points when the target map
stops being the identity. The mechanism is exactly the one that creates balance:
when two kinds can author the same slot, a given change of that slot has more
possible causes, so fewer codes are unreachable. Supersession moves the other
way (clearing a whole cell destroys information), and has the highest GoE
fraction of all. Meanwhile the *fixed* fraction rises under cross-amendment —
those are the new balanced codes.

---

## 6. VERIFICATION BATTERY

| check | scope | result |
|---|---|---|
| `xring.py` bitmask engine ≡ `../xnomos.py` reference engine | 4,000 random constitutions × 6 steps × all 4 semantics | 0 mismatches |
| `sweep.c` ≡ `xring.py` ≡ `xnomos.py` (every reported witness re-run) | 20,966 rotor certificates, each re-verified over **3 full periods** by the xnomos path | **0 failures** |
| maximal-period certificates re-simulated independently | 122,238 (one per census job) | **0 failures** |
| stabiliser hygiene (rot_r(S) ≠ S enforced) | every rotor claim | rotation-symmetric false positives removed |
| Single-Author on rings: parity ≡ OR under permutation targets | 2,000 random ring states × 8 steps | 0 divergences |
| dead-letter classification (15 of 27 kinds never fire) | exhaustive on ℤ/7, 27 kinds × 128 states | exact |
| own-kind nilpotency (Thm 2.1) | 220,968 (kind, m ≤ 12, occupancy) triples | 0 violations |
| Cycle-Length Law: exact q(M) over every frozen occupancy | own-kind 1/2/3-kind, 2-cycle, non-injective classes: exhaustive (m ≤ 10 / 8 / 6); L = 4…7 sampled | predictions match at every L |
| light cone (Thm 3.1) | 4,000 random perturbations at distance > 2 | 0 leaks |
| tiling lift (Thm 3.2) | 17,746 rotor classes × q = 2, 3 | 35,492 confirmed, 0 failed |
| wrapping (Thm 4.3) | 4,000 random (constitution, code) pairs, all semantics | 4,000/4,000 |
| transfer-matrix counts vs brute force | 7 constitutions × 4 semantics × m = 4…8 | 0 mismatches |
| balance impossibility (Thm 5.1.1–3) | 729 rule pairs × 4 semantics × m = 4…12 = 26,244 exact counts | 0 violations |
| balance count agreement (transfer matrix vs complete sweep) | 70 admitting constitutions, m = 3…11 | exact agreement |
| odd-ring rotor hunt (sampled) | 21,600,000 codes, odd m ≤ 21, n ≤ 4, 4 semantics | 0 rotors |
| … the same sampler, even-ring control | 3,840,000 codes | 3,917 rotors, 193 classes |
| odd-ring rotor **decision** by SAT | 4,860 (1 kind, m ≤ 31, p ≤ 6) + 27,648 (2 kinds, m ≤ 17, p ≤ 3) + 62,208 (3 kinds, m ≤ 13, p ≤ 2) | see §3.4 |
| … SAT decider validated against enumeration | even-ring controls, 2,484 calls | reproduces exactly the enumerated rotor classes |
| ℤ-release of every ring rotor | 17,746 codes, budget 600 then 6,000 steps | **0 gliders**, 48 permanent holdouts |

Total: **122,238 complete state-space censuses covering 3.50 × 10¹⁰ codes**,
plus 25.4 M sampled seeds and ≈ 97,000 SAT decisions. Every number in this
document is either an exact enumeration or is labelled as a sample / decision
with its bound.

---

## 7. VERDICT

**The period spectrum.** Own-kind nomodynamics on a ring is temporally rigid:
over all 27 kinds and every m ≤ 20 the attainable periods are
{1, 2, 4, 8, 16} plus five isolated resonances (3 at m=6 and 12 and 18, 7 at
m=14, 15 at m=10 and 20, 63 at m=18, 30 at m=20). Adding kinds without
cross-amendment barely helps — three own-kind kinds on ℤ/6 still top out at 6.
**Cross-amendment dissolves the rigidity.** With the same rule pool, the same
state space and the same semantics, changing the target map from the identity
to a 3-cycle takes the maximum on ℤ/6 from 6 to **81**, and the attainable set
from {1,2,3,4,6} to twenty-five distinct periods including 27, 45 and 81 —
a new resonance family of **powers of three**, where own-kind resonances are
Mersenne. With two kinds sharing a target, the spectrum on ℤ/m becomes an
**initial segment**: every period 1 … m is realised for m = 6 and m ≥ 8.

The mechanism splits in two, and both halves are new. The **linear clock**
obeys an exact law: the frozen-occupancy operator of an L-cycle constitution
lives in 𝔽₂[y]/(y^L − 1), which is local exactly when L is a power of two — so
own-kind (L = 1) and reciprocal amendment (L = 2) are *provably* confined to
periods that are powers of 2, while an odd factor L′ in L produces 𝔽_{2^d}
factors and units 1 + ζ of odd order up to 2^{ord_{L′}(2)} − 1. Measured and
matched for L = 1…7: L = 5 realises the full order **15 on a three-cell ring**,
L = 7 realises **7**. The **combinatorial clock** is the occupancy word, and it
is where the record-holders live: every champion cycle has q = p, ord(T) = 1.
Cross-amendment lengthens both.

**Rotors.** Cross-amendment lowers the minimal rotor ring from 6 to **4**;
supplies the first **kind-relay rotor** (K-6: three kinds pass a four-law packet
round ℤ/6 at exactly the light-cone speed, changing legal identity each step);
supplies a species with no own-kind counterpart at all (**D-3**, the doctrinal
rotor: the code is frozen in space while its kinds circulate); and — the
headline — supplies the **first rotors on odd rings**, at m = 9 with three
kinds and m = 15 with two. Every odd-ring rotor found is a *third-turn*,
r = ±m/3, so 3 must divide m; odd rings with no factor 3 (5, 7, 11, 13, 17, 25,
35) carry none in any test performed. The light-cone analysis (Thm 3.1) splits
the whole rotor zoo — including the founding ℤ/6 specimen — into **transporting
packets** and **barber poles**, and all odd-ring rotors so far are barber poles.

**Ring ↔ line.** Three exact statements. Rotors *tile*: a rotor on ℤ/m lifts to
ℤ/qm with the same p and r (35,492 confirmations). Rotors *unroll*: the
m-periodic states of ℤ are Φ_ℤ-invariant and carry exactly the ring dynamics,
so every ring rotor is a genuine infinite travelling wave on ℤ — of infinite
support, which is why the Anchor Theorem is untouched. Codes *wrap*: line and
ring orbits agree exactly until the support reaches the seam. Hence:

> **The ring is the line whose front eats its own anchor.** Entrenchment is a
> theorem of linear order; a ring has order locally and none globally, and the
> moment the advancing front meets its own rear the eldest law becomes a
> target.

And the limit is a clean dichotomy: rotors with fixed rotation are tilings and
converge to infinite wave trains; rotors with r = m/2 keep three laws but
spread their diameter like m/2 and dissolve into independent anchored fronts.
The compact ring rotors are exactly the ones whose motion was never transport.
Released as finite codes on ℤ, **all 17,746 rotor classes fail to glide** — no
counterexample to the cross-amendment no-go from this direction.

**Constitutional algebra.** Balance is exactly multi-authorship. Under OR, under
supersession-OR, and under every injective target map, a fixed code is a dead
code — the Dead Letter Theorem survives verbatim on every ring (26,244 exact
counts, 0 violations). Under parity with two kinds sharing a slot, or under
supersession with two kinds sharing a cell, balanced codes exist from **two
placed laws** on every ring m ≥ 4, in exactly **70 of the 729** two-kind
constitutions — and they take over: under the two-chamber veto on ℤ/20,
**88.8 %** of all fixed codes are balanced. Gridlock stops being the absence of
activity and becomes its equilibrium. Cross-amendment also makes history more
writable: the Garden-of-Eden fraction drops by 10–12 points at every ring size,
for the same reason — a slot with two possible authors has more possible pasts.

> **The law of the expedition.** *One author, one slot: the code can only
> freeze. Two authors, one slot: the code can be alive and still.* Everything
> new here — balanced constitutions, the filled-in period spectrum, the kind
> relay, the odd-ring third-turns, the extra reachability — is a consequence of
> letting two laws speak to the same place at the same time.

### Open questions, sharpest first

1. **Is there a transporting rotor on an odd ring?** (min(r, m−r) ≤ 2p, r ≠ 0.)
   Every odd-ring witness is a barber pole. A negative would read: *causal
   transport of a law-packet around a ring requires an even ring.*
2. **Prove the Third-Turn Law** — or find an odd-ring rotor whose rotation is
   not ±m/3. The parity obstruction that forbids odd rings for own-kind is still
   unidentified; the block/gap calculus of §2.3 gives m = 2γ+4 for the base
   own-kind family (hence even), but no general argument.
3. **What is the true growth of max period with m under cross-amendment?**
   The 3-cycle class gives 8, 8, 20, 81, 54 for m = 3…7 — non-monotone, and 81
   at m = 6 is 3⁴. Is there a resonance criterion on m analogous to the
   Sunset Parliament's m ≡ 2 (mod 4)?
4. **Exact fixed-point and balance counts for n ≥ 3** — the transfer matrix is
   written for 2^n-letter alphabets and n = 2 is done exactly for all m; n = 3
   needs a 1024-context implementation.
5. **Does the balanced fraction B/F tend to 1?** It is 0.888 at m = 20 for the
   two-chamber veto and rising; the transfer matrix should settle the limit
   (ratio of dominant eigenvalues).

---

## 8. REPRODUCTION

```sh
cd xrings
cc -O3 -march=native -o sweep sweep.c        # complete state-space censuses
cc -O3 -march=native -o hunt  hunt.c         # sampled rotor hunt
python3 ../xnomos.py                         # reference-engine self-tests
python3 xring.py                             # engine == xnomos, 4 semantics

export XR_RAW=./raw                          # raw JSONL lands here (~30 MB)
python3 campaign.py own                      # own-kind baseline, m=3..20     (2 s)
python3 campaign.py own2 own3                # the honest own-kind controls  (20 min)
python3 campaign.py recip                    # 2-cycle permutation, m=3..11   (5 min)
python3 campaign.py noninj                   # both kinds -> kind 0           (5 min)
python3 campaign.py cyc3all cyc3             # 3-cycle permutation            (6 min)
python3 campaign.py super1 super2 super3     # supersession, 1/2/3 kinds      (7 min)
python3 campaign.py goe                      # Garden-of-Eden census          (1 min)
python3 campaign.py big2                     # m=12, live-live pairs, 3 classes (9 min)

python3 tables.py                > tables.txt   # every table of section 2
python3 analyze.py recip noninj cyc3            # period sets + rotor classes
python3 certify.py own own2 own3 recip noninj cyc3 cyc3all super1 super2 super3 goe big2
                                                # 20,966 rotor + 122,238 period certs
python3 specimens.py                            # the gallery of section 3.3
python3 unroll.py                               # tiling lift, wave train, Z release
python3 deep.py                                 # mechanism, Eden, Z-holdouts
python3 theory.py                               # Thm 2.1 and 3.1 machine checks
python3 linorder.py                             # the Cycle-Length Law, L = 1,2,3
python3 runL.py ; python3 runL6.py              # the Cycle-Length Law, L = 4,5,6,7
python3 balance.py                              # transfer matrix + the 26,244 counts
python3 balwitness.py                           # the 70 constitutions, minimal witness

./oddhunt.sh                                    # 21.6 M sampled odd-ring codes
python3 satrotor.py control                     # SAT decider validated on even rings
./satrun.sh                                     # the odd-ring SAT decision campaign
python3 oddrotor.py minimal                     # minimum law count at m=15
python3 oddscan.py                              # the third-turn family, m up to 35
```

Files: `xring.py` (engine), `sweep.c` / `hunt.c` (C workhorses), `campaign.py`
(census driver), `analyze.py` / `tables.py` (reports), `certify.py` (independent
re-verification), `specimens.py` (gallery), `unroll.py` (ring↔line),
`balance.py` / `balwitness.py` (constitutional algebra), `theory.py` (theorem
checks), `deep.py` (mechanism + Eden + holdouts), `satrotor.py` / `oddrotor.py`
/ `oddscan.py` (the odd-ring decision campaign). Aggregated results in `data/`,
logs in `*.log` and `tables.txt`.
