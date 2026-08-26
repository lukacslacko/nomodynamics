# Expedition Y-B — the computation question

*Gate inventory and universality for nomodynamics.  Chapter-three (citation)
sector, chapter-two (anonymous, occupancy-guard) sector, and the ballistic
(glider-collision) sector.*

> **The headline.**  Nomodynamics is computation-universal, and it does not need
> chapter three to be so.  Every Turing machine compiles into a **finite code**
> of the **founding, occupancy-guard sector**, with a fixed constitution, a
> fixed window and time dilation 3.  Rule 110 runs exactly in a **24-kind,
> window-1** citation constitution and in a **31-kind, out-degree-1** anonymous
> one.  In the computing part of both machines **nothing travels**: every gate
> law stands exactly where it was enacted, forever.  The Out-Degree Law is not
> contradicted — it is *bypassed*.  Motion was never the resource; the
> **vacancy clause** was, and a matching theorem shows that when the guard goes
> vacuous the whole field collapses to 𝔽₂-linear algebra.

---

## 0. Pre-registration (frozen before the first big run)

Written after reading `README.md`, `XFINDINGS.md`, `CITATION.md` and `xnomos.py`,
after exactly three scratch probes (an AND-NOT guard, an XOR-merge with a
constant, and a one-cell-per-step signal track), and **before** any census,
compiler, circuit, Rule-110 attempt or collision sweep was written.  Kept as
found.

- **B1 — the citation sector is a circuit substrate, and the gates are cheap.**
  The guard `g at i+a ∧ ¬(h at i+b)` is a two-input AND-NOT read at fixed
  offsets, and a target cell that is toggled accumulates by XOR.  I expect
  AND-NOT, XOR, NOT, fan-out and a unit-delay wire all to exist as *one-law*
  gadgets at window 1.  Confidence: high (the three probes already show
  AND-NOT and XOR-merge).
- **B2 — the expensive primitive is not a gate but ASSIGNMENT.**  Toggling
  accumulates; a wire must be cleared before it is rewritten.  Prediction: the
  clean fix is a *self-clearing kind* (rule `(0,0,0)`, target itself, guard
  always true), which converts `x ⊕= f` into `x ← f`.  Confidence ≈ 0.8.
- **B3 — a full synchronous Boolean circuit compiles, at window 1, with a
  fixed finite constitution.**  Prediction: there is a single citation
  constitution on ℤ, with a fixed number of kinds and offsets in `{−1,0,1}`,
  into which an *arbitrary* fan-in-2 Boolean circuit can be laid out as a
  placement of immortal laws.  Confidence ≈ 0.6.
- **B4 — Rule 110 falls.**  Given B3, a Rule-110 cell is a five-gate circuit
  (`q ⊕ r ⊕ qr ⊕ pqr`) and should simulate with a small constant time dilation.
  Confidence ≈ 0.5.  Universality then holds for the class of codes Rule 110's
  own universality proof needs (ultimately periodic backgrounds), **not**
  automatically for finite codes.
- **B5 — the finite-code gap is the real difficulty, and I may not close it.**
  Nomodynamics codes are *finite*.  Simulating a machine with an unbounded tape
  needs hardware that builds itself ahead of the head.  Confidence that a
  self-extending hardware front is built and certified this cycle: ≈ 0.35.
- **B6 — P-completeness falls out cheaply and is the safe floor.**  A circuit
  simulation with log-space-computable layout reduces the Circuit Value Problem
  to nomodynamic prediction.  Confidence ≈ 0.75.  I expect this to be the
  result that survives even if B4/B5 fail.
- **B7 — ballistic gates are *harder*, not easier.**  Against the Life
  intuition: I predict the glider-collision sector yields **absorption and
  reflection readily but fan-out badly**, because chapter two's collision
  parity rule (even gap ⇒ mutual transparency) means colliding writs mostly
  *ignore* each other, and transparency is the enemy of interaction.
  Prediction: ≥ 1 certified reflector, ≥ 1 certified absorber (deleter),
  and **no** certified ballistic fan-out (duplicator) from a bounded sweep.
  Confidence ≈ 0.55.  *(Recorded as a box statement, per the width correction.)*
- **B8 — the single-author sector is NOT provably poly-time predictable, and I
  expect I will fail to prove it.**  Given occupancy, per-kind dynamics is
  𝔽₂-linear — but occupancy is itself the nonlinear part, and occupancy is a
  function of the kind fields.  Prediction: linearity gives a *conditional*
  poly-time algorithm only, and no unconditional non-universality theorem.
  Confidence ≈ 0.7 that the obstruction does not close.
- **B9 — what I do not expect.**  I do not expect a replicator (Y5), I do not
  expect the ballistic sector to reach universality, and I do not expect to
  find any *new* glider.  This expedition is about gates, not fauna.

**The honesty bar I am holding myself to:** a universality claim requires an
explicit constitution, an explicit encoding, an explicit composition argument,
and a machine check of the simulation against an independent reference
implementation.  Anything less is reported as "ingredients present".

---

## 1. The one idea: a provision that repeals itself

Every construction below rests on a three-line observation.

A citation guard — and, it turns out, the **founding occupancy guard** too —
is an AND-NOT read at fixed offsets.  Targets are *toggled*, so several authors
of the same provision XOR together.  AND-NOT plus XOR plus a constant is
functionally complete.  The one thing missing is **assignment**: a toggle
accumulates, and a wire must be cleared before it can be rewritten.

> **The self-clearing kind.**  Let kind `v` have rule `(0,0,0)`, a guard that is
> vacuously true, and target `{v}`.  A law of kind `v` at cell `j` is then
> active whenever it stands, and it toggles *itself*: it repeals itself every
> step.  Therefore, with `f(t)` the XOR of every other author's toggle of `v` at
> `j`,
>
>     x(t+1) = x(t) ⊕ x(t) ⊕ f(t) = f(t).
>
> A provision that expires every step is a **register**: the code writes it
> rather than amending it.  (`statute.py`)

That single trick converts nomodynamics from an amendment calculus into a
synchronous logic array.  A law that stands forever (nobody amends it) is a
**gate**; a law that repeals itself every step is a **wire**.

**THEOREM 1 (Statute-Circuit Theorem).**  Call a constitution *normal* if its
kinds split as `K = V ⊎ G ⊎ {NIL}` with

* (W) every `v ∈ V`: rule `(0,0,0)`, guard `(v, NIL)`, target `{v}`;
* (G) every `g ∈ G`: rule `(a,b,c)`, guard `(p,n)` with `p ∈ V ∪ {g}`,
  `n ∈ V ∪ {NIL}`, target `T_g ⊆ V`;
* (N) `NIL` is in no target set and is never placed;
* (I) no `g ∈ G` is in any target set.

