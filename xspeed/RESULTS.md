# The Displacement-Quantisation Law

### Expedition X-E, NOMODYNAMICS program · 2026-08-26

*Charter: settle why the number of kinds appears to cap the displacement per
period of a free glider — X-A's sharpest open question.*

---

## 1. Verdict up front

**The premise is false, and the reason it looked true is worth more than the
law it replaced.**

X-A measured, over complete SAT decisions at `W = 1`:

| kinds | X-A's finding |
|---|---|
| n = 2 | realises only `|d| = 1` (speed 1 only) |
| n = 3 | realises exactly `|d| ≤ 2` |
| n ≥ 4 | realises every coprime `(p,d)` tested |

The `n = 2` row is **refuted by certified counterexample**. The universe

```
MIRROR   n = 2, W = 1     rules  A = (a,b,c) = (0, −1, +1)      T_A = T_B = {A,B}
                                 B = (a,b,c) = (0, +1, −1)
```

— *"a left-edge law pushes right; a right-edge law pushes left"* — carries free
gliders of **minimal period 4, 5, 6, 7 and 12, each with displacement exactly
2** (speeds 1/2, 2/5, 1/3, 2/7, 1/6). They were invisible to every census in
the program's history for two independent reasons, and both reasons are
general:

1. **They are enormous.** The `p = 5` specimen spans 20 cells, the `p = 4`
   specimen **53 cells**, the `p = 7` specimen **438 cells**, the `p = 6`
   specimen **616 cells**. Every census in the program — X-A's `N = 16`, X-D's
   span-3 seeds, X-E's own first map — fixed a box no wider than ~26 interior
   cells. A box-fixed "UNSAT" is a statement about *narrow* gliders, and the
   objects that carry the interesting speeds are not narrow.
2. **Three of the five have minimal period not coprime to their displacement.**
   `Φ⁴ = σ²` holds while `Φ² = σ¹` fails; `Φ⁶ = σ²` holds while `Φ³ = σ¹`
   fails. A sweep that enumerates only coprime `(p,d)` — as X-A's speed
   spectrum and X-E's first map both did — cannot see them at all.

With those two confounds removed, the surviving law is **not about the number
of kinds**. It is this:

> **The Single-Field Cap `[measured, width-unbounded]`.** Call a constitution
> *single-field* when every law amends every kind (`T_k = K` for all `k`);
> by X-A's Twin-Kind Lemma all kind-supports then coincide and the system is a
> one-bit cellular automaton with `n` independent **channels** `(a_k,b_k,c_k)`.
> At `W = 1`, in the single-field sector, every free glider has
>
> **|d| ≤ 2 under parity, |d| ≤ 1 under OR at two channels** — *for any number
> of channels*, **at any width**, where `d` is the displacement per **minimal**
> period.
>
> Decided exactly, with no bound on the pattern width, over all 171 / 1,140 /
> 5,985 / 26,334 constitutions at `n = 2, 3, 4, 5` channels: complete for
> `p ≤ 5` (`n = 2, 3`), `p ≤ 4` (`n = 4`), and for the critical case
> `(p,d) = (4,3)` at `n = 5` — **`NONE`, 26,334 constitutions, 0 undecided.**

and the resource that buys `|d| ≥ 3` is **not another kind — it is another
𝔽₂ kind-field**:

