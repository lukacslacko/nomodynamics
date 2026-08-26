# BALLISTIC.md — the glider-collision half of the gate inventory

Expedition Y-B, ballistic sub-expedition. 1-D (ℤ), chapter-two semantics
(occupancy guards, `guards=None`, no citation). Engine:
`/Users/lukacs/claude/math/program/phase6/xnomos.py`.
Code: `/Users/lukacs/claude/math/program/phase6/computation/ballistic_*.py`.
Every number below is a machine result; every box is stated exactly.
This is a **data report**, not RESULTS.md.

Honesty tiers used: `[established]` = machine certificate in this file;
`[interpretation]` = my reading of the data; `[proposal]` = original conjecture.

---

## 0. Specimen verification (T0) — `ballistic_t0_verify.py`, `ballistic_t1_leftmovers.py`

| specimen | constitution | **corrected** seed | p | d | mode | `verify_glider` |
|---|---|---|---|---|---|---|
| TANDEM-1 | `Const([(0,-1,1),(0,-1,0)], targets=[(0,1),(0,1)])` | `state_of([(1,0),(1,1)])` | 1 | +1 | parity **and** or | ✓ |
| SOLO | `Const([(0,1,0),(0,1,1),(0,1,0)], targets=[(1,2),(0,),(0,)])` | `state_of([(1,0)])` | 2 | +1 | parity **and** or | ✓ |
| TRIPTYCH | `Const([(0,1,0),(0,-1,1),(0,1,-1)], targets=[(0,1,2)]*3)` | `state_of([(c,k) for c in (1,2,4) for k in range(3)])` — **all three kinds at each of cells 1,2,4 = 9 laws**, not 3 | 1 | +1 | parity only | ✓ |
| 1-D GUN | `Const([(0,1,0),(0,1,1),(0,1,0)], targets=[(0,1),(0,1),(0,1)])` | `state_of([(0,2)])` | — | — | parity | see below |
| MIRROR-2/5 | `Const([(0,1,-1),(0,-1,1)], targets=[(0,1),(0,1)])` | `{c:3 for c in [2,3,4,6,7,8,9,10,12,13,14,16,18,19,20,21]}` — **32 laws, span 20** | 5 | +2 | parity only | ✓ |

**Corrections recorded.**
* TRIPTYCH's seed as briefed ("all three kinds at cells 1,2,4") was passed to me
  as `[(1,0),(2,1),(4,2)]` (one kind per cell) — that is a **CYCLE of period 2**,
  not a glider. The true seed is the 9-law block. Source: `verify.py:310`.
* The 1-D GUN's law `|S_t| = 2⌊t/2⌋+3` holds for **t ≥ 1 only**: `|S_0| = 1`.
  Machine check t = 0..19: `[1,3,5,5,7,7,9,9,11,11,13,13,15,15,17,17,19,19,21,21]`.
* MIRROR's gliders are far wider than the brief implies; the paste-ready seeds
  are in `xspeed/RESULTS.md §12`. Verified here: p=4 (span 53, 72 laws), p=5
  (span 20, 32 laws), p=12 (span 39, 58 laws), all d=+2, all parity-only.

---

## 1. T1 — LEFT-MOVERS

### 1a. Mirror-image constitutions `[established]`
Negating every offset (`(a,b,c) → (−a,−b,−c)`) and reflecting the seed gives a
certified left-mover for every specimen. All four `verify_glider` certificates ✓:

| left universe | rules | seed | p | d |
|---|---|---|---|---|
| TANDEM-1-L | `[(0,1,-1),(0,1,0)]`, `targets=[(0,1),(0,1)]` | `state_of([(-1,0),(-1,1)])` | 1 | **−1** |
| SOLO-L | `[(0,-1,0),(0,-1,-1),(0,-1,0)]`, `targets=[(1,2),(0,),(0,)]` | `state_of([(-1,0)])` | 2 | **−1** |
| TRIPTYCH-L | `[(0,-1,0),(0,1,-1),(0,-1,1)]`, `targets=[(0,1,2)]*3` | all 3 kinds at cells −4,−2,−1 | 1 | **−1** |
| MIRROR-L | `[(0,-1,1),(0,1,-1)]`, `targets=[(0,1),(0,1)]` | reflected 32-law block | 5 | **−2** |

### 1b. One universe, both directions `[established]`
**MIRROR is PALINDROMIC**: `r₁ = −r₀` and both targets are `{0,1}`, so
`x ↦ −x` (composed with the kind swap 0↔1, which acts trivially here because
every MIRROR glider carries *both* kinds in every occupied cell) is an
**automorphism of the constitution**. Hence