Then under **parity** resolution, for every cell `j` and wire `v`,

    x[j,v](t+1) = ⊕ over gates g and cells i with i+c_g = j and v ∈ T_g
                  of   [g stands at i] ∧ [p_g at i+a_g] ∧ ¬[n_g at i+b_g],

and the placement of the `G`-laws is constant in time.

*Proof.* `step` accumulates, per `(cell,kind)`, the parity of all toggles.  The
only toggles of kind `v` at `j` are the self-clearing `v`-law at `j` (which
contributes `x[j,v]`) and the gates above; `x ⊕ x = 0`.  Gates are never
targeted, so they never move or vanish. ∎

*Certificate*: **2 000 random normal-form constitutions × random codes, 0
deviations** from the predicted circuit semantics (`statute.certify_selfclear`),
plus the normal-form audit re-derived from the raw `Const` in every experiment.

So a normal-form constitution **is** a synchronous AND-NOT network with free
XOR fan-in, free fan-out (guards are read-only, so any number of gates may cite
the same `(cell,kind)`) and unit delay.

---

## 2. The gate table

Every row is certified by exhaustion: all 2² input assignments, run to the
stated depth, then observed for **six further steps** to confirm the output is
stable.  Nothing is written into the state after `t = 0`: the inputs are held by
immortal *source* laws that are part of the constitution, so each row is one
code evolving under one law.  Re-derived independently in `verify_y.py` from
hand-written `(a,b,c)`/target/guard tuples.

### 2.1 Citation sector (chapter three), window 1, parity

| gate | depth | gate laws | kinds | table `uv=00,01,10,11` | how |
|---|---|---|---|---|---|
| `ZERO` | 0 | 0 | 6 | `0000` | no gate at all |
| `ONE` | 1 | 1 | 7 | `1111` | `cite(self@0, ¬NIL) → {Y}` |
| `BUF` | 1 | 1 | 7 | `0011` | `cite(U@0, ¬NIL) → {Y}` |
| `NOT` | 1 | 1 | 7 | `1100` | `cite(self@0, ¬U@0) → {Y}` |
| **`ANDNOT`** | **1** | **1** | 7 | `0010` | **the guard, verbatim** |
| `IMPL` | 1 | 2 | 8 | `1101` | `ANDNOT ⊕ 1` |
| `XOR` | 1 | 2 | 8 | `0110` | two authors of one provision |
| `XNOR` | 1 | 3 | 9 | `1001` | `XOR ⊕ 1` |
| `AND` | 2 | 2 | 9 | `0001` | `¬v` then `u ∧ ¬(¬v)` |
| `NAND` | 2 | 3 | 10 | `1110` | `AND ⊕ 1` |
| `OR` | 2 | 3 | 10 | `0111` | `¬(¬u ∧ v)` |
| `FANOUT` | 1 | 1 | 9 | `1→3` | one law, three targets — **free** (also 3 laws, 11 kinds) |
| `WIRE` | 1/cell | 1 | 3 | — | signal moves 1 cell/step through *static* hardware |

`AND` and `OR` cost depth 2 only because one input must be negated first.  In a
**dual-rail** layout (every wire carried with its complement, as in the Rule-110
machine below) **`AND` is one law at depth 1**, and the complement of any gate
is free: add the complement wire to the gate's target set and one constant.

**Fan-out is free** and this is the decisive difference from the ballistic
style.  A guard is *read-only*: any number of gates, at any number of cells, may
cite the same `(cell, kind)` without disturbing it.  In Life, fan-out is the
expensive gadget; here it is not a gadget at all.

### 2.2 Anonymous sector (chapters one and two), occupancy guards, `guards=None`

**The same table, every row, with `guards=None`.**  See §4.

---

## 3. Rule 110 inside a citation constitution

`rule110.py`.  Rule 110 is `y_n = x_n ⊕ x_{n+1} ⊕ x_n x_{n+1} ⊕ x_{n−1} x_n x_{n+1}`.
The machine is **24 kinds, window 1, parity, time dilation 3, space dilation 1**
— one Rule-110 cell is one nomodynamics cell.

```
wires   X Xb      the bit and its complement                     (phase 0)
        A Ab      A = x_n & x_{n+1}, and its complement          (phase 1)
        X1        x_n delayed                                    (phase 1)
        X2 A2 B   x_n, A, and B = x_{n-1} & A                    (phase 2)
        K0 K1 K2  a three-phase clock, present at every cell

phase 0 gA   cite(X@0, ¬Xb@+1) -> {A, Ab}     A  <- x_n & x_{n+1}
        gX1  cite(X@0, ¬NIL)   -> {X1}
        kK0  cite(K0@0,¬NIL)   -> {K1, Ab}    clock + the 1 that makes Ab = ¬A
phase 1 gB   cite(X1@-1,¬Ab@0) -> {B}         B  <- x_{n-1} & A
        gX2  cite(X1@0,¬NIL)   -> {X2}
        gA2  cite(A@0, ¬NIL)   -> {A2}
        kK1  cite(K1@0,¬NIL)   -> {K2}
phase 2 gY0  cite(X2@0, ¬NIL)  -> {X, Xb}     the four terms of the Rule-110
        gY1  cite(X2@+1,¬NIL)  -> {X, Xb}     polynomial, XOR-merged into X
        gY2  cite(A2@0, ¬NIL)  -> {X, Xb}
        gY3  cite(B@0,  ¬NIL)  -> {X, Xb}
        kK2  cite(K2@0, ¬NIL)  -> {K0, Xb}    clock + the 1 that makes Xb = ¬X
```

Every gate is **self-timed**: its input wire exists only in its own phase, so
the three stages fire in sequence with no clocking beyond `K0/K1/K2`.

**Paste-ready** (kinds `0=NIL, 1=X, 2=Xb, 3=A, 4=Ab, 5=X1, 6=X2, 7=A2, 8=B,
9=K0, 10=K1, 11=K2, 12=gA, 13=gX1, 14=kK0, 15=gB, 16=gX2, 17=gA2, 18=kK1,
19=gY0, 20=gY1, 21=gY2, 22=gY3, 23=kK2`):

```python
rules   = [(0,0,0)]*12 + [(0,1,0),(0,0,0),(0,0,0),(-1,0,0),(0,0,0),(0,0,0),
                          (0,0,0),(0,0,0),(1,0,0),(0,0,0),(0,0,0),(0,0,0)]
targets = [(), (1,),(2,),(3,),(4,),(5,),(6,),(7,),(8,),(9,),(10,),(11,),
           (3,4),(5,),(10,4),(8,),(6,),(7,),(11,),(1,2),(1,2),(1,2),(1,2),(9,2)]
guards  = [(0,0),(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0),(8,0),(9,0),(10,0),
           (11,0),(1,2),(1,0),(9,0),(5,4),(5,0),(3,0),(10,0),(6,0),(6,0),(7,0),
           (8,0),(11,0)]
C = Const(rules, targets, dim=1, guards=guards)
# phase-0 code: kinds 12..23 and kind 9 (K0) at EVERY cell of the tape,
#   plus kind 1 (X) where the Rule-110 bit is 1 and kind 2 (Xb) where it is 0.
# Then step 3 times per Rule-110 step, under mode='parity'.
```