> **The Field-Count Threshold `[measured]`.** At `W = 1`, `|d| = 3` requires at
> least **four kinds carrying at least two independent kind-fields**.
> * four kinds, **one** field: `(p,d) = (4,3)` is impossible **at any width**
>   (both resolutions) — the SFT decider and the SAT instrument agree;
> * four kinds, **two** fields: `(4,3)` exists in a 3-cell seed
>   (X-A's specimen, re-verified here);
> * three kinds, any field structure: `|d| ≥ 3` is UNSAT to interior 26 for
>   *every* constitution and every seed, `p ≤ 8`.

Three further things fell out, each independently useful:

* **Theorem K (the Even-Support Law)** — a strict generalisation of X-A's
  Twin-Kind Lemma, proved and fuzz-tested: the kind-fields of *any* orbit are
  constrained by the 𝔽₂ left-kernel of the amendment incidence matrix, whose
  determinant is the parity of the number of cycle covers of the amendment
  digraph.
* **The Dilation Theorem** — proved: dilating space by `r` maps a
  `(W, p, d)` glider to an `(rW, p, rd)` glider. Hence **no `W`-independent
  cap on `|d|` can be true**, which kills the whole `f(n)` family of
  hypotheses before a single solver call.
* **The decisive `W = 2` test** (the coordinator's discriminator): at `n = 3`
  the cap moves from `2` at `W = 1` to **at least 5** at `W = 2` — a certified
  `p = 3, d = 5` glider, `5 > 2W = 4`. So the law is **neither** "about the
  number of kinds" **nor** "about `n·W`".

---

## 2. Pre-registration

Written before the campaign and kept verbatim in
[`PREREG.md`](PREREG.md). Scorecard in §9.

Two facts were in hand when it was written and are labelled there as such: the
Dilation Theorem (proved on paper, killing every `W`-independent cap), and one
smoke-test call showing `n=3, W=2, p=3, d=5` SAT (killing `|d| ≤ g(n)·W`).

---

## 3. The two confounds, in detail

### 3.1 The width confound

`xsat.py` decides a **box**: "no glider of period `p` and displacement `d`,
over any constitution in the class, **whose `t = 0..p` trajectory spans at most
`N − 2W` cells**." That qualifier is load-bearing, and the program had been
reading past it.

The first crack: X-E re-ran X-A's `n = 2, W = 1` no-goes at larger boxes.

```
n=2 W=1 p=5 d=2  interior 14 UNSAT   18 UNSAT   22 UNSAT   26 *** SAT ***
```

The witness, certified by `xnomos.verify_glider` over 3 full periods in
`parity` (and correctly rejected under `or`):

```
MIRROR-2/5     n = 2, W = 1, parity      p = 5   d = +2   speed 2/5
rules   [(0, 1, −1), (0, −1, 1)]      T = [{0,1}, {0,1}]
seed    16 laws, one per cell of {2,3,4, 6,7,8,9,10, 12,13,14, 16, 18,19,20,21}
        (every cell carries BOTH kinds)

t=0   ..###.#####.###.#.####...
t=1   ..###.#.#.#.#######..#...
t=2   ..#####.#.###.###.#.###..
t=3   ..#.#.#######.#########..
t=4   .##.###.###.#.#.#####.#..
t=5   ....###.#####.###.#.####.        = t=0 shifted by +2
```

Then the width-unbounded decider (§5) found three more gliders in the *same*
universe, far beyond any box a SAT solver will reach, and the width ladder
found a fifth:

| specimen | p | d | reduced speed | span | resolution | found by |
|---|---|---|---|---|---|---|
| MIRROR-1/2 | 4 | 2 | 1/2 | **53 cells** | parity only | `sft.py` |
| MIRROR-2/5 | 5 | 2 | 2/5 | 20 cells | parity only | `xsat` @ interior 26 |
| MIRROR-1/3 | 6 | 2 | 1/3 | **616 cells** | parity only | `sft.py` |
| MIRROR-2/7 | 7 | 2 | 2/7 | **438 cells** | parity only | `sft.py` |
| MIRROR-1/6 | 12 | 2 | 1/6 | 39 cells | parity only | `xsat` @ interior 44 |

All five verified by `xnomos.verify_glider`, and the 4/5/6/12 cases
independently reported `GLIDER, period p, displacement 2` by
`xnomos.classify` — so each minimal period is confirmed, not inferred.
All five have displacement exactly **2**: `Φ⁴ = σ²` while `Φ² ≠ σ¹`,
`Φ⁶ = σ²` while `Φ³ ≠ σ¹`, `Φ¹² = σ²` while `Φ⁶ ≠ σ¹`.

Meanwhile `d = 1` and `d = 3` are **`NONE` at any width** in this universe for
every `p ≤ 7`, in both resolutions.

> **One constitution, five gliders, five minimal periods, one displacement.**
> This is what the "cap" really looks like from the inside: `MIRROR` will run
> at 1/2, 2/5, 1/3, 2/7 and 1/6 and it will not run at any speed whose
> displacement per minimal period is 1 or ≥ 3.
>
> **Conjecture M `[original proposal]`.** `MIRROR` has a free glider with
> `Φᵖ = σ²` for **every** `p ≥ 4` (parity), and none with `d ≠ 2`. Decided for
> `4 ≤ p ≤ 7` and `p = 12`; the spans (53, 20, 616, 438, 39) show no
> monotonicity, which is itself worth explaining.

> **Consequence for the whole program.** Every "UNSAT ⇒ impossible" reading in
> `xamend1d/RESULTS.md` §4.6, and every speed-set claim from a fixed-box
> census (including X-D's sunset speed set), is a statement about gliders
> narrower than the box. X-E recommends that all such claims be re-labelled.

### 3.2 The coprimality confound

`Φᵖ(S) = σᵈ(S)` with `gcd(p,d) = g > 1` does **not** imply
`Φ^{p/g}(S) = σ^{d/g}(S)`. The coordinator's `(6,3)` example makes the point;
MIRROR makes it twice more, with `g = 2`. A sweep restricted to coprime `(p,d)`
therefore misses an entire class of objects — and it misses them exactly where
the interesting slow speeds live.

X-E's final tables enumerate **every** `(p,d)` with `1 ≤ d ≤ pW`, and report
the reduced speed `d'/p'` separately from the displacement-per-minimal-period
`d`. These are different quantities and the cap is on the second one.

---

## 4. What is actually quantised

Three candidate quantities were on the table. The data separates them.

| quantity | is it capped? |
|---|---|
| reduced-speed numerator `d'` | capped in the single-field sector, but only because `d' ≤ d` |
| **displacement per minimal period `d`** | **yes — this is the quantised one** |
| speed `d/p` | no (Theorem 1's bound `d/p ≤ λ_max` is the only constraint, and it is loose) |

At `W = 1` in the single-field sector, the realisable minimal-period objects
are exactly (parity):

```
n = 2 channels :  (1,1)  (4,2)  (5,2)  (6,2)                    -> |d| in {1,2}
n = 3 channels :  (1,1)  (2,1)  (4,2)  (5,2)                    -> |d| in {1,2}
n = 4 channels :  (1,1)  (2,1)  (3,1)  (3,2)  (4,1)  (4,2)      -> |d| in {1,2}
```

`(2,2), (3,3), (4,4), (5,5)` also solve `Φᵖ = σᵈ` but are iterates of the
period-1 TANDEM glider, not minimal-period objects.

`|d| = 3` never appears — not at 2, 3, 4 or 5 channels, and **not at any
width**. Meanwhile at four kinds with *two* fields it appears immediately, in a
3-cell seed.

### 4.1 The resolution axis decides the cap

A **fourth** independent parity/OR split, and this time it is the cap itself:

| sector (`W = 1`, width-unbounded) | parity | OR |
|---|---|---|
| single field, 2 channels | `|d| ≤ 2` (MIRROR family) | **`|d| ≤ 1`** |
| single field, 3 channels | `|d| ≤ 2` | `|d| ≤ 2` |
| single field, 4 channels | `|d| ≤ 2` | `|d| ≤ 2` |

At two channels the entire `|d| = 2` family is parity-only: under OR the
MIRROR toggles no longer cancel, and every one of `(4,2), (5,2), (6,2)` is
`NONE` at any width. This joins TRIPTYCH, X-A's `p = 9` 3-law glider and the
coordinator's `(6,3)` as evidence that the resolution convention is a physical
axis, not a bookkeeping choice.

### 4.2 The window lifts the cap faster than linearly

The coordinator's discriminating test, run properly:

| | `W = 1` | `W = 2` | `W = 3` |
|---|---|---|---|
| max `|d|` seen at `n = 3` | **2** | **≥ 5** | **≥ 14** |
| relevant certificate | complete SAT to interior 26 | `p=3, d=5` certified | `p=5, d=14` certified |

`5 > 2W = 4`, so the cap is not `(n−1)·W`; and `d = 5` at `n = 3, W = 2` is
carried by a **single-field** constitution, so it is not a field-count effect
either. The `W = 2` specimen:

```
TRIAD          n = 3, W = 2, single field.  ONE cell carrying all three kinds.
rules   [(1, −1, 0), (0, −2, 1), (0, −2, 2)]     T = [{0,1,2}]×3
seed    {cell 0 : kinds 0,1,2}

  parity                          or
  t=0  .#.........               t=0  .#.........
  t=1  .###.......               t=1  .###.......
  t=2  ...##......               t=2  ....#......      = t=0 shifted by +3
  t=3  ......#....  = +5         t=3  ....###....
  t=4  ......###..               t=4  .......#...      = t=2 shifted by +3
```

**The same seed in the same universe is a `p = 3, d = 5` glider under parity
and a `p = 2, d = 3` glider under OR** — different period *and* different
displacement, from one cell. Both certified by `xnomos.verify_glider`; the
parity/OR verdicts each fail for the other's `(p,d)`. This is the cleanest
parity/OR split in the program: not "moves vs. doesn't", but *moves at a
different speed*.

So `W` and the field count are two *separate* resources that both buy
displacement, and the number of kinds by itself buys nothing in the
single-field sector.

---

## 5. The instrument: width-unbounded decisions

`sft.py`. The single-field reduction makes the state one bit per cell, so the
space-time diagrams of `(p,d)`-gliders form a **subshift of finite type** whose
letters are the *columns* `v_x = (c_0(x), …, c_{p−1}(x)) ∈ {0,1}^p`, with
`c_p(x) := c_0(x−d)` supplied by the glider condition itself. A channel at
`i = j − c_k` reads `i + a_k` and `i + b_k`, so the CA has radius `r = 2W` and
every constraint centred on column `y` is decidable from columns `y−r … y+r`
plus the row-0 bit of column `y−d`. Scanning left to right, the transition
system has state

```
   (the last 2r columns in full)  +  (row-0 bits of the max(0, d−r) columns before them)
```

and

> **a glider with `Φᵖ = σᵈ` exists ⟺ the quiescent state lies on a cycle of the
> reachable transition graph carrying at least one non-zero column** —
> **with no bound whatsoever on the width of the pattern.**

BFS from the quiescent state settles it. A `GLIDER` verdict returns the witness
columns, which are handed to `xnomos.verify_glider`; a `NONE` verdict is a
complete no-go over ℤ. `CAP` means the reachable set exceeded the state budget
and nothing is claimed (**zero `CAP` verdicts occurred in any run reported
here**).

**Cross-validation against the SAT instrument** (independent code paths):

| question | `xsat` (boxed) | `sft` (unbounded) | agree |
|---|---|---|---|
| n=4 W=1 full-T p=4 d=3 parity | UNSAT (interior 24) | NONE | ✓ |
| n=4 W=1 full-T p=4 d=3 or | UNSAT (interior 24) | NONE | ✓ |
| n=3 W=1 full-T p=5 d=2 parity | SAT | GLIDER | ✓ |
| n=3 W=1 full-T p=4 d=3 parity | UNSAT (interior 24) | NONE | ✓ |
| n=2 W=1 full-T p=3 d=2 parity | UNSAT (interior 24) | NONE | ✓ |
| n=2 W=2 full-T p=2 d=3 parity | UNSAT (interior 22) | NONE | ✓ |
| n=2 W=1 full-T p=4 d=2 parity | UNSAT (interior 28) | **GLIDER** | ✓* |

*The last row is the instrument earning its keep: the witness has span **53**,
so the boxed UNSAT and the unbounded GLIDER are both correct and the boxed
result is simply not the question. The SFT witness passes
`xnomos.verify_glider`.

Self-tests in `sft.py` reproduce MIRROR-2/5 and TANDEM-1 from scratch, and the
`d > r` code path is validated on the certified `W = 2, p = 3, d = 5`
specimen.

---

## 6. Theorems proved here

### 6.1 Theorem D (Dilation) `[proved]`

> Let `C` be a constitution with window `W` and let `S` be a free glider with
> `Φᵖ(S) = σᵈ(S)`. For every integer `r ≥ 1`, the dilated constitution
> `C^{(r)}` — same target sets, offsets `(a,b,c) ↦ (ra, rb, rc)`, window `rW` —
> has the dilated code `S^{(r)} = { (r·i, k) : (i,k) ∈ S }` as a free glider
> with `Φᵖ(S^{(r)}) = σ^{rd}(S^{(r)})`.

*Proof.* `S^{(r)}` occupies only cells `≡ 0 (mod r)`. A law of `S^{(r)}` at
`ri` reads occupancy at `ri + ra` and `ri + rb`, both `≡ 0 (mod r)`, where the
occupancy of `S^{(r)}` equals that of `S` at `i + a`, `i + b`; so a law is
active in `S^{(r)}` iff its preimage is active in `S`. Each active law emits at
`ri + rc ≡ 0 (mod r)`, the image of `i + c`. Toggle multiplicities at
corresponding slots therefore agree, and both resolutions are functions of the
multiplicity, so `Φ(S^{(r)}) = (Φ(S))^{(r)}`. Induct, and dilate the
translation. ∎

**Corollary D1.** `maxdisp(n, rW) ≥ r · maxdisp(n, W)`. No cap on `|d|`
independent of `W` can hold. *(This is why the question had to be re-asked as a
joint `(n, W)` question, and it was settled before the campaign began.)*

**Corollary D2 `[certified]`.** Dilating MIRROR-2/5 gives certified gliders
`(p,d) = (5,4)` at `n = 2, W = 2` and `(5,6)` at `n = 2, W = 3` — both
verified by `xnomos.verify_glider`, both far outside every box tested. So the
`n = 2` row of the frontier table is `|d| ≥ 2W`, not `|d| ≤ 2`.

### 6.2 Theorem K (the Even-Support Law) `[proved]`

Let `A ∈ 𝔽₂^{n×n}` be the **amendment incidence matrix**, `A[m][k] = 1` iff
`m ∈ T_k`, and let `X_m(t) ∈ 𝔽₂[σ^{±1}]` be the generating function of
`supp_m(t)`.

> **Theorem K (parity resolution).** Let `U ⊆ K` satisfy `|T_k ∩ U|` even for
> every kind `k` — equivalently `1_U` lies in the left kernel of `A` over `𝔽₂`.
> Then `Y_U(t) = Δ_{m∈U} supp_m(t)` is a **constant of the motion** along every
> orbit, and in a free glider `Y_U ≡ ∅`: at every time, every cell carries an
> **even** number of kinds of `U`.

*Proof.* Per step `X_m(t+1) = X_m(t) + Σ_{k : m ∈ T_k} σ^{c_k} A_k(t)`, where
`A_k(t)` is the generating function of the active kind-`k` laws. Summing over
`m ∈ U` in `𝔽₂`, the coefficient of `σ^{c_k}A_k(t)` is `|T_k ∩ U| mod 2 = 0`,
so `Y_U(t+1) = Y_U(t)`. For a glider `Y_U(t+p) = σ^d Y_U(t)`, and a finite set
equal to its own translate by `d ≠ 0` is empty. ∎

> **Theorem K′ (the determinant).** Writing `M[m][k] = σ^{c_k}[m ∈ T_k]`, we
> have `M = A·diag(σ^{c_k})`, hence `det M = (det A)·σ^{Σ_k c_k}` and
> `det A = #{permutations π of K with π(m) → m for all m} mod 2` — the parity
> of the number of **cycle covers** of the amendment digraph. The left kernel
> of `M` is non-trivial exactly when that parity is `0`, and the offsets are
> irrelevant to it.

**Strictly stronger than X-A's Lemma T.** Lemma T is the case `|U| = 2`
(`|T_k ∩ {m,m′}|` even for all `k` ⟺ `m` and `m′` have identical author sets).
`|U| = 3` cases exist with no two kinds twinned, e.g.

```
T = [{0,1}, {1,2}, {0,2}]   :  |T_k ∩ {0,1,2}| = 2 for every k
```

whose author sets `{0,2}, {0,1}, {1,2}` are pairwise distinct. Every glider in
that universe has an **even number of kinds at every cell** — a conservation
law Lemma T cannot see.

**Fuzz certificate** (`thmK.py`, 3,000 random universes, `n ∈ 2..5`,
`W ∈ 1..3`, 12 steps each):

| check | count | violations |
|---|---|---|
| `Y_U` constant along the orbit (Theorem K) | 27,876 | **0** |
| of which `|U| ≥ 3` with all author sets distinct (beyond Lemma T) | 239 universes | **0** |
| `det A` over `𝔽₂` = parity of cycle covers (Theorem K′) | 3,000 | **0** |
| Lemma FR (rear repeals need `c_k ≤ 0`) | 2,598 | **0** |

### 6.3 Lemma FR (front/rear channel dichotomy) `[proved]`

> For any resolution satisfying X-A's (R0)/(R1), and any code:
> (i) `β(t+1) ≤ β(t) + max_k c_k`, so `d ≤ p·max(0, max_k c_k)`;
> (ii) if a law at the **rearmost** occupied cell `α(t)` is repealed at step
> `t`, its repealing author `k` has `c_k ≤ 0`.

*Proof.* (i) A slot at `j` is toggled only by an active law at `j − c_k`, which
sits on an occupied cell, so `j − c_k ≤ β(t)`. (ii) Same, with
`j = α(t) ≤ j − c_k`. ∎

**Corollary.** A free glider with `d > 0` needs at least one kind with
`c_k > 0` *in play* (to advance the front) and at least one with `c_k ≤ 0` (to
clear the rear). This is the elementary shadow of X-A's Theorem 2, and unlike
Theorem 2 it names the mechanism.

### 6.4 What X-D's Path-Sum Confinement gives here `[interpretation]`

X-D's Corollary 4.4 — *a glider's velocity is a positive rational multiple of
the cycle offset-sum `S_Z`* — is a theorem of the **functional** (out-degree 1)
sector, which X-A's Out-Degree Law shows is glider-free. Generalised to
multi-target constitutions, the reach set is the union over **walks** in the
amendment digraph of their partial offset-sums; asymptotically that is a
**cone** `[λ_min, λ_max]·r`, not a ray, and pigeonholing a point of the support
into it recovers exactly X-A's Theorem 1, `p·min(λ_min,0) ≤ d ≤ p·max(λ_max,0)`
— no more. So Path-Sum Confinement does **not** supply the numerator cap: it
degenerates to the tropical speed law as soon as out-degree exceeds 1, which is
precisely the sector the question lives in.

---

## 7. Frontier tables

Generated by `tables.py` from the raw `.jsonl` in `data/`.
**Every entry is a completed solve.** `timeout` was never used: as X-A warned,
pysat's CaDiCaL bindings cannot be interrupted, so every SAT/UNSAT here is a
decision, never a truncation.

### 7.1 Table A — width-unbounded, single-field sector, `W = 1` `[COMPLETE DECISIONS, no width bound]`

Every full-target constitution with `n` live channels `(a,b,c) ∈ {−1,0,1}³`,
`a ≠ b`, every `d ∈ 1..p`, both resolutions. `NONE` = **no glider at any
width**.

| n | constitutions | COMPLETE for | parity: realisable `(p,d)` | parity: `NONE` at any width | OR: realisable |
|---|---|---|---|---|---|
| 2 | 171 | `p ≤ 6` | (1,1) (2,2) (3,3) **(4,2)** (4,4) **(5,2)** (5,5) **(6,2)** (6,6) | (2,1) (3,1) (3,2) (4,1) **(4,3)** (5,1) (5,3) (5,4) (6,1) (6,3) (6,4) (6,5) (7,1) | (1,1) (2,2) (3,3) (4,4) (5,5) (6,6) — **`|d| ≤ 1`** |
| 3 | 1,140 | `p ≤ 5` | (1,1) (2,1) (2,2) (3,3) **(4,2)** (4,4) **(5,2)** (5,5) **(6,2)** | (3,1) (3,2) (4,1) **(4,3)** (5,1) (5,3) (5,4) (6,1) | (1,1) (2,1) (2,2) (3,3) (4,2) (4,4) (5,5) |
| 4 | 5,985 | `p ≤ 4` | (1,1) (2,1) (2,2) (3,1) (3,2) (3,3) (4,1) (4,2) (4,4) | **(4,3)** | (1,1) (2,1) (2,2) (3,3) (4,2) (4,4) |
| 5 | 26,334 | `(4,3)`, both resolutions | — | **(4,3) — NONE, 0 undecided, both resolutions** | — |

Realised reduced speeds: `n=2` parity `{1, 1/2, 2/5, 1/3}`; `n=3` parity
`{1, 1/2, 2/5, 1/3}`; `n=4` parity `{1, 2/3, 1/2, 1/3, 1/4}`. Under OR:
`{1}` at two channels, `{1, 1/2}` at three and four.

Minimal-period displacement in every row: **`|d| ≤ 2`**. Zero `CAP`
(state-budget) verdicts anywhere in this table.

**The MIRROR family, isolated** (`mirror.py`, the single constitution
`[(0,−1,1), (0,1,−1)]`, width-unbounded):

| p | d = 2, parity | d = 2, OR | d = 3, either |
|---|---|---|---|
| 4 | **GLIDER**, span 53 | NONE | NONE |
| 5 | **GLIDER**, span 20 | NONE | NONE |
| 6 | **GLIDER**, span 616 | NONE | NONE |
| 7 | **GLIDER**, span 438 | NONE | NONE |

One constitution, four gliders, four different minimal periods, one
displacement — plus `(12,2)` at span 39 from the width ladder. All
re-verified by `xnomos`.

### 7.2 Table B — box-fixed SAT map, ALL constitutions `[complete for the stated box]`

Interior `= N − 2W`; base map at interior 14, with a box audit at interiors 20
and 26 on every load-bearing entry, and a width ladder to interior **50** for
`n = 2, W = 1`. Max `|d|` is the largest displacement realised in the box;
"max `d'`" is the largest reduced-speed numerator.

| n | W | interior decided | max `|d|` realised | max `d'` | UNSAT entries |
|---|---|---|---|---|---|
| 2 | 1 | **50** (every `(p,d)`, `p ≤ 12`, both resolutions) | 2 (`p=5`) | 2 | everything else |
| 2 | 2 | 26 | 2 | 2 | `(2,3) (3,4) (4,3) (5,*) (6,5) …` |
| 2 | 3 | 26 | 4 (`p=3`) | 4 | `(2,5) (3,5) (4,5) (5,4) …` |
| 3 | 1 | 26 | 2 | 2 | `(4,3) (5,3) (5,4) (6,5) (7,3..6) (8,3..7)` |
| 3 | 2 | 26 | 8 (`p=5`) | 8 | `(4,7) (5,9) (6,11)` only |
| 3 | 3 | 26 | 14 (`p=5`) | 14 | **none** |
| 4 | 1 | 14 | 6 (`p=7`) | 6 | **none** |
| 4 | 2 | 14 | 9 | 9 | **none** |
| 4 | 3 | 14 | 11 | 11 | **none** |

Read this table with §3.1 in mind: the `n = 2, W = 2` row says `|d| ≤ 2` in a
box of interior 26, while Corollary D2 exhibits a certified `|d| = 4` glider
there of span ≈ 40. **The `W ≥ 2` rows are box statements, not no-goes.**

### 7.3 Table C — the `n = 2, W = 1` speed spectrum, complete to interior 50

All 78 pairs `(p,d)`, `1 ≤ p ≤ 12`, `1 ≤ d ≤ p`, all target matrices (free),
both resolutions, interiors 14/20/26/32/38/44/50 — 156 width scans.

```
parity, realisable:   (p,d) = (1,1) and its iterates (p,p);  (5,2) wmin 26;
                              (10,4) wmin 26;  (12,2) wmin 44
or,     realisable:   (p,p) only
```

Combined with Table A, the `n = 2, W = 1` picture is: `|d| ≤ 2`, with `|d| = 2`
realised at minimal periods 4, 5, 6 and 12 (speeds 1/2, 2/5, 1/3, 1/6) — every
one of them parity-only, every one of them wider than X-A's box.

### 7.4 Table D — `n = 3, W = 1`, the headline cell

The `|d| ≥ 3` frontier at three kinds, all constitutions, all seeds fitting the
interior, both resolutions:

| `(p,d)` | interior 18 | 22 | 26 | 30 | 34 |
|---|---|---|---|---|---|
| **(4,3)** | UNSAT | UNSAT | UNSAT | **UNSAT** | **UNSAT** |
| (5,3) | UNSAT | UNSAT | UNSAT | | |
| (5,4) | UNSAT | UNSAT | UNSAT | | |
| (6,5) | UNSAT | UNSAT | UNSAT | | |
| (7,5) | UNSAT | UNSAT | UNSAT | | |
| (8,6) | UNSAT | UNSAT | UNSAT | | |

Both resolutions, at every interior shown. Plus, from the base map at interior
14, `(7,3) (7,4) (7,6) (8,3) (8,5) (8,7)` UNSAT, and from X-E's deeper runs
`(9,4) (9,5)` UNSAT.

Given §3.1, the honest statement is: **`|d| ≥ 3` at `n = 3, W = 1` is decided
impossible for gliders of span ≤ 34 (for `(4,3)`; ≤ 26 for the rest), and
impossible at any width in the single-field sub-sector. It is NOT established
impossible in general** — and the `n = 2` counterexamples of span 53 and 616
are the reason to keep that caveat sharp.

---

## 8. The law as finally stated

**[established]**

1. **Dilation.** `maxdisp(n, rW) ≥ r·maxdisp(n, W)`. No `W`-independent cap.
2. **Theorem K.** The kind-fields of any orbit are constrained by the 𝔽₂ left
   kernel of the amendment incidence matrix; a glider annihilates every such
   kernel vector.
3. **Lemma FR.** Front advance costs a `c_k > 0` kind; rear clearance costs a
   `c_k ≤ 0` kind.
4. **X-A's `n = 2` claim is false.** Certified `|d| = 2` gliders exist at
   `n = 2, W = 1` at minimal periods 4, 5, 6, 7 and 12 — spans 53, 20, 616,
   438 and 39 — all in one constitution, all parity-only.

**[measured — complete decisions, no width bound]**

5. **The Single-Field Cap.** `W = 1`, every law amends every kind: `|d| ≤ 2`
   (parity), `|d| ≤ 1` (OR at two channels). Complete for `p ≤ 6` (2
   channels), `p ≤ 5` (3), `p ≤ 4` (4), and for the critical `(4,3)` at 5
   channels — 33,630 constitutions decided in all, **0 undecided**.

**[measured — box statements]**

6. **The Field-Count Threshold.** At `W = 1`, `|d| = 3` requires ≥ 4 kinds and
   ≥ 2 kind-fields. Three kinds cannot reach it in a box of interior 26; four
   kinds in one field cannot reach it at any width; four kinds in two fields
   reach it in three cells.
7. **The window buys displacement faster than linearly.** `n = 3` reaches
   `|d| = 5` at `W = 2` (single-field, certified) and `|d| = 14` at `W = 3`.

**[original proposal — conjecture]**

> **Conjecture SF (stated, then refuted here — kept because the refutation is
> the datum).** In the single-field sector at window `W`, every free glider
> satisfies `|d| ≤ 2W` under parity and `|d| ≤ W` under OR.
>
> *Status:* the `W = 1` case is decided at any width for 2–5 channels
> (`|d| ≤ 2` parity / `|d| ≤ 1` OR at two channels). Dilation gives the
> matching lower bound `|d| = 2W`. **It is contradicted at `W = 2` by
> TRIAD (`|d| = 5 > 4`)** — so the conjecture as stated is *false* for
> `W ≥ 2` and survives only as the `W = 1` statement. Recorded here in refuted
> form because the refutation is itself the interesting datum: the `W = 1`
> cap of 2 does **not** scale as `2W`, so whatever mechanism enforces it is
> special to the smallest window.

> **Conjecture FC (the one X-E would attack next).** At `W = 1`, a free glider
> with `|d| ≥ 3` requires **both** at least four kinds **and** at least two
> independent 𝔽₂ kind-fields. Neither condition alone suffices: four kinds in
> one field is `NONE` at any width; three kinds in two fields is UNSAT to span
> 34.

**The field count of every known specimen** (`fields.py`; the field count is
`rank_{𝔽₂}(A)` of the amendment incidence matrix, which is the number of
independent kind-supports by Theorem K):

| specimen | kinds | fields | W | `|d|` |
|---|---|---|---|---|
| TANDEM-1 (X-A) | 2 | 1 | 1 | 1 |
| **MIRROR (X-E)** | 2 | 1 | 1 | **2** |
| X-A DRIFTER-1/2 | 3 | 2 | 1 | 1 |
| X-A speed 2/3 | 3 | 2 | 1 | 2 |
| X-E `n=3 (5,2)` | 3 | 2 | 1 | 2 |
| X-A speed 3/4 | 4 | **2** | 1 | **3** |
| X-A speed 3/5 | 4 | **2** | 1 | **3** |
| X-A speed 6/7 | 4 | **2** | 1 | **6** |
| **TRIAD (X-E)** | 3 | 1 | **2** | **5** |

Read the last three `W = 1` rows against the rest: **every specimen in the
program with `|d| ≥ 3` at `W = 1` has exactly four kinds and exactly two
fields.** And the last row shows the window is a wholly separate escape: one
field, three kinds, `|d| = 5`.

---

## 9. Pre-registration scorecard

| # | prediction | outcome |
|---|---|---|
| **R1** | The `n=3, W=1` cap is real, not a period artefact (0.70). | **Partly right, for the wrong reason.** `|d| ≥ 3` survives to interior 26 and `p ≤ 9`, so it is not a *period* artefact. But the sibling claim at `n = 2` **was** an artefact — of *width*, which I had ranked at only 0.30 (R8). |
| **R2** | The core is a cycle-mean / denominator-`≤ n` statement (0.45 for the shape, 0.20 for `n=3`). | **Refuted.** Cycle means bound the *speed* and say nothing about `d`; and the observed caps are on `d`, not on `d/p`. |
| **R3** | `n = 2` realises exactly `(1, r)`, `r ≤ W`; period 1 only (0.55). Provable (0.55). | **Refuted by my own instrument, decisively.** `n = 2, W = 1` realises minimal periods 4, 5, 6, 12. The proof I expected does not exist because the statement is false. |
| **R4** | Front/rear channel dichotomy provable (0.85); explains `n=3` (0.25). | **Right on the lemma** (§6.3, proved, 2,598 fuzz checks, 0 violations); **right to doubt** that it explains the cap — it does not. |
| **R5** | No full `n=3` theorem (0.20 for a proof); exact table + conjecture instead (0.80). | **Held.** No `n = 3` theorem. The table is here, the boundary is located, and the conjecture is stated — but about fields and windows, not kinds. |
| **R6** | 2-D magnitude cap survives, `n=2` is `p=1` only (0.50). | **Split.** The "`p = 1` only" clause dies with R3. The *cap* clause survives the sample: no reduced 2-D velocity at `n ≤ 3` has a component of magnitude ≥ 3 (§11). Sample, not a decision. |
| **R7** | 0.35 that "`n ≤ 3` is a low-complexity accident with no `f(n)`". | **Essentially right, and it was my best-calibrated call.** There is no `f(n)`. The controlling variables are the field count and the window. |
| **R8** | 0.30 that some X-A UNSAT flips to SAT at a wider box. | **Right, and badly under-weighted.** It flipped, it flipped in the most load-bearing cell, and the objects behind it are 53 and 616 cells wide. Had I priced this at 0.7 I would have started the campaign with the width scan. |

**Calibration lesson.** The one methodological rule that would have found this
in the first hour: *never read a box-fixed UNSAT as a no-go without a width
ladder attached to it.* X-A's instrument states this correctly in its own
docstring; three expeditions in a row, including mine at the start, read past
it.

---

## 10. Live-run status

Finished and reported above: the `n = 5` single-field `(4,3)` decision (both
resolutions, `NONE`, 0 undecided), the MIRROR ladder to `p = 7`, and the
`n = 3, W = 1` box audit at interiors 30/32/34 for `(4,3)` and `(8,6)`.

Still executing when this report was frozen, and **not** used by any table:

* `sweep2.py 2 1 8` — single-field `n = 2` at `p = 7, 8`.
* `sweep2.py 3 1 7` / `sweep2.py 4 1 4` — the tails of those sweeps.
* `sweep2.py 2 2 4` — single-field `n = 2, W = 2` at `p = 4`.
* `mirror.py` — MIRROR at `p ≥ 8`.

Their partial output is in `data/*.log`. Every completeness claim in §7 is
computed by `tables.py` from records actually on disk, and `tables.py` reports
the largest `p` for which **every** `d` and **both** resolutions are present.

---

## 11. Two dimensions `[sample, not a decision]`

`twod.py` samples full-target constitutions in `ℤ²` at `W = 1` and classifies
small seeds with the reference engine (3,000 constitutions × 6 seeds per
`(n, mode)`). Findings, all at `n ∈ {2,3}`:

* Every axis and diagonal unit velocity is realised at `p = 1` (X-A's TANDEM
  lift, reproduced).
* Genuinely 2-D reduced velocities appear at `n = 3`: `p = 3, v = (1,2)` under
  parity, and `p = 2, v = (2,−1)` under OR — a knight-move glider at `W = 1`.
* **The 1-D cap does appear to survive componentwise.** Across the whole
  sample, at `n ≤ 3`, **no reduced velocity has a component of magnitude
  `≥ 3`** — the largest is `2`, exactly the 1-D `W = 1` cap. Every component of
  every observed reduced velocity is a displacement the corresponding 1-D
  universe also realises.
* At `n = 2` the sample found only `p ∈ {1,2}` with `‖v‖_∞ = 1`; it did not
  reach the wide objects, which is expected — the 1-D `n = 2` gliders that beat
  `p = 1` have spans 20–616 and cannot appear in a 3×3 seed search.

So R6's *cap* clause is consistent with the data and its *"`p = 1` only"*
clause is refuted (the 1-D MIRROR family lifts to 2-D by giving every offset a
zero second coordinate). The sample is small and no 2-D no-go is claimed at
all: the SFT construction is one-dimensional, so there is no width-unbounded
2-D instrument.

A width-unbounded 2-D decider is not available — the SFT construction is
one-dimensional — so no 2-D no-go is claimed at all.

---

## 12. Specimens (paste-ready)

```python
import sys; sys.path.insert(0, '/Users/lukacs/claude/math/program/phase6')
import xnomos

# ---- MIRROR: n=2, W=1.  One CA, three gliders, all displacement 2, parity only.
rules  = [(0, 1, -1), (0, -1, 1)]          # right-edge pushes left; left-edge pushes right
tgt    = [(0, 1), (0, 1)]                  # both laws amend both kinds  (single field)
C      = xnomos.Const(rules, tgt)

# MIRROR-2/5   p=5  d=+2   span 20
seed25 = {c: 3 for c in [2,3,4, 6,7,8,9,10, 12,13,14, 16, 18,19,20,21]}
assert xnomos.verify_glider(seed25, C, 5, 2, 'parity')

# MIRROR-1/2   p=4  d=+2   span 53   (minimal period 4: Phi^2 != sigma^1)
seed12 = {c: 3 for c in [1,2,3,4,5,7,9,10,11,13,15,17,19,21,23,26,28,30,31,32,33,
                         34,36,38,40,42,43,44,46,47,48,49,50,51,52,53]}
assert xnomos.verify_glider(seed12, C, 4, 2, 'parity')

# MIRROR-1/6   p=12 d=+2  span 39
seed16 = {c: 3 for c in [3,6,7,8,10,11,12,13,14,16,18,19,20,22,24,25,26,28,29,30,
                         32,33,34,36,37,38,39,40,41]}
assert xnomos.verify_glider(seed16, C, 12, 2, 'parity')

# ---- TRIAD: n=3, W=2, single field, ONE cell -- and the resolution decides
#      the SPEED, not merely whether it moves.
rules3 = [(1, -1, 0), (0, -2, 1), (0, -2, 2)]
C3     = xnomos.Const(rules3, [(0,1,2)]*3)
assert xnomos.verify_glider({0: 7}, C3, 3, 5, 'parity')   # speed 5/3
assert xnomos.verify_glider({0: 7}, C3, 2, 3, 'or')       # speed 3/2

# ---- Dilation of MIRROR-2/5 (Corollary D2): |d| = 2W at n = 2
for r in (2, 3):
    Cr = xnomos.Const([tuple(r*x for x in ru) for ru in rules], tgt)
    assert xnomos.verify_glider({r*c: 3 for c in seed25}, Cr, 5, 2*r, 'parity')

# ---- Theorem K, a relation Lemma T cannot see: every cell carries an EVEN
#      number of kinds, in any glider of this universe.
#      T = [{0,1},{1,2},{0,2}] : |T_k ∩ {0,1,2}| = 2 for every k,
#      yet the three author sets {0,2}, {0,1}, {1,2} are pairwise distinct.
```

---

## 13. Verification battery

| what | how | result |
|---|---|---|
| every SAT model in every campaign | `xsat.solve` auto-certifies with `xnomos.verify_glider` and **raises** on disagreement | 0 raises across ~900 solves |
| every `sft.py` GLIDER verdict | witness columns → `xnomos.verify_glider`, 3 full periods | all `True` |
| `sft.py` against `xsat.py` | 7 head-to-head questions on full-target classes, independent code paths | agree on all 7 (the 8th apparent clash is the span-53 witness, §5) |
| `sft.py` self-test | rediscovers MIRROR-2/5 and TANDEM-1 from scratch; `d > r` path validated on TRIAD (`W=2, p=3, d=5`) | pass |
| Theorem K + K′ + Lemma FR | `thmK.py` fuzz, 3,000 universes, `n ∈ 2..5`, `W ∈ 1..3` | 33,474 checks, **0 violations** |
| Dilation Theorem | `xnomos.verify_glider` on `r = 2, 3` dilations of MIRROR-2/5 | both `GLIDER`, `p = 5`, `d = 4` and `6` |
| solver truncation | `timeout` never passed; pysat CaDiCaL runs to completion | every UNSAT is a completed decision |
| state-cap truncation | `sft.py` returns `CAP` if the reachable set exceeds the budget | **0 `CAP` verdicts** in any reported run |

---

## 14. Code and reproduction

All paths relative to `xspeed/`.

| file | what it does |
|---|---|
| `PREREG.md` | sealed pre-registration |
| `run.py` | parallel driver over X-A's `xsat.py`; one job = one bounded question |
| `jobs.py` | job-file generators: `map`, `deep`, `wide`, `box`, `pmap` |
| `width.py` | width ladders — escalates the interior until SAT, records `wmin` |
| `probe.py` | per-slot windows (`Wa`, `Wb`, `Wc` independent) on top of `xsat` |
| **`sft.py`** | **the width-unbounded decider** (subshift-of-finite-type BFS) |
| `sweep2.py` | width-unbounded sweeps organised by `(p, d)` |
| `n5probe.py` | the 5-channel `(4,3)` decision (both resolutions) |
| `mirror.py` | the MIRROR family, one constitution, `p = 4..12` |
| `fields.py` | kind-field count `rank_{F2}(A)` of any constitution |
| `thmK.py` | fuzz certificate for Theorems K, K′ and Lemma FR |
| `twod.py` | 2-D sample |
| `tables.py` | renders every table in §7 from `data/*.jsonl` |

```sh
python3 sft.py                                   # self-test: rediscovers MIRROR-2/5
python3 thmK.py 3000                             # Theorem K fuzz certificate
python3 jobs.py map  > data/map.json  && python3 run.py data/map.json data/map.jsonl
python3 jobs.py box  > data/box.json  && python3 run.py data/box.json data/box.jsonl
python3 width.py data/spdA.json data/spdA.jsonl  # n=2 W=1 to interior 50
python3 sweep2.py 2 1 6 data/sft2_n2W1.jsonl     # width-unbounded, 2 channels
python3 sweep2.py 3 1 5 data/sft2_n3W1.jsonl     # width-unbounded, 3 channels
python3 sweep2.py 4 1 4 data/sft2_n4W1.jsonl     # width-unbounded, 4 channels
python3 mirror.py                                # the MIRROR (p,2) family
python3 fields.py                                # field counts of all specimens
python3 n5probe.py 5 4 3                         # the 5-channel (4,3) decision
python3 tables.py                                # all frontier tables
```

---

## 15. What remains open

1. **Prove the Single-Field Cap at `W = 1`.** `|d| ≤ 2` for one field, any
   number of channels, is now a decided fact for 2–5 channels at any width and
   the most promising theorem in sight. Lemma FR and the gait word
   (`T(y) = min{t : β(t) ≥ y}` is strictly increasing at `W = 1`, so the
   arrival gaps form a `d`-periodic composition of `p` into `d` positive parts)
   are the two tools I would build on.
2. **Why does the `W = 1` cap of 2 not scale to `2W`?** TRIAD breaks it at
   `W = 2`. Something about `W = 1` — probably that `c ∈ {−1,0,1}` forces the
   front to advance in unit steps — is doing work no dilation preserves.
3. **Is `|d| ≥ 3` really impossible at three kinds?** Decided only to span 26.
   Given that the `n = 2` counterexamples have spans 53 and 616, this is the
   claim in the whole report I would bet against most readily.
4. **Extend the SFT decider past one field.** The construction needs alphabet
   `2^n` per cell for general targets; Theorem K's kernel relations cut that
   alphabet, and for the rank-2 constitutions where `|d| = 3` lives it may be
   just small enough.
5. **A width lower bound.** `wmin(n,W,p,d)` is a well-defined function
   (Table C measures it: 26, 26, 44 for the `n = 2` family) and the data
   suggests it blows up as the arithmetic gets harder. A theorem
   "displacement `d` at `n` kinds needs span `≥ g(d,n)`" would explain every
   census in the program at once.
6. **2-D.** No width-unbounded instrument exists; the sample in §11 already
   refutes the naive transfer of the 1-D cap.
