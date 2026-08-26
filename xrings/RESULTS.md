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
| P2 | rotors appear on odd rings, first at m=5 or 7 | **CONFIRMED but the size guess was badly wrong.** No odd-ring rotor exists at m = 3,5,7,9,11 (complete state spaces) nor at 13 (SAT). The first is at **m = 15**, 12 laws, two kinds. |
| P3 | permutation targeting ⟹ parity ≡ OR on rings | **CONFIRMED.** 0 divergences; Single-Author holds verbatim on ℤ/m. |
| P4 | balance is parity-only and needs non-injective targeting | **CONFIRMED and made exact.** B(m)=0 under OR, super_or, and every injective target map (26,244 exact counts, 0 violations); exists under parity+non-injective and under supersession with ≥2 kinds; minimum **2 laws**. |
| P5 | rotation speed of an L-cycle is Σ c per L steps | **REFUTED.** Of the L-cycle rotors, 964 satisfy r·L ≡ s·p (mod m) and **4212 do not**. Σc predicts nothing. |
| P6 | cross-amendment maxima exceed the own-kind maxima at equal m | **CONFIRMED at equal state space and equal rule pool** (the honest control): 3 own-kind kinds vs 3 kinds in a 3-cycle gives 2→8, 2→8, 4→20, 6→**81**, 6→54 at m=3..7. New resonance family: **powers of 3** (27, 45, 81 at m=6). |
| P7 | ring rotors do not unroll into ℤ gliders | **CONFIRMED.** 8,332 rotor classes released as finite ℤ codes: 0 gliders (48 holdouts survive a 10× budget as anchored ruler fronts). |
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

**Scope.** 121,806 complete state-space censuses covering **2.78 × 10¹⁰ codes**,
every one of them classified exactly — not sampled. Where a claim rests on
sampling or on SAT decision it says so and gives the bound.

---

## 2. THE PERIOD SPECTRUM

### 2.1 The tables (complete enumerations)

Maximal period attained anywhere in the class, over the complete state space of
every constitution in it:

| class (all rule combinations in the class) | m=3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|
| own-kind, 1 kind (27) | 2 | 2 | 4 | 4 | 4 | 4 | 8 | 15 | 8 |
| own-kind, 2 kinds (729) | 2 | 2 | 4 | 6 | 6 | 8 | 8 | 80 | 12 |
| own-kind, 3 live kinds (1728) | 2 | 2 | 4 | 6 | 6 | — | — | — | — |
| **2-cycle permutation** (reciprocal, 729) | **4** | **6** | **8** | **14** | **16** | **30** | **30** | **80** | **64** |
| **2 kinds, both amending kind 0** (729) | **4** | **6** | **8** | **14** | **16** | **30** | 18 | 65 | **64** |
| **3-cycle permutation, live** (1728) | **8** | **8** | **20** | **81** | **54** | — | — | — | — |
| 3-cycle permutation, all (19683) | 8 | 8 | 20 | — | — | — | — | — | — |
| supersession, 1 kind (27×2) | 2 | 2 | 4 | 4 | 4 | 4 | 8 | 15 | 8 |
| supersession, 2 kinds (729×2) | 2 | 2 | 4 | 5 | 4 | 8 | 8 | 23 | — |
| supersession, 3 live kinds (1728) | 2 | 3 | 6 | 7 | 10 | — | — | — | — |

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
from four laws. 81 = 3⁴ is *not* the order of any element of GL(18,2) whose
semisimple part alone could carry it… but it is 3 × 27, and 27 is: the period
factorises through an occupancy loop, exactly as §2.3 says.

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
constitutions, m ≤ 7, the only ones are **{1,2}**.

**Theorem 2.2 (cross-amendment: block-cyclic, still nilpotent).** *For an
L-cycle permutation constitution the frozen-occupancy step is I+N with N
block-cyclic: (NX)_{k+1} = σ^{c_k}(g_k · X_k). Then N^L is block-diagonal with
k-th block σ^s ∘ diag(mask), s = Σ_{cycle} c_k.* Measured: over **217,728
(constitution, m, occupancy) triples** (m ≤ 8, all 144 live two-kind rule
pairs, all three target classes) N is **always nilpotent** — so single steps are
unipotent under cross-amendment too, and the constant-occupancy period sets are
{1,2} for the 2-cycle and non-injective classes as well.