### 3.1 The certificate is COMPLETE, not a sample

Every offset lies in `{−1,0,+1}`, so one step moves information at most one
cell and the 3-step map is a **local map `f : {0,1}⁷ → {0,1}`**.  Running all
**2⁷ = 128** configurations of the ring `ℤ/7` evaluates `f` at *every one of its
inputs*.  Agreement there is agreement on ℤ **for every configuration, finite or
infinite**.  That is `certify_local()`, and it is a complete enumeration, not a
box.

Redundant checks, all EXACT:

| check | scope |
|---|---|
| local map | **all 128** configurations of `ℤ/7` — decides ℤ entirely |
| `ℤ/8 … ℤ/12` | **all** 256 / 512 / 1024 / 2048 / 4096 configurations × 16 Rule-110 steps |
| `ℤ/13` | 12 seeds × 40 Rule-110 steps (independent bit-parallel reference) |
| `ℤ/17` | 200 random configurations × 60 Rule-110 steps |
| phase purity | at every `t = 3k`: `K0` at every cell, exactly one of `X`/`Xb` per cell, all eight other wires empty, and the 12 gate laws in exactly their original cells — 30 checkpoints |
| on ℤ | hardware on `[0,39]`, light-cone interior correct for 12 Rule-110 steps |

The reference implementation in `verify_y.py` is the bit-parallel integer form
`y = x ^ r ^ (x&r) ^ (l&x&r)`, written independently of the table lookup in
`rule110.py`.

### 3.2 The machine at work

Four Rule-110 steps (12 nomodynamics steps) on `ℤ/14`, seeded with the ether:

```
  t= 0 K0  X=...#..##.#####  A=..............  X1=..............  X2=..............  B=..............
  t= 1 K1  X=..............  A=......#..####.  X1=...#..##.#####  X2=..............  B=..............
  t= 2 K2  X=..............  A=..............  X1=..............  X2=...#..##.#####  B=..........###.
  t= 3 K0  X=..##.#####...#  A=..............  X1=..............  X2=..............  B=..............
  t= 4 K1  X=..............  A=..#..####.....  X1=..##.#####...#  X2=..............  B=..............
  t= 5 K2  X=..............  A=..............  X1=..............  X2=..##.#####...#  B=......###.....
  t= 6 K0  X=.#####...#..##  A=..............  X1=..............  X2=..............  B=..............
  t= 7 K1  X=..............  A=.####.......#.  X1=.#####...#..##  X2=..............  B=..............
  t= 8 K2  X=..............  A=..............  X1=..............  X2=.#####...#..##  B=..###.........
  t= 9 K0  X=##...#..##.###  A=..............  X1=..............  X2=..............  B=..............
```

The bit field `X` exists only in phase 0; between phases the computation lives
in `A`, `X1`, `X2`, `B`.  The Rule-110 ether drifts left at one cell per step,
inside the statute book.

---

## 4. **Citation was not necessary.** The founding sector already computes.

`anon.py`.  `CITATION.md` predicted (Y3) that the first credible universality
construction would live in the citation sector.  **That prediction is refuted.**

The founding guard is *already* an AND-NOT:

> *"some law stands at `i+a` **and** no law stands at `i+b`"*

— an AND-NOT over the **occupancy** field.  What citation buys is only that
several independent bits may share one cell.  Give up that convenience and
spend **cells** instead of **kinds**, and the entire circuit substrate
reappears with `guards=None`.

**The layout.**  Each logical *site* is a block of `L = r+2` consecutive cells:

```
[ w_0 | w_1 | ... | w_{r-1} | POWER | GAP ]
```

* `w_i` is a **wire cell**: occupied ⇒ the bit is 1, empty ⇒ 0.  Its kind has
  rule `(0, r+1−i, 0)` and targets itself.  The precedent clause reads *its own
  cell*, which is occupied exactly when the law stands there — vacuously
  satisfied.  The vacancy clause reads the block's `GAP`, empty forever.  So the
  law is always active and repeals itself: the self-clearing wire, again.
* `POWER` carries one law with rule `(0,0,0)`.  Since `a = b`, its guard is
  self-contradictory: it **never acts**, and nobody amends it, so it stands
  forever.  This is the field's own *unconditional dead letter*
  (`xrings/RESULTS.md`, P9) used as scaffolding.  Every **gate law** is placed
  in this cell, which is therefore permanently occupied — so a gate whose
  `a`-offset is `0` is unconditionally enabled.
* `GAP` is targeted by nothing, so it is empty forever: the constant FALSE that
  every vacancy clause needs.

A gate is then **one law** with rule `(a,b,c)` reading two wire cells and
toggling the wire kind of a third.  **Its out-degree is 1.**

> **THEOREM 4.**  The anonymous (occupancy-guard) sector is computation-universal
> on ultimately-periodic-hardware codes, at **out-degree 1** — inside the very
> sector the Out-Degree Law proves incapable of motion.

**Exactly which sector this is, said precisely.**  The *guards* are chapter
one's, verbatim: `Const.cited == False`, no guard names a kind.  The *targeting*
is chapter two's: a gate kind amends a wire kind other than itself, so this is
**cross-amendment at out-degree 1** — the single-target sector, the one X-A
proved has no free glider and X-D's 286-million-run periodic table found empty.
It is **not** chapter one's own-kind sector (`T_k = {k}`); see §11.2.  Nothing
from chapter three is used, and `guards=None` is passed to `Const`.

**The same 11-row gate table** (§2.1) certifies in this sector, exhaustively
(`anon.certify_gate`).  And the **same Rule-110 circuit** compiles:

| | citation | anonymous |
|---|---|---|
| kinds | **24** | **31** |
| window | **1** | 20 |
| cells per Rule-110 cell | **1** | 13 |
| max out-degree | 2 | **1** |
| guards | citation | **`guards=None`** |
| time dilation | 3 | 3 |
| complete certificate | all 2⁷ configs of `ℤ/7` | all 2⁷ configs of the 7-site ring |
| further | `ℤ/8…12` complete, `ℤ/13`, `ℤ/17` | 8-, 9-, 10-site rings complete × 12 steps |