```python
MIR = Const([(0,1,-1),(0,-1,1)], targets=[(0,1),(0,1)])
R   = {c: 3 for c in [0,1,2,4,5,6,7,8,10,11,12,14,16,17,18,19]}   # p=5, d=+2
L   = {-c+19: 3 for c in R}                                        # p=5, d=-2
assert verify_glider(R, MIR, 5,  2, 'parity')
assert verify_glider(L, MIR, 5, -2, 'parity')
```
Both certified. **MIRROR is the ballistic laboratory**: one universe, six glider
species (p = 4, 5, 12 at d = +2 and their d = −2 partners), speeds
1/2, 2/5, 1/6 in each direction.

### 1c. No *small* bidirectional universe `[established, complete box]`
**Box A** — 13 palindromic rule pairs `(r,−r)`, `r ∈ {−1,0,1}³`, × 2 target
patterns (`FULL=[(0,1),(0,1)]`, `RECIP=[(1,),(0,)]`) × 2 modes; seeds = every
non-empty subset of `{0..5}×{0,1}` with cell 0 occupied (complete).
**Result: 0 universes carrying gliders of both signs.**

**Box B** (`ballistic_t1c_bigsweep.py`) — **complete**: n = 2, all 27×27 = 729
rule pairs × 4 target patterns × 2 modes = **5832 universes**; seeds = all
**192** anchored non-empty subsets of `{0,1,2,3}×{0,1}`;
`classify(max_steps=90, max_card=40, max_span=90)`.

* universes carrying ≥1 glider in the box: **88**
* universes carrying **two species that can meet** (opposite d-signs, or equal
  sign with different d/p): **0**
* **GUN candidates** (a GROWING seed that at t = 90 splits into ≥3 mutually
  separated clusters): **0**

> `[interpretation]` Meeting-capable glider pairs are *not* a small-box
> phenomenon at n = 2. MIRROR gets them only because it is palindromic and its
> packets are 20–53 cells wide. There is **no glider gun in Box B**, and a gun
> is exactly what an AND/OR/XOR stream gate needs (see §4).

### 1d. Glider species per specimen universe `[established, complete boxes]`
Complete seed enumeration, cell 0 occupied, both modes:

| universe | box | seeds | species found |
|---|---|---|---|
| TANDEM-1 | cells 0..5, ≤12 laws | 3072 | **1**: (p1,d+1), card 2 |
| SOLO | cells 0..3, ≤4 laws | 538 | **1**: (p2,d+1), card 1 |
| GUN | cells 0..3, ≤4 laws | 538 | **1**: (p1,d+1), card 2, seed `[(0,0),(0,1)]` |
| TRIPTYCH | cells 0..3, ≤5 laws | 1204 | **0** (its glider has 9 laws) |
| MIRROR | cells 0..6, ≤14 laws | 12288 | **0** (its gliders span ≥20) |

---

## 2. T2 — THE COLLISION TABLE

### 2a. MIRROR glider ⨯ glider `[established, complete boxes]`
Engine: `ballistic_t2_mirror.py`, `ballistic_t2_family.py`; outcome certified by
`ballistic_collide.resolve()`, which uses the **separation lemma** proved and
machine-checked in `ballistic_collide.py`:

> If the isolated evolutions satisfy `min(supp Bₜ) − max(supp Aₜ) ≥ 3` for all
> t ∈ [0,N] then `Φᵗ(A ⊔ B) = Aₜ ⊔ Bₜ` on [0,N] (every offset is in {−1,0,1});
> and if both are certified gliders with non-decreasing per-common-period
> displacement, the conclusion extends to **t = ∞**.

All boxes are `mode = 'parity'` (MIRROR's gliders are **not** gliders under OR —
`verify_glider(...,'or') = False` — so the OR half of the box is not a glider
collision at all and is reported as N/A, not as a result).