**So the extra periods are NOT a failure of unipotency.** They are periods of
the *occupancy word* itself. Decomposing every champion cycle as
p = q · ord(T), q = the occupancy period and T the 𝔽₂ monodromy over q steps:

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
the occupancy trajectory, never in a linear resonance sitting on a short
occupancy loop. *(Interpretation.)* Cross-amendment buys its periods by making
the occupancy dynamics richer, not by breaking the 𝔽₂ algebra. What it changes
is **how many laws can be repealed per step and by whom** — under own-kind
targeting only one author can edit a slot, so occupancy changes are a thin
sub-dynamics; under cross-amendment the occupancy word can wander much further
before repeating.

**Lemma S (supersession collapse).** *With a single kind, supersession is
own-kind toggling.* With n=1 a cell is occupied iff kind 0 stands there, so
"enact if empty, clear if occupied" is exactly "toggle kind 0", and the clear
resolution is vacuous. Hence the n=1 rows of the tables coincide identically at
every m ≤ 20, both clear resolutions. *(This is why P8 failed: supersession is
not a variant at all until there are two kinds.)*

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
whole gallery the split is 7,503 transporting to 6,875 barber-pole. *This
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
tiling. ∎ Machine check: **all 8,332 rotor classes lifted to ℤ/2m and ℤ/3m —
16,664 confirmations, 0 failures.** This explains the "extra" rotor classes at
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

Two facts jump out.

**(A) Cross-amendment lowers the minimal rotor ring from 6 to 4.** Own-kind
nomodynamics has *no* rotor at m=4 (complete: 27 kinds × 16 states; 729
two-kind constitutions × 256 states; 1728 three-kind × 4096). Cross-amendment
has 88 classes there. The smallest is three laws (specimen **Q-4** below).

**(B) Odd rings are almost, but not quite, forbidden.** Every complete
enumeration on an odd ring returns zero spatial rotors — see §3.4.

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

### O-15 — THE FIRST ROTOR ON AN ODD RING
constitution: X:(-1,1,1)->X   Y:(0,1,-1)->X           [parity, ring Z/15]
Phi^1(S) = rot_5(S)   laws = 12   barber pole (5 > 2p = 2)
  t=0  |.  XY .  Y  .  X  XY .  Y  .  X  XY X  Y  . |
  t=1  |X  XY X  Y  .  .  XY .  Y  .  X  XY .  Y  . |
  t=2  |X  XY .  Y  .  X  XY X  Y  .  .  XY .  Y  . |
  t=3  = t=0                     (a rigid third-turn of the ring)
```

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

**And yet odd-ring rotors exist.** Deciding the question by SAT rather than by
enumeration (`satrotor.py`: the statement "∃ X ≠ 0 with Φ^p(X) = rot_r(X) and
rot_r(X) ≠ X" is a propositional formula in p·n·m variables) turns up the first
one at **m = 15** — see specimen O-15 and its reciprocal sibling O-15b. Both
were re-verified over three full periods by the xnomos engine. Their minimum
law counts, obtained with a z3 cardinality constraint, are **12** (non-injective,
p=1, rot 5) and **10** (2-cycle permutation, p=2, rot 5).

So the picture is:

> **Odd rings are not forbidden — they are expensive.** Own-kind nomodynamics
> never turns an odd ring. Cross-amendment can, but only from m = 15, only with
> ten to twelve laws, and only as a barber pole: rot 5 = m/3 per step is far
> outside the light cone, so what rotates is a *phase* of a nearly-5-periodic
> code, not a carried packet. The 3-fold near-symmetry is doing the work: Φ acts
> on the code as the rigid third-turn, and the whole orbit is one rotation orbit.

**Open (sharpened).** Is there a *transporting* rotor on any odd ring? None of
the odd-ring witnesses found is one, and the light cone makes the demand
severe: it needs min(r, m−r) ≤ 2p with r ≢ 0 (mod m).

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
window-1 system can display motion at speed m/2 per step. Machine: every rotor
class travels correctly on a 6-fold tiling.

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
laws as a finite code on ℤ gives, over the whole gallery of **8,332 rotor
classes**: 7,757 CYCLE, 416 GROWING, 86 FIXED, 17 BALANCED, 8 EXTINCT, 48
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