The locality argument that makes the 2⁷ enumeration *complete* is itself
machine-checked here: `AnonMachine.site_locality()` reads every rule off the raw
`Const`, resolves each offset to a `(site, slot)` pair, and certifies that every
wire law stays inside its own site and every gate law reads only wire slots at
site offsets in `{−1,0,+1}` and writes only its own site's wires — **radius 1
site, 0 violations**.  Hence the 3-step map is site-local of radius 3 and the
7-site ring exhausts its inputs.

### 4.1 Computation without transport

This does **not** contradict the Out-Degree Law, the Anchor Theorem or
Path-Sum Confinement.  Those are theorems about *free gliders* — about packets
of law that travel.  Here **nothing travels**.  The battery certifies it:

> `no free glider: every gate law and every POWER law is exactly where it was`
> — 60 steps, out-degree 1.

Chapter one already drew this distinction once, and had to retract a claim over
it: the ℤ/6 "ring rotor" was found to be a **barber pole** — a code that
coincides with its own rotation while nothing hops.  The same distinction now
pays: **a statute book can compute while every one of its provisions stands
still.**  What moves is not law; it is *information*, and information moves
because the guards read across cells.

> *Motion was never the resource.  The vacancy clause was.*

---

## 5. **Finite-code universality**: every Turing machine as a finite code

Rule 110's universality theorem (Cook 2004; Neary–Woods 2006) concerns
configurations with infinite ultimately-periodic backgrounds.  A nomodynamic
**code is finite**.  §3 and §4 therefore give universality *relative to the
hardware supplied*, i.e. for codes that are ultimately periodic.  This section
closes the gap outright, without going through Rule 110 at all.

`turing.py` (citation) and `anontm.py` (anonymous).

> **THEOREM 5.**  For every Turing machine `M` over the binary tape alphabet
> there is a constitution `N*(M)` — dimension 1, finitely many kinds, finite
> window, **occupancy guards only** — and a **finite code** `C(M,x)` such that
> the code at step `3t` decodes to the configuration of `M` on `x` after `t`
> steps, for every `t`.  The simulated tape is **unbounded**: the code grows by
> two blocks per step.  Every kind of `N*(M)` except the **eighteen** kinds of
> the two building fronts has **out-degree 1**.

Two ingredients beyond §1.

**(1) Latches.**  A self-clearing wire lives one step.  Add a *hold* gate
`cite(v@0, ¬KILL@0) → {v}` and the wire re-enacts itself every step: a register
that persists until the `KILL` phase.  With `KILL = NIL` it persists forever and
any other author toggling it acts as a **T flip-flop** — which is exactly how
the tape bit `T` is written.

**(2) The building front.**  Gate laws are immortal, so hardware cannot grow —
but a finite code carries only finitely much of it.  A front of **nine kinds per
side**, phase-tagged, walks outward at **one site per step**:

```
P_j (a=0, b=+1, c = s·L)  -> {P_{j+1}, Q_{j+1}, R_{j+1}, POWER, every gate law}
R_j (a=0, b=+1, c = s·L + slot(K_{j+1}) − r)   -> {K_{j+1}}
Q_j (a=0, b=+1, c = 0)    -> {P_j, Q_j, R_j}
```

`a = 0` reads the front's own cell, permanently occupied by `POWER`, so the
precedent clause is vacuous; `b = +1` reads the block's `GAP`, empty forever, so
the vacancy clause is vacuous; the triple fires every step.  `P` enacts the
complete hardware of the next block one site ahead together with the next front,
`R` enacts that block's clock wire *in the phase it will need*, and `Q` repeals
the front where it stands.  **This is the TANDEM-1 mechanism at block scale** —
one kind enacts the pair one cell ahead, its partner repeals the pair where it
stands — and it is the *only* place in the whole construction where out-degree
exceeds 1.

The front advances one site per step; the simulated head advances one site per
**three** steps.  So the front is never overtaken and never re-enters built
ground: every gate law is enacted exactly once and never amended again.  And
**blank tape needs no data at all** — an empty hardware block *is* a `0` with no
head, which is why the whole TM circuit is written in single-rail logic.

The per-cell circuit, three micro-steps per Turing step:

```
phase 0 (K0)  nT     cite(K0@0, ¬T@0)     -> {Tb}      Tb <- ¬t
              cpH_q  cite(H_q@0, ¬NIL)    -> {Ha_q}    transient head copy
              kK0    cite(K0@0, ¬NIL)     -> {K1}
phase 1 (K1)  r1_q   cite(Ha_q@0, ¬Tb@0)  -> {R_q1}    head in q reads 1
              r0_q   cite(Ha_q@0, ¬T@0)   -> {R_q0}    head in q reads 0
              kK1    cite(K1@0, ¬NIL)     -> {K2}
phase 2 (K2)  wr_qg  cite(R_qg@0, ¬NIL)   -> {T}       flip the tape bit
              mv_qg  cite(R_qg@−d, ¬NIL)  -> {H_q'}    the head arrives
              kK2    cite(K2@0, ¬NIL)     -> {K0}
always        holdT  cite(T@0, ¬NIL)      -> {T}       the tape remembers
```

`mv_qg` sits at the **destination** cell and cites the source across the
offset, so a right move is a gate citing at `−1` and a left move a gate citing
at `+1`.  `H_q`, `Ha_q`, `R_qg` are transients, so they are phase-tagged for
free and no explicit head-clearing gate is needed.

**Certificates** (both sectors, against an independently written TM simulator,
with a from-scratch decoder in the battery):

| machine | states | kinds (citation / anon) | Turing steps | verdict |
|---|---|---|---|---|
| move-right forever | 1 | 33 / 39 (L=11, window 18) | 24 / 20 | EXACT |
| move-left forever | 1 | 33 / 39 | 24 / 20 | EXACT |
| binary increment `1011` | 4 | 61 / 67 (L=23, window 42) | 20 / 18 | EXACT |
| busy beaver 3 | 4 | 62 / 68 | 18 / 16 | EXACT |
| busy beaver 4 | 5 | 74 / 80 (L=27, window 50) | 30 / 26 | EXACT |
| 120 random 3- and 4-state machines × random tapes (citation) | — | — | 14 | **0 mismatches** |
| 40 random 3-state machines × random tapes (anonymous) | — | — | 12 | **0 mismatches** |

Structural certificates:

* **front discipline** — 63 sites built, one per side per step, every block
  complete when it appears, none ever re-amended (40 steps).
* **scaffolding hygiene** — every `GAP` cell empty and every `POWER` cell
  intact at every step, 40 steps.
* **out-degree** — 1 everywhere outside the 18 front kinds.
* **anonymity** — `Const.cited == False`: no guard names a kind.
* **growth** — `|S_t|` grows by `+56.4` laws per step for a 1-state machine
  (two fronts × 28 laws), i.e. exactly linear.  Consistent with `CITATION.md`'s
  Y4.