| pair | geometry | box (phase A × phase B × gap) | N | **outcome** |
|---|---|---|---|---|
| M2/5 → ← M2/5 | head-on | 5 × 5 × 0..40 | **1025** | ARREST 1025 |
| M1/2 → ← M1/2 | head-on | 4 × 4 × 0..24 | **400** | ARREST 400 |
| M1/2 → ← M2/5 | head-on | 4 × 5 × 0..24 | **500** | ARREST 500 |
| M2/5 → ← M1/6 | head-on | 5 × 12 × 0..24 | **1500** | ARREST 1500 |
| M1/6 → ← M1/6 | head-on | 12 × 12 × 0..16 | **2448** | ARREST 2448 |
| M1/2 ⇉ M2/5 | rear-end (1/2 catches 2/5) | 4 × 5 × 0..20 | **420** | ARREST 420 |
| M1/2 ⇉ M1/6 | rear-end | 4 × 12 × 0..16 | **816** | ARREST 816 |
| M2/5 ⇉ M1/6 | rear-end | 5 × 12 × 0..16 | **1020** | ARREST 1020 |
| **total** | | | **8129** | **ARREST 8129** |

**Bucket counts over the whole 8129-run box:**

```
MUTUAL TRANSPARENCY      0
ANNIHILATION             0        (never EXTINCT — the debris always survives)
ARREST                8129        (BALANCED fixed points and stationary CYCLEs)
REFLECTION               0
ABSORPTION               0
FAN-OUT                  0
EXPLOSION                0
UNRESOLVED               0
```

**"Interesting outcome" coordinates: there are none — the box is uniform.**
The only variation is *which* debris: e.g. the M2/5 head-on box (i,j,gap) yields
exactly **8** distinct debris signatures over its 1025 cells —
`BAL(c36)`×357, `BAL(c24)`×255, `BAL(c48)`×253, `CYCLE(p12,c60)`×102,
`BAL(c60)`×50, `CYCLE(p8,c48)`×4, `CYCLE(p8,c40)`×2, `CYCLE(p8,c36)`×2.
The `BAL` debris are **balanced constitutions** — fixed codes with ≥1 *active*
law whose enactments cancel under parity. The larger boxes give 9–28 signatures.

> `[interpretation]` MIRROR is a **perfectly inelastic** ballistic medium. Two
> law-packets that touch always freeze. That is the strongest possible DELETE
> and the worst possible wire.

### 2b. Glider ⨯ stationary obstacle `[established, complete boxes]`
`ballistic_t4_walls.py`. Walls = every stationary code with support in cells
`0..WW−1`, cell 0 occupied (complete enumeration), classified DEAD (FIXED, 0
active laws), BAL (FIXED, ≥1 active law) or OSC (stationary CYCLE, p≥2).
Wall phases capped at 4; glider fired in from the left at every glider phase
and every gap 0..12.

| universe | mode | wall box | seeds | DEAD | BAL | OSC | collision N | outcome |
|---|---|---|---|---|---|---|---|---|
| TANDEM-1 | parity | cells 0..4 | 768 | **0** | **0** | 132 | **4056** | ABSORBED 4056 |
| TANDEM-1 | or | cells 0..4 | 768 | 0 | 0 | 132 | **4056** | ABSORBED 4056 |
| GUN | parity | cells 0..3 | 3584 | **0** | **416** | 0 | **5408** | ABSORBED 5408 |
| GUN | or | cells 0..3 | 3584 | 0 | 0 | 0 | — | no stationary code in the box |
| SOLO | parity / or | cells 0..3 | 3584 | 0 | 0 | 0 | — | no stationary code in the box |
| TRIPTYCH | parity | cells 0..2 | 448 | **24** | 65 | 119 | **2943** | **EXPLOSION 2943** |
| MIRROR | parity | cells 0..4 | 768 | **41** | 14 | 297 | **29205** | ABSORBED 29163, UNRESOLVED 42 |

Collision boxes: glider fired in from the left at every glider phase (TANDEM-1,
GUN, TRIPTYCH have p = 1, so one phase; MIRROR p = 5, phases 0..4), wall phase
`0..min(q,PHCAP)−1` with PHCAP = 4 (TANDEM-1, GUN) or 2 (TRIPTYCH, MIRROR), gap
0..12 (TANDEM-1, GUN) or 0..8 (TRIPTYCH, MIRROR). Budgets: TANDEM-1/GUN
`T_max=220, max_card=300, max_span=600`; MIRROR `T_max=240, max_card=250,
max_span=500`; TRIPTYCH `T_max=200, max_card=120, max_span=200`.

MIRROR by wall type: **DEAD 1845/1845 ABSORBED, BAL 630/630 ABSORBED,
OSC 26688 ABSORBED + 42 UNRESOLVED.** Not one FAN-OUT, REFLECT, TRANSPARENT or
WALL-DESTROYED in 29 205 runs.

TRIPTYCH is the **opposite extreme from MIRROR** `[established]`: every one of
its 2943 glider-vs-wall collisions EXPLODES (grows past the span/card budget).
Perfectly elastic-to-the-point-of-detonation, and therefore also gateless: no
certified outcome exists to read a bit off.
(TRIPTYCH's OR-mode sweep — 171 stationary codes, N = 2862 — gives EXPLOSION
2590 / ABSORBED 272, but it is **not** a glider experiment: the 9-law block is
not a glider under OR, so that row is excluded from all totals below.)

**TANDEM-1 has no dead-letter wall at all** `[established]`: its guard makes a
law at cell *i* active iff cell *i−1* is empty, and the leftmost law of any
finite code always has an empty cell to its left. So every finite TANDEM-1 code
has ≥1 active law — a Dead-Letter-Theorem-style obstruction at the level of the
constitution, not the box.

### 2c. Glider ⨯ collision debris `[established, stated box]`
`ballistic_t3_gates.py`, last section. Box: **35** distinct debris states
harvested from the T2 head-on sweep (phases 0..4 × 0..4 × gap ∈ {0,3,7,11}),
each used as an obstacle; a fresh MIRROR-2/5 right-mover fired in at every
phase 0..4 and every gap 0..24 → **N = 4375**.

```
ABSORBED    4368
UNRESOLVED     7        (budget T_max=300, max_card=400, max_span=900)
FAN-OUT        0
REFLECT        0
TRANSPARENT    0
```

---

## 3. T3 — THE GATE TABLE (ballistic sector)

Convention: a **right wire** carries a bit as the presence/absence of the
(5,+2) MIRROR glider on a fixed launch range at t=0; a **left wire** likewise
with (5,−2). A **constant** is a glider planted as part of the geometry. A gate
is certified when all 2ᵏ input cases run through the **same** geometry and the
output port — a fixed (time, cell-window) — holds the right bit, the bit read by
`verify_glider` on the window content.

### GATE 1 — AND-NOT / DELETE / INHIBIT `[established]` — **certified**
`ballistic_t3_gates.py`. Universe `MIRROR`, `mode='parity'`.

```python
import sys; sys.path.insert(0, '/Users/lukacs/claude/math/program/phase6')
from xnomos import Const, state_of, step, verify_glider
MIR = Const([(0,1,-1),(0,-1,1)], targets=[(0,1),(0,1)])
A = {c:3 for c in [ 0, 1, 2, 4, 5, 6, 7, 8,10,11,12,14,16,17,18,19]}  # right wire
B = {c:3 for c in [40,41,42,43,45,47,48,49,51,52,53,54,55,57,58,59]}  # left  wire
# gap 20.  Run 200 steps.
# RIGHT PORT = cells [60,400]   bit = verify_glider(window, MIR, 5,  2)
# LEFT  PORT = cells [-400,-5]  bit = verify_glider(window, MIR, 5, -2)
```

| A | B | state at T=200 | RIGHT port | LEFT port |
|---|---|---|---|---|
| 0 | 0 | empty | 0 | 0 |
| 0 | 1 | cells −40..−21, card 32 | 0 | **1** |
| 1 | 0 | cells 80..99, card 32 | **1** | 0 |
| 1 | 1 | cells 16..43, card 24, **BALANCED** | 0 | 0 |

**RIGHT = A ∧ ¬B ✓  LEFT = B ∧ ¬A ✓** — one gadget, two ports, both AND-NOT.

### GATE 1b — CASCADE `[established]` — **certified**
`ballistic_t3_cascade.py`. Same universe. A right on 0..19; B left on 40..59;
C left on 300..319. Read the right port at T=800, cells [200,4000].
All **8** input cases:

| A B C | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |
|---|---|---|---|---|---|---|---|---|
| out | 0 | 0 | 0 | 0 | **1** | 0 | 0 | 0 |

`out = A ∧ ¬B ∧ ¬C` ✓ — **the AND-NOT output is a real glider that drives the
next stage.** AND-NOT cascades.

### GATE 2 — WALL-DELETE (static control) `[established]` — **certified**
Universe `TANDEM-1`. `A = state_of([(0,0),(0,1)])` (the (1,+1) glider);
`W = state_of([(20,0),(20,1),(21,0)])` (a period-2 stationary CYCLE).
Observe T = 40, window cells [30,60].

| A | W | port | out |
|---|---|---|---|
| 0 | 0 | — | 0 |
| 0 | 1 | — | 0 |
| 1 | 0 | `{40: 3}` | **1** |
| 1 | 1 | — | 0 |