The `move-right` machine runs its head 24 tape cells beyond the initial
hardware segment: the tape it uses did not exist in the initial code.  That is
the whole point.

**What this proves and what it does not.**  It proves that *the halting problem
for finite nomodynamic codes is undecidable*, and that for a fixed universal `M`
the constitution `N*(M)` is a fixed, finite, occupancy-guard constitution whose
finite codes simulate arbitrary computation.  It does **not** claim any
*minimality*: `N*(M)` has `≈ 11|Q| + 30` kinds and a window that grows with
`|Q|`, and no attempt was made to shrink either.

### 5.1 The front's out-degree is forced — **paving needs breadth**

`paving.py`.  The whole construction runs at out-degree 1 except the fronts.  Is
that an artefact of my design?  No.

> **LEMMA (backward paths).**  Let `C` have out-degree ≤ 1, so the target map
> `t : K → K` is a **function**.  A kind-`k` law can be enacted at cell `j`
> only by a kind-`k'` law at `j − c_{k'}` with `t(k') = k`.  So a kind-`k` law
> standing at distance `D` from the initial support forces a `t`-path
> `k_L → … → k_0 = k` with `L ≥ D / max|c|`.  In a finite functional graph any
> forward path longer than `n = |K|` has entered a cycle and can never leave
> it, so its **last** vertex lies on a cycle.

> **PROPOSITION 6.**  In an out-degree-≤1 constitution, every kind ever enacted
> at distance `> n·max|c|` from the initial support **lies on a cycle of the
> amendment digraph**, and its only target is the next kind of that cycle.
>
> **COROLLARY 6.1.**  A statute machine in normal form cannot grow its own
> hardware at out-degree 1.  A self-clearing wire is a 1-cycle (`t(w) = w`) and
> *can* be paved; but a gate `g` has `t(g) = w` with `w ≠ g` and `t(w) = w`, so
> the forward path from `g` is `g → w → w → …` and `g` never recurs.  `g` lies
> on no cycle, so **no out-degree-1 constitution can ever enact a gate law on
> virgin ground.**

*Certificate*: 400 random out-degree-1 constitutions (half with citation guards,
half anonymous) × random codes × 60 steps produced **45 094** sightings of a law
beyond `n·max|c|` of its initial support and **0** of them were of a kind off a
cycle.  Plus 300 random normal-form target maps: the cycle set is *exactly* the
wires, never a gate, 0 exceptions.

So the dividing line is **exact**, and it is the Out-Degree Law's own threshold
seen from a second side:

| | |
|---|---|
| **out-degree 1** | computes, on the hardware it is given — a linear bounded automaton (Theorem 4) |
| **out-degree ≥ 2** | can enact hardware on virgin ground, hence an **unbounded** tape (Theorem 5) |

> Chapter two: **breadth buys motion.**  Here: **breadth buys memory.**  They are
> the same threshold, and now there are two independent reasons for it.

---

## 6. Complexity

`circuit.py`.  Define

> **PREDICT** — given a constitution `C`, a finite code `S₀`, a step count `t`
> in unary, a cell `j` and a kind `k`: does a law of kind `k` stand at `j` at
> time `t`?

*Upper bound.*  One step costs `O(|S|·n)`, and `|S|` grows by at most `n` per
frontier cell, so `t` steps cost `poly(|C| + |S₀| + t)`.  **PREDICT ∈ P.**

*Lower bound.*  The **Circuit Value Problem** reduces to PREDICT in log space.
A constitution can hold **one wire kind per circuit wire and one gate kind per
circuit gate, with every law in a single cell** — kinds are the wires, so there
is no routing, no geometry, and every offset is `0`.  The transcription is a
direct syntactic copy of the circuit.

> **THEOREM 2.**  PREDICT is **P-complete** under log-space reductions, already
> for `dim = 1`, **window 0**, parity resolution, and codes supported on **one
> cell**.

*Certificates.*  120 random circuits (5 inputs, 22 gates, 9 gate types) × all 32
assignments = **3 840 evaluations, 0 mismatches**; and **COMPLETE: all 2^(2³) =
256 Boolean functions of three variables**, each compiled from its DNF and
checked on all 8 inputs, plus **all 16 functions of two variables** — 0
mismatches.  Compiled constitutions run 96–200 kinds at depth 1–13, and every
offset of every one of them is verified to be `0`.

For a **fixed** constitution the same conclusion follows from §5: the Generic
Machine Simulation Problem is P-complete, and `N*(U)` simulates a universal `U`
with dilation 3 and a log-space-computable code.

---

## 7. The obstruction: where the computation actually lives

`linear.py`.  §4 says citation is not the resource.  This section says what is.

Call a kind **unconditional** if its guard is vacuously true — cite yourself at
your own cell, and let the vacancy clause name a kind that is never enacted.
Every placed law then acts at every step, and the dynamics loses its only
nonlinearity.

> **THEOREM 3.**  If every kind of `C` is unconditional then `Φ` is
> **𝔽₂-linear**.  Writing a code as a vector of Laurent polynomials
> `x ∈ (𝔽₂[z,z⁻¹])ⁿ` with `x_k` the indicator series of the kind-`k` laws,
>
>     Φ(x) = L x ,    L = I + A ,    A[v][k] = [v ∈ T_k] · z^{c_k},
>
> so `Φᵗ = Lᵗ`, computable by `⌈log₂ t⌉` squarings of an `n × n` matrix of
> Laurent polynomials instead of `t` simulation steps.

*Certificate*: 400 random unconditional constitutions × random codes,
**0 deviations** from `Φ = L`; 60 trials of `Φᵗ = Lᵗ` by repeated squaring
against `t` engine steps, **0 deviations**.

> **COROLLARY 3.1 (Pascal, explained).**  For `n = 1`, `T = {k}`, offset `c`, a
> one-law seed gives `x(t) = (1+z^c)^t`, whose support has exactly
> `2^popcount(t)` cells by Lucas's theorem.  Chapter one's **Pascal columns**
> (`|S_t| = 2^popcount(t)`, `nomos2d/`) are the Frobenius endomorphism of
> `𝔽₂[z,z⁻¹]` and nothing else.
> *Certificate*: 2 710 checks (engine to `t < 200`, matrix powers to `t < 4096`),
> 0 deviations.

> **COROLLARY 3.2 (tameness).**  Iterated squaring of a polynomial matrix is an
> arithmetic circuit of depth `O(log² t)` and polynomial size, so PREDICT
> restricted to the unconditional sector lies in **NC**.  It is therefore **not
> P-complete unless NC = P** — in flat contrast with Theorem 2, and with
> Theorems 4 and 5, where the *same field with live guards* simulates every
> Turing machine.
> *(Honesty tier: the linear-algebra half is established and machine-verified;
> the NC membership is the standard circuit-complexity consequence, quoted, not
> re-proved here; the conditional non-universality is an interpretation of it.)*