`out = A ∧ ¬W` ✓. **Honest limits:** W is a *static* control, not a travelling
signal, so no gate output can drive it — this gate does not cascade. And the
wall is **consumed**: the residue is a *different* card-1/3 period-2 oscillator
one cell to the right, so the gate is **one-shot**.

### GATE 3 — NOT `[established]` — **certified**
Same MIRROR geometry as Gate 1 with **B planted as a constant 1**. Input A on
the right wire, output on the LEFT port at T=200, cells [−400,−5]:

| A | out |
|---|---|
| 0 | **1** |
| 1 | 0 |

`out = ¬A` ✓. **NOT flips polarity**: a right-wire input yields a left-wire
output. There is no same-polarity NOT in this sector.

### GATE 4 — XOR, non-local readout `[established, weaker]`
Same geometry as Gate 1; output = **the number of certified free gliders
anywhere in the universe at T = 200**.

| A B | 00 | 01 | 10 | 11 |
|---|---|---|---|---|
| #free | 0 | 1 | 1 | **0** |

`#free = A ⊕ B` ✓. Marked weaker because the readout is **not a single spatial
port** — you must inspect the whole line. Reading either single port and OR-ing
the two bits gives the *same* table, i.e. **the two-port OR is in fact XOR**
(machine-checked in `ballistic_t3_logic.py`).

### DUPLICATE / FAN-OUT — **not found** `[established, exact box]`
Searched, complete over the stated boxes:

| experiment | N | fan-outs |
|---|---|---|
| MIRROR glider ⨯ glider (8 pairs, §2a) | 8129 | **0** |
| MIRROR glider ⨯ 35 collision-debris walls, phase 0..4 × gap 0..24 | 4375 | **0** |
| MIRROR glider ⨯ all 352 stationary codes in cells 0..4 (§2b) | 29205 | **0** |
| TANDEM-1 glider ⨯ all 132 stationary codes in cells 0..4, both modes | 8112 | **0** |
| GUN glider ⨯ all 416 balanced codes in cells 0..3, parity | 5408 | **0** |
| TRIPTYCH glider ⨯ all 208 stationary codes in cells 0..2, parity | 2943 | **0** |
| GUN glider ⨯ the immortal kind-2 source, gap 0..30 | 31 | **0** |
| **total** | **58 203** | **0** |

**No fan-out in the box** `[established]`. Also **no REFLECT** and **no
TRANSPARENT** anywhere in the same 58 203 runs.

### REFLECT — **not found in the box** `[established]`
Zero REFLECT outcomes in all 58 203 collision runs above. Left-moving gliders
exist (§1), but no experiment in these boxes turns a right-mover into one.

### The detector is not the reason `[established]` — `ballistic_selftest.py`
Six positive controls, all passing, prove `resolve()`/`bucket()` really do see
the empty buckets: two certified gliders moving apart are bucketed
**TRANSPARENCY** (with `forever = True`); three spreading gliders from one input
are bucketed **FAN-OUT**; a surviving glider next to a surviving wall is bucketed
**ABSORPTION**; a right input with a left output is bucketed **REFLECTION**;
EXTINCT is bucketed **ANNIHILATION**; and the separation lemma is re-verified
step-by-step for 200 steps on the control. The zeros above are results, not
blind spots.

### AND / OR on two glider streams — **not found**, with the mechanism `[established]`
`ballistic_t3_logic.py`, GATE 5/6. The natural two-stage AND
(`A → ¬A` by Gate 3, then `B ∧ ¬(¬A)`) is machine-run on all 4 cases and
**fails at A=1,B=1**:

```
A=0 B=0 -> 0   clusters: [(-320,-301,32,'G-2')]
A=0 B=1 -> 0   clusters: 3 stationary
A=1 B=0 -> 0   clusters: 3 stationary
A=1 B=1 -> 0   clusters: [(-6,9,24,'stat'),(13,34,30,'stat'),(41,43,6,'stat')]
```

**Failure mechanism (machine-visible).** When A = 1 the stage-1 collision leaves
**balanced debris standing in B's lane**, and every one of the 4375
glider-vs-debris runs is ABSORBED. In one spatial dimension there is no second
lane to route B around the debris and no certified transparent obstacle, so
B dies and `A∧B` reads 0 instead of 1.