Putting §4, §5 and §7 together:

| what the guard does | what the field is |
|---|---|
| vacuous guard (unconditional) | 𝔽₂-linear; `Φᵗ = Lᵗ`; PREDICT ∈ NC; Pascal/Lucas fauna |
| live guard, occupancy only | **universal** (Theorems 4, 5), at out-degree 1 |
| live guard, citation | universal, and *compact*: 24 kinds at window 1 |

> **All the computation in nomodynamics is in the exception clause.**  The
> amendment channel is linear algebra; what makes the field a computer is the
> word *"unless"*.

**What did NOT close (B8, as pre-registered).**  The single-author / own-kind
sector is 𝔽₂-linear **given occupancy**, but occupancy is `⋁_k x_k`, a function
of the very fields the linearity is supposed to describe.  So the linearity is
*conditional* and yields no unconditional poly-time algorithm and no
non-universality theorem.  I predicted at ≈ 0.7 that this would not close, and
it did not.  The obstruction that *did* close is a different one: unconditional
**guards**, not single **authorship**.

---

## 8. The ballistic sector — the gate table, and where it stops

Full data report: `BALLISTIC.md`; code `ballistic_*.py`.  1-D, chapter-two
semantics (`guards=None`).  **Every number here is a box statement** in the
sense of the width correction: a bounded sweep decides a box, never a question,
and none of these zeros is an impossibility claim.

**The laboratory is `MIRROR`** — `Const([(0,1,-1),(0,-1,1)], targets=[(0,1),(0,1)])`.
It is *palindromic* (`r₁ = −r₀`, both targets `{0,1}`), so `x ↦ −x` is an
automorphism of the constitution and **one universe carries gliders in both
directions**: `(p,d) = (4,±2), (5,±2), (12,±2)`, spans 53/20/39, parity only.
That is the one universe in which head-on ballistic gates can be posed at all.

### 8.1 The collision table

Outcomes certified with a **separation lemma** (`ballistic_collide.py`): all
offsets lie in `{−1,0,1}`, so if two isolated evolutions stay ≥ 3 cells apart
their union evolves as their disjoint union — proved and machine-checked, then
used to decide each run.

| box (complete) | runs | outcome |
|---|---|---|
| MIRROR glider × glider: 5 head-on + 3 rear-end pairings, all phases × gap 0..40 | **8 129** | **ARREST 8 129** |
| MIRROR glider × all 352 stationary codes in cells 0..4 | 29 205 | ABSORBED 29 163, UNRESOLVED 42 |
| MIRROR glider × 35 collision-debris walls, all phases × gap 0..24 | 4 375 | ABSORBED 4 368, UNRESOLVED 7 |
| TANDEM-1 glider × all 132 stationary codes in cells 0..4, both modes | 8 112 | ABSORBED 8 112 |
| GUN glider × all 416 balanced codes in cells 0..3, parity | 5 408 | ABSORBED 5 408 |
| **TRIPTYCH** glider × all 208 stationary codes in cells 0..2, parity | 2 943 | **EXPLOSION 2 943** |
| GUN glider × the immortal kind-2 source, gap 0..30 | 31 | UNRESOLVED 31 |
| **total** | **58 203** | |

Bucket totals over all 58 203 runs (arithmetic re-checked here):
`ARREST/ABSORBED 55 180 · EXPLOSION 2 943 · UNRESOLVED 80 · TRANSPARENCY 0 ·
ANNIHILATION 0 · REFLECTION 0 · FAN-OUT 0`.

Inside the 8 129-run glider×glider box every bucket but one is empty
(`TRANSPARENCY 0 · ANNIHILATION 0 · ARREST 8129 · REFLECTION 0 · ABSORPTION 0 ·
FAN-OUT 0 · EXPLOSION 0 · UNRESOLVED 0`), and the box is **uniform**: the only
variation is *which* debris — the `M2/5` head-on box yields exactly 8 distinct
debris signatures over its 1 025 cells, most of them **balanced constitutions**
(fixed codes with live, mutually cancelling laws).

**The zeros are meaningful because the detector has positive controls.**
`ballistic_selftest.py` builds a synthetic instance of *every* bucket —
TRANSPARENCY, FAN-OUT, ABSORPTION, REFLECTION, ANNIHILATION, ARREST, EXPLOSION —
and the classifier labels each one correctly; the suite reports **6/6** (five
bucket controls plus a 200-step check of the separation lemma).  So "0 fan-outs
in 58 203 runs" is a statement about the boxes, not about a blind instrument.

> **MIRROR is a perfectly inelastic medium.**  Two law-packets that touch always
> freeze.  That is the strongest possible DELETE and the worst possible wire.

Also established: **TANDEM-1 has no dead-letter wall at all**, at the level of
the constitution rather than the box — its guard makes a law at `i` active iff
`i−1` is empty, and the leftmost law of any finite code always has an empty cell
to its left, so every finite TANDEM-1 code has an active law.

### 8.2 The ballistic gate table

| gate | universe | status | note |
|---|---|---|---|
| **AND-NOT / DELETE** | MIRROR | **certified**, 4/4 | one gadget, **two ports**: right port `= A ∧ ¬B`, left port `= B ∧ ¬A` |
| **AND-NOT cascade** | MIRROR | **certified**, 8/8 | `out = A ∧ ¬B ∧ ¬C` — the output is a real glider that drives the next stage |
| **NOT** | MIRROR | **certified**, 2/2 | plant `B` as a constant 1; **flips polarity** (right input → left output) |
| **XOR** | MIRROR | **certified**, 4/4, *weaker* | readout is "how many free gliders exist anywhere", not a single spatial port |
| **WALL-DELETE** | TANDEM-1 | **certified**, 4/4 | static control, **one-shot**, does not cascade |
| **REFLECT** | — | **not found**, 0 / 58 203 | left-movers exist; nothing turns a right-mover into one in the box |
| **FAN-OUT** | — | **not found**, 0 / 58 203 | |
| **AND, OR** | — | **not found**, mechanism identified | see below |
| **glider gun** | — | **not found**, 0 in a complete 5 832-universe × 192-seed box at `n = 2` | so there is no stream source for a two-stream gate |

Paste-ready AND-NOT (MIRROR, parity, `T = 200`; right port `= cells [60,400]`
read by `verify_glider(·,MIR,5,2)`, left port `= [−400,−5]` at `(5,−2)`):

```python
MIR = Const([(0,1,-1),(0,-1,1)], targets=[(0,1),(0,1)])
A = {c:3 for c in [ 0, 1, 2, 4, 5, 6, 7, 8,10,11,12,14,16,17,18,19]}  # right wire
B = {c:3 for c in [40,41,42,43,45,47,48,49,51,52,53,54,55,57,58,59]}  # left  wire
#  A B  |  state at T=200                          | RIGHT | LEFT
#  0 0  |  empty                                   |   0   |  0
#  0 1  |  cells -40..-21, card 32                 |   0   |  1
#  1 0  |  cells  80.. 99, card 32                 |   1   |  0
#  1 1  |  cells  16.. 43, card 24, BALANCED       |   0   |  0
```

### 8.3 Why it stops there, and why it does not matter

The two-stage `AND` (`¬A` by the NOT gate, then `B ∧ ¬(¬A)`) was run on all four
inputs and **fails at `A = B = 1`**.  The mechanism is machine-visible: when
`A = 1`, stage one leaves **balanced debris standing in `B`'s lane**, and every
one of the 4 375 glider-vs-debris runs is ABSORBED.  On ℤ there is no second
lane to route `B` around the debris and no certified transparent obstacle, so
`B` dies.  For the same reason the gates are **one-shot**: firing an AND-NOT
leaves a permanent wall on the wire (verified — a second shot into a used gate
is eaten).

**And the other extreme is gateless too.**  `TRIPTYCH` is MIRROR's opposite:
**every one of its 2 943 glider-vs-wall collisions EXPLODES**, growing past the
budget.  MIRROR freezes everything it touches; TRIPTYCH detonates everything it
touches; neither leaves a certified outcome you can read a bit off.  The two
1-D media the field has are at opposite ends of the same missing property —
*controlled, repeatable, non-destructive interaction* — and both fail it.

> `[original proposal]` **The 1-D ballistic obstruction.**  In an inelastic 1-D
> medium — every collision arrests, none is transparent, none fans out — the
> gate set reachable by ballistic collision is exactly the *monotone-decreasing*
> one: AND-NOT and its cascades, NOT across polarity, XOR only under a non-local
> readout.  AND, OR and fan-out each require a transparent crossing or a second
> lane, and ℤ has neither.  The detonating medium is no better: an outcome that
> exceeds every budget carries no readable bit.

And this is exactly why §§1–5 are in a different sector.  **Fan-out is free in
the statute machine and absent in the ballistic one**, because a guard is
read-only and a collision is not; and the statute machine needs no motion at
all, so it is untouched by *every* no-go theorem the field has proved — the
Out-Degree Law, the Anchor Theorem, Path-Sum Confinement, the Tropical Speed
Law, the Zero-Sum No-Go.  They are all theorems about **transport**.

**Corrections found by this sub-expedition** (kept as found): the TRIPTYCH seed
is nine laws (all three kinds at each of cells 1, 2, 4), not three — the
one-kind-per-cell reading gives a period-2 *cycle*, not a glider; and the 1-D
gun's law `|S_t| = 2⌊t/2⌋+3` holds for `t ≥ 1` only, since `|S_0| = 1`.

---

## 9. Scorecard

### Against this expedition's own pre-registration

| | verdict |
|---|---|
| **B1** gates cheap at window 1 | **HELD** — 11-row table, one law for AND-NOT/NOT/BUF, free fan-out |
| **B2** assignment is the hard primitive; self-clearing kind fixes it | **HELD** — it is the whole construction |
| **B3** full synchronous circuit at window 1, fixed finite constitution | **HELD** — Theorem 1 + the 24-kind Rule-110 constitution; the *arbitrary*-circuit compiler uses window 0 with a circuit-dependent constitution |
| **B4** Rule 110 falls with small dilation | **HELD** — dilation 3, and in **both** sectors |
| **B5** finite-code gap probably will not close (≈ 0.35) | **REFUTED, in my favour** — it closed, in both sectors, via the building front |
| **B6** P-completeness | **HELD** — Theorem 2, with a complete 256-function certificate |
| **B7** ballistic: reflector *and* deleter yes, fan-out no | **SPLIT — 2 of 3, and the reasoning was wrong.**  DELETE (AND-NOT, cascading) **certified**; fan-out **absent**, 0 in 58 203 runs; but **REFLECT is also absent**, 0 in 58 203 — that half is refuted.  And the *mechanism* I named was wrong: I predicted transparency would spoil interaction, and in 1-D MIRROR there is **no transparency at all** — every collision arrests.  The right diagnosis is the opposite one, *perfect inelasticity*, and it kills fan-out for a reason I did not anticipate. |
| **B8** single-author linearity obstruction will not close (≈ 0.7) | **HELD** — it did not close; a *different* linearity theorem did |
| **B9** no replicator, no new glider, ballistic not universal | **HELD with one qualification.**  No replicator was sought or found; the ballistic sector did not reach universality.  But the sub-expedition did certify specimens the repository did not have: the **mirror-image left-moving** TANDEM-1-L, SOLO-L, TRIPTYCH-L and MIRROR-L, and — the useful one — that **MIRROR is palindromic**, so a *single* universe carries gliders of both signs at three speeds.  That is a new fact about a known universe, not a new universe. |

### Against `CITATION.md` (chapter three's frozen charter)

| | verdict |
|---|---|
| **Y1** the plenum still freezes | **HELD** — 200 random constitutions, a saturated region has 0 active laws |
| **Y3** citation is *the* computational substrate; the first universality construction lives there | **REFUTED.**  Universality is already in the anonymous sector, at out-degree 1.  What citation buys is compactness — 24 kinds/window 1 versus 31 kinds/window 20 — not power.  *(The second half of Y3, "a gate-level inventory with working AND, NOT and fan-out", HELD.)* |
| **Y4** growth stays linear | **HELD** — `|S_t|` grows by a constant per step in every construction here |
| **Y5** a replicator exists | not addressed |

### Against `XNOMOS.md`

| | verdict |
|---|---|
| **X8** no universality this cycle (≈ 90 %) | **REFUTED** |

---

## 10. Verdict — exactly what is and is not proved

**Proved, with machine certificates and a composition argument.**

1. **Theorem 1** (statute-circuit normal form): a constitution of the stated
   shape *is* a synchronous AND-NOT network with free XOR fan-in, free fan-out
   and unit delay.  Two-line proof; 2 000-instance fuzz certificate.
2. **The gate table** of §2, in both the citation and the anonymous sector,
   exhaustively certified (all inputs, output stable for 6 further steps),
   re-derived independently in `verify_y.py`.
3. **Theorem 2**: PREDICT is **P-complete** under log-space reductions, at
   `dim = 1`, window 0, one cell.  Complete certificate over all 256 Boolean
   functions of three variables.