> `[proposal] The 1-D ballistic obstruction.` In an inelastic 1-D medium
> (every collision arrests, no collision is transparent, no collision fans out)
> the gate set reachable by ballistic collision is exactly the **monotone-
> decreasing** one: AND-NOT and its cascades, NOT across polarity, and XOR only
> under a non-local readout. AND, OR and fan-out all require either a
> transparent crossing or a second lane, neither of which exists on ℤ. Getting
> them needs a *gun* (a constant-1 stream) — and Box B contains none.

### Reusability `[established]`
`ballistic_t3_gates.py`: fire two right-movers (200 cells apart) at one B.
* B = 0 → 2 clusters at T=900, **both certified (5,+2) gliders**.
* B = 1 → 3 clusters, **all stationary**: the debris eats the second shot too.

So the MIRROR AND-NOT gate is **one-shot**: after it fires it leaves a permanent
wall on the wire.

---

## 4. What I could NOT find (exact box statements)

* **No glider gun** in Box B (5832 universes × 192 seeds, complete). No source
  of a periodic free-glider stream, so the "AND/OR/XOR on two glider streams"
  task of T3 has no stream source in the searched box.
* **No MUTUAL TRANSPARENCY** in 8129 MIRROR glider-glider runs (complete boxes
  in §2a) and none in 50 074 glider-vs-obstacle runs (§2b, §2c).
* **No FAN-OUT / DUPLICATOR** in 58 203 runs (§3).
* **No REFLECTION** in 58 203 runs (§3).
* **No ABSORPTION with a *surviving glider*** in any MIRROR glider-glider run —
  the DELETE gate works by *mutual* arrest, not by one glider eating another.
* **No bidirectional universe with small packets**: Box A (13 palindromic pairs
  × 2 target patterns × 2 modes, seeds in cells 0..5, complete) and Box B both
  return 0.
* **No same-polarity NOT** and **no AND / OR** gate; the failure mechanism is
  §3 GATE 5.
* GUN universe: a glider fired into the immortal kind-2 source at gaps 0..30
  gives **UNRESOLVED for all 31 gaps** (`T_max=200, max_card=300, max_span=500`)
  — the gun's front and the glider both move at speed 1, so they never separate
  and no free glider emerges on the far side. Not a certified outcome; the box
  simply does not resolve.

---

## 5. Grand total

**58 203** certified collision runs across all boxes. Bucket totals:

```
ARREST / ABSORBED (a signal dies, the obstacle stays)   55 180
   = 8129 glider-glider ARREST + 4368 vs debris + 29163 vs MIRROR walls
   + 8112 vs TANDEM-1 walls + 5408 vs GUN walls
EXPLOSION (TRIPTYCH, every one of its wall collisions)   2 943
UNRESOLVED (budget exhausted: 7 + 42 + 31)                   80
MUTUAL TRANSPARENCY                                          0
ANNIHILATION (EXTINCT)                                       0
REFLECTION                                                   0
FAN-OUT / DUPLICATION                                        0
```

---

## 6. Files

| file | what |
|---|---|
| `ballistic_lib.py` | helpers: mirror_const, mirror_state, orbit, find_gliders |
| `ballistic_collide.py` | separation lemma + `resolve()` + buckets |
| `ballistic_t0_verify.py` | specimen reproduction |
| `ballistic_t1_leftmovers.py` | T1a/b/c: mirror constitutions, palindromic search |
| `ballistic_t1b_species.py` | glider species per specimen universe |
| `ballistic_t1c_bigsweep.py` | Box B: 5832 universes (→ `ballistic_meeting_universes.json`) |
| `ballistic_t2_mirror.py` | MIRROR-2/5 head-on, gap 0..40 (→ `ballistic_mirror_headon.json`) |
| `ballistic_t2_family.py` | head-on across species + rear-end (→ `ballistic_family_all.json`) |
| `ballistic_t3_gates.py` | GATE 1, GATE 2, reusability, debris fan-out hunt |
| `ballistic_t3_cascade.py` | GATE 1b cascade |
| `ballistic_t3_logic.py` | GATE 3 NOT, GATE 4 XOR, GATE 5/6 AND/OR attempts |
| `ballistic_t3_extras.py` | wall-delete spacetime, glider-vs-gun |
| `ballistic_t4_walls.py` | T4 wall enumeration + glider-vs-wall sweeps |
| `ballistic_t4_trip.py`, `ballistic_t4_mirwall.py`, `ballistic_t4_dead.py` | T4 TRIPTYCH / MIRROR / dead-letter wall sweeps |
| `ballistic_selftest.py` | 6 positive controls for the outcome detector |