4. **Rule 110 simulates exactly** in a 24-kind window-1 citation constitution
   and in a 31-kind out-degree-1 **anonymous** one, dilation 3, space dilation 1
   / 13.  The certificate is a **complete enumeration of the local map's
   inputs** (all 2⁷ configurations of the 7-site ring), with the locality lemma
   itself machine-checked off the raw `Const`.
5. **Theorem 5**: **every Turing machine compiles into a finite code** of the
   founding occupancy-guard sector, with unbounded tape supplied by a
   self-extending front; out-degree 1 everywhere except the 18 front kinds.
   Hence nomodynamics is **computation-universal**, and halting for finite codes
   is **undecidable**.
6. **Theorem 3**: the unconditional sector is 𝔽₂-linear, `Φᵗ = Lᵗ`, with
   Pascal/Lucas as a corollary; PREDICT there is in NC and so is not P-complete
   unless NC = P.
7. **Proposition 6 / Corollary 6.1**: at out-degree ≤ 1 only kinds on a cycle
   of the amendment digraph can be enacted far from the initial support; hence a
   normal-form statute machine **cannot pave its own hardware** at out-degree 1,
   and the front's breadth is necessary, not a design accident.

**Not proved, and not claimed.**

* **No minimality.**  24 kinds and 31 kinds are what these constructions
  happened to need.  Nothing here rules out a universal constitution with 5
  kinds, or with window 1 in the anonymous sector.
* **Nothing about the strict own-kind sector.**  Every construction here uses
  *cross*-amendment (a gate targets a wire kind other than its own), even where
  out-degree is 1.  Whether **chapter one** — own-kind, `T_k = {k}` — is
  universal is **open**; see §11.
* **Nothing about the ballistic sector's universality.**  §8 argues it is the
  wrong tool; the 1-D ballistic obstruction is an *original proposal*, not a
  theorem.  And every zero in §8 — no reflector, no fan-out, no gun, no
  transparency — is a **box statement**: `[no X in the stated box]`, never
  `[X is impossible]`.  The width correction applies in full: MIRROR's own
  gliders span 20–616 cells and were invisible to every earlier census in this
  program.
* **Rule 110's own universality is quoted, not re-proved**, and its standard
  form concerns ultimately-periodic backgrounds.  The finite-code claim rests
  on Theorem 5, which does not depend on Rule 110 at all.
* **The NC membership in Corollary 3.2 is quoted** from standard circuit
  complexity, not proved here; only the linear algebra it rests on is
  machine-verified.

---

## 11. The sharpest open questions

1. **Is out-degree 1 enough for an unbounded machine *outside* normal form?**
   Proposition 6 settles this for statute machines: at out-degree 1 only kinds
   on a *cycle* of the amendment digraph can be paved, and a normal-form gate
   lies on no cycle, so it can never be enacted on virgin ground.  What remains
   open is whether some **non-normal-form** design evades it — a machine built
   entirely out of cycle-kinds, where each computing kind's single target is
   forced to be the next kind of its own cycle.  Chapter one's colonizers are
   exactly such cycle-kinds and they *do* pave, so the question is whether a
   cycle can carry logic as well as pavement.  A negative answer would upgrade
   Proposition 6 into a genuine **space-hierarchy theorem stated in the field's
   own vocabulary**: narrow law can compute, but only in a bounded chamber.

2. **Is chapter one universal?**  In the own-kind sector the only author of kind
   `k` at cell `j` is the kind-`k` law at `j − c_k`, so the system is `n`
   one-directional *toggle-conveyors* coupled solely through the shared
   occupancy field: `x_k(j,t+1) = x_k(j,t) ⊕ [x_k(j−c_k,t) ∧ occ(j−c_k+a_k,t) ∧
   ¬occ(j−c_k+b_k,t)]`.  The self-clearing wire survives (`c_k = 0` gives a kind
   that repeals itself), but *writing* a cell requires a wave arriving from a
   fixed direction, and no gadget here does that.  Universality of the founding
   own-kind object is open in both directions.

3. **How small can a universal constitution be?**  Nothing is known below 24
   kinds.  A natural target: is there a **two-kind** universal constitution at
   some window, or a window-1 universal anonymous one?

---

## 12. Files and repro list

```
computation/
  statute.py    Theorem 1, the normal form, the citation gate table   python3 statute.py
  rule110.py    Rule 110 in 24 kinds at window 1, complete certificate python3 rule110.py
  turing.py     every TM as a finite citation code; building front     python3 turing.py
  anon.py       the ANONYMOUS statute machine; Rule 110 with           python3 anon.py
                guards=None at out-degree 1; site-locality audit
  anontm.py     every TM as a finite code of the FOUNDING sector       python3 anontm.py
  circuit.py    arbitrary circuits; CVP reduction; P-completeness      python3 circuit.py
  linear.py     the unconditional sector is F2-linear; Pascal/Lucas    python3 linear.py
  paving.py     Proposition 6: out-degree 1 cannot pave its own gates    python3 paving.py
  verify_y.py   the battery: everything re-derived independently       python3 verify_y.py
                                    ... and the paste-ready dump       python3 verify_y.py -d

  BALLISTIC.md          the glider-collision data report
  ballistic_lib.py      shared helpers
  ballistic_collide.py  the separation lemma + outcome classifier
  ballistic_t0_verify.py     specimen re-certification (and two corrections)
  ballistic_t1_leftmovers.py mirror-image constitutions
  ballistic_t1b_species.py   complete per-universe glider censuses
  ballistic_t1c_bigsweep.py  the complete 5832-universe n=2 sweep
  ballistic_t2_mirror.py     head-on MIRROR collisions
  ballistic_t2_family.py     the full 8129-run collision table
  ballistic_t3_gates.py      AND-NOT, NOT, XOR, reusability
  ballistic_t3_cascade.py    A & ~B & ~C
  ballistic_t3_logic.py      the AND/OR failure, with its mechanism
  ballistic_t4_walls.py      complete wall censuses and glider-vs-wall boxes
  ballistic_selftest.py      positive controls: one synthetic instance of each
                             outcome bucket, all 6 classified correctly
```

Approximate runtimes: `statute.py` 1 s, `linear.py` and `paving.py` < 1 s,
`anontm.py` 3 s, `turing.py` 10 s, `circuit.py` 11 s, `anon.py` 19 s,
`rule110.py` ~2 min (the exhaustive `ℤ/12` sweep), `verify_y.py` ~1 min.

Python 3.11, no dependencies beyond the standard library and the repository's
`xnomos.py`.  Total runtime of the battery: a few seconds.  `verify_y.py`
rebuilds every headline constitution from raw `(a,b,c)` / target / guard tuples
without importing the builders, re-implements the reference semantics from the
definitions, and uses a bit-parallel Rule 110 written independently of the
table-driven one.

**21/21 battery checks pass.**
