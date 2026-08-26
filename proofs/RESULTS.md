# Expedition Y-D — closing the open conjectures

*Four named targets, all measured-but-unproved when this expedition opened.
Repo: `/Users/lukacs/claude/math/program/phase6`. Engine: `xnomos.py`.*

---

## 0. Pre-registration

**Frozen 2026-08-26, before the first big run of this expedition.** Written
after reading `README.md`, `XFINDINGS.md`, `nomos2d/JUBILEE-LAW.md`, and after
one small orienting run on the Jubilee specimen (16 384 steps, which established
that the Jubilee's kinds 0 and 1 are frozen singletons and that the code lives on
three axis rays — recorded here so the record shows what was already known when
the predictions were made). Nothing else had been run.

| # | prediction | confidence |
|---|---|---|
| **Y1** | The Jubilee reset law `\|S_{2^k}\| = 4` is a **theorem** and will be proved this expedition. The route is the ray reduction plus an inductive/renormalisation argument on the binary expansion of `t`. | 80 % |
| **Y2** | The crest formula `\|S_{2^k−1}\| = 3·2^{⌊(k−1)/2⌋} + 1/2` will also fall, but is harder than the reset law (it needs the *whole* profile at `2^k − 1`, not just its weight). | 55 % |
| **Y3** | The weight grading (min = `w+3` for `w ≤ 9`, max formula) will **not** fall completely; the min half is a finite claim of a different character from the max half, and I expect at best one half plus a sharpened conjecture. | 35 % for a full proof |
| **Y4** | The Jubilee/Odometer "four laws" coincidence is **not** a conjugacy of the two machines. My prediction: both reduce to a one-dimensional carry automaton, and `4` is forced *separately* in each by the same mechanism — a fixed overhead of frozen/boundary laws plus a weight-1 counter word. I.e. it is a **normal form, not an isomorphism**: the shared cause is "binary counter with a constant frame", and the constant happens to be 4 in both. | 60 % that the two machines are NOT conjugate; 50 % that a common renormalisation is nevertheless exhibited |
| **Y5** | The width-free speed cap (Target 3) will **not** be proved outright. I expect the OR half (`\|d\| ≤ 1`) to be provable and the parity half to survive as a sharpened conjecture. The Dilation tension will be resolved (I predict: dilation does **not** preserve the single-field sector, because spreading one cell into `r` cells changes which cells are occupied and hence the guards). | 30 % full cap, 75 % dilation tension resolved |
| **Y6** | Target 4's converse — *every light-cone-admissible ring rotor is a wrapped ℤ glider* — is **true with a vacancy hypothesis and false without it**. I predict a counterexample exists on a ring with no vacant arc (a fully-occupied or nearly-fully-occupied ring code that rotates inside its light cone without lifting to a finite ℤ glider). | 65 % |
| **Y7** | No target will require a new engine: everything will be checkable through `xnomos.Const/step`. | 90 % |

**Risk clause.** If a "measured" claim in the source documents turns out to be
false as stated, the correction is the result and is reported as such, in the
manner of `XFINDINGS.md`'s two self-caught errors.

**Honesty labels used throughout**: *[established]* = proved here or previously,
*[interpretation]* = a reading of established facts, *[original proposal]* = a
conjecture or a fitted formula, not a theorem. A proof sketch is labelled
**sketch** and is never called a proof.

**The width correction applies**: every bounded search below decides a box, and
the box's parameters are stated with the count.

---

## 1. TARGET 1 — the Jubilee clock law: **CLOSED**

*All three parts fall, to one closed form. The reset law and the crest law are
theorems for **every** k, not just the sixteen measured. The grading's max half
is a theorem for every w; its **min half as published is a box artefact of
`t < 2^17` and is corrected here.***

Certificates: `python3 proofs/t1_jubilee.py --deep` — 15/15, complete over
`t < 2^17` against `xnomos.step` on the original 2-D specimen.

### 1.1 The specimen and the reduction to a ray *[established]*

Kinds (compass `E=(1,0)`, `W=(−1,0)`, `N=(0,−1)`, `S=(0,1)`), own-kind, parity:

| kind | guard "some law at" | guard "no law at" | enacts at |
|---|---|---|---|
| 0 = ESN | `E` | `S` | `N` |
| 1 = SNS | `S` | `N` | `S` |
| 2 = WNE | `W` | `N` | `E` |

Seed `S_0 = {ESN@(−1,0), SNS@(−1,1), WNE@(0,1)}`.

> **Lemma 1.1 (three rays).** For every `t`, `supp_k(S_t) ⊆ supp_k(S_0) + ℕ·c_k`.

*Proof.* Single-Author Lemma: the only law that can flip kind `k` at cell `j` is
the kind-`k` law at `j − c_k`. So a kind-`k` law can only be created one `c_k`
beyond an existing kind-`k` law; induct on `t`. ∎

Concretely `supp_0 ⊆ {(−1,−a) : a ≥ 0}`, `supp_1 ⊆ {(−1,1+b) : b ≥ 0}`,
`supp_2 ⊆ {(c,1) : c ≥ 0}` — three **pairwise disjoint** rays (the first has
`x=−1, y≤0`; the second `x=−1, y≥1`; the third `y=1, x≥0`). Occupancy is the
union, so occupancy of any cell is decided by which ray it lies on.

> **Lemma 1.2 (the frame is frozen).** `supp_0(S_t) = {(−1,0)}` and
> `supp_1(S_t) = {(−1,1)}` for every `t`; both laws are permanently blocked.

*Proof.* A kind-0 law at `(−1,−a)` needs `occ((0,−a))`. That cell has `x = 0 ≥ 0`
and `y = −a ≤ 0`, so it lies on none of the three rays (`x=−1` fails for the
first two, `y=1` fails for the third): the guard never passes, so no kind-0 law
ever fires and `supp_0` never changes. Then, by induction on `t`,
`supp_1(S_t) = {(−1,1)}`: the only kind-1 law present sits at `b = 0` and needs
`¬occ((−1,0))`, but `(−1,0)` carries the permanent kind-0 law, so it is blocked;
the only cell a kind-1 law could ever create is `b = 1`, and only that blocked
law could create it. ∎

Write `C_t ⊆ ℕ` for the kind-2 ray coordinates: `WNE@(c,1)` iff `c ∈ C_t`.

> **Lemma 1.3 (the carry automaton).** `|S_t| = 2 + |C_t|`, `0 ∈ C_t` for all `t`,
> and
> ```
> C_{t+1} = K(C_t),   K(C) = C Δ { c+1 : c ∈ C, (c = 0 or c−1 ∈ C) }.
> ```

*Proof.* A kind-2 law at `(c,1)` needs `occ((c−1,1))` and `¬occ((c,0))`. The cell
`(c,0)` (`x = c ≥ 0`, `y = 0`) lies on no ray, so the vacancy clause always
passes. For `c = 0` the precedent cell is `(−1,1)`, which carries the permanent
kind-1 law, so the law at `c = 0` is **always active**; for `c ≥ 1` it is active
iff `c−1 ∈ C`. An active law toggles kind 2 at `(c+1,1)`. Toggles land only at
`c ≥ 1`, so `0 ∈ C_t` forever. ∎

Substituting `y_n := [n+1 ∈ C]` and using `[0 ∈ C] ≡ 1` turns `K` into a rule
with **no boundary case at all**:

> ```
> y_n(t+1) = y_n(t) ⊕ ( y_{n−1}(t) ∧ y_{n−2}(t) ),   y_{−1} ≡ y_{−2} ≡ 1,
> y(0) = 0,        |S_t| = 3 + wt(y(t)).
> ```

*A lazy binary counter*: bit `n` flips when the **two** bits below it are both
set — where an honest counter would ask for **all** the bits below it. That one
truncation is the whole of the Jubilee.

*Certificate*: the 2-D engine and this rule run in lockstep for every `t < 2^17`
(131 072 steps), with `|S_t| = 3 + wt(y(t))` checked at each step. **Complete box.**

### 1.2 The Monomial Law *[established — this is the whole engine]*

For finite `M ⊆ ℕ` write `f_M(t) = ∏_{i∈M} bit_i(t) = [M ⊆ supp₂(t)]`, where
`supp₂(t)` is the set of positions of the 1-bits of `t`. Note `f_∅ ≡ 1` and
`f_A·f_B = f_{A∪B}`.

> **Lemma 1.4 (partial sums of a monomial are a monomial).** For every finite
> `M ⊆ ℕ` and every `t ≥ 0`,
> ```
>   Σ_{s<t} f_M(s)  ≡  f_{σ(M)}(t)   (mod 2),     σ(M) = {q} ∪ {i ∈ M : i > q},
> ```
> where `q = mex(M)` is the least non-element of `M`.

*Proof.* `Σ_{s<t} f_M(s) = #{s < t : M ⊆ supp₂(s)}`. Split by the highest bit at
which `s` differs from `t`: `s < t` iff there is a unique `q` with
`bit_q(s)=0`, `bit_q(t)=1` and `bit_i(s)=bit_i(t)` for all `i > q`. For a given
such `q` the count of admissible `s` is `0` unless `q ∉ M` and every element of
`M` above `q` lies in `supp₂(t)`; the bits below `q` are free except that those
in `M` are forced to 1, so the count is `2^{#{i<q : i ∉ M}}`. Modulo 2 the term
survives iff that exponent is `0`, i.e. iff `{0,…,q−1} ⊆ M`. Together with
`q ∉ M` this pins `q = mex(M)` — **exactly one** term survives, and it equals
`[bit_q(t)=1] · ∏_{i∈M, i>q} bit_i(t) = f_{σ(M)}(t)`. ∎

> **Theorem 1.5 (Monomial Law).** Put `M_{−2} = M_{−1} = ∅` and
> `M_n = σ(M_{n−1} ∪ M_{n−2})` for `n ≥ 0`. Then for all `n ≥ 0` and all `t ≥ 0`
> ```
>                       y_n(t) = f_{M_n}(t).
> ```

*Proof.* Strong induction on `n`. Summing the rule,
`y_n(t) = y_n(0) ⊕ Σ_{s<t} y_{n−1}(s) y_{n−2}(s)` and `y_n(0)=0`. By induction
(the cases `n = 0,1` using `y_{−1}=y_{−2}=1=f_∅`),
`y_{n−1}(s)y_{n−2}(s) = f_{M_{n−1}}(s) f_{M_{n−2}}(s) = f_{M_{n−1} ∪ M_{n−2}}(s)`,
and Lemma 1.4 turns the partial sum into `f_{σ(M_{n−1}∪M_{n−2})}(t) = f_{M_n}(t)`. ∎

The first monomials:

```
n     0     1     2      3       4    5      6        7        8        9      10   11
M_n  {0}   {1}   {2}  {0,1,2}  {3}  {4}  {0,3,4}  {1,3,4}  {2,3,4}  {0..4}   {5}  {6}
```

> **Corollary 1.6 (the closed form).**
> ```
>            |S_t|  =  3 + #{ n ≥ 0 : M_n ⊆ supp₂(t) }.
> ```
> `|S_t|` depends on `t` **only through the set of positions of its 1-bits**.

*Certificate*: `y_n(t) = f_{M_n}(t)` for all `n < 200` and all `t < 2^13`
(1 638 400 bit identities, complete box); Lemma 1.4 on every `M ⊆ [0,6]` with
`|M| ≤ 4` over `t < 2^10` (99 sets × 1024, complete box); the closed form against
`xnomos.step` for every `t < 2^17` (complete box).

### 1.3 The block structure *[established]*

> **Theorem 1.7 (blocks).** Let `N_j = 3·2^j − 2` (so `N_0,N_1,… = 1,4,10,22,46,…`,
> `N_{j+1} = 2N_j + 2`) and `Q_j = {2j+1, 2j+2}`. Then for every `j ≥ 0`
>
> 1. `M_i ⊆ [0,2j]` for all `i < N_j`, with `M_{N_j−1} = [0,2j]` and
>    `M_i ≠ [0,2j]` for `i < N_j − 1`;
> 2. `M_{N_j} = {2j+1}` and `M_{N_j+1} = {2j+2}`;
> 3. `M_{N_j+2+i} = M_i ∪ Q_j` for every `0 ≤ i < N_j`.
>
> So the list of monomials is built by the substitution
> `𝓜_{j+1} = 𝓜_j ⧺ [{2j+1}, {2j+2}] ⧺ (𝓜_j ∪ Q_j)`.

*Proof.* Induction on `j`. **Base** `j = 0`: `N_0 = 1`, `M_0 = σ(∅) = {0} = [0,0]`,
`M_1 = σ({0}) = {1}`, `M_2 = σ({1}∪{0}) = σ([0,1]) = {2}`,
`M_3 = σ({2}∪{1}) = σ({1,2}) = {0,1,2} = M_0 ∪ Q_0`. ✓

**Step.** Assume (1)–(3) at level `j`. Then
`M_{N_j} = σ(M_{N_j−1} ∪ M_{N_j−2}) = σ([0,2j]) = {2j+1}` (the union is `[0,2j]`
since `M_{N_j−2} ⊆ [0,2j]`), and
`M_{N_j+1} = σ({2j+1} ∪ [0,2j]) = σ([0,2j+1]) = {2j+2}`.
For (3) use the *shift rule*: **if `M ⊆ [0,2j]` and `M ≠ [0,2j]` then
`σ(M ∪ Q_j) = σ(M) ∪ Q_j`** — because then `q = mex(M) ≤ 2j`, so
`mex(M ∪ Q_j) = q` as well, and `Q_j` sits entirely above `q`. Now
`M_{N_j+2} = σ({2j+2} ∪ {2j+1}) = σ(∅ ∪ Q_j) = {0} ∪ Q_j = M_0 ∪ Q_j`, and
`M_{N_j+3} = σ((M_0∪Q_j) ∪ {2j+2}) = σ(M_0 ∪ Q_j) = σ(M_0) ∪ Q_j = M_1 ∪ Q_j`;
for `2 ≤ i < N_j`,
`M_{N_j+2+i} = σ((M_{i−1}∪M_{i−2}) ∪ Q_j) = σ(M_{i−1}∪M_{i−2}) ∪ Q_j = M_i ∪ Q_j`,
the shift rule applying because `M_{i−1}∪M_{i−2} = [0,2j]` would force
`M_i = {2j+1} ⊄ [0,2j]`, contradicting (1). Finally
`M_{N_{j+1}−1} = M_{N_j−1} ∪ Q_j = [0,2j] ∪ Q_j = [0,2j+2]`, and no earlier index
gives `[0,2j+2]`, which is (1) at level `j+1`. ∎

Two consequences used below.

> **Corollary 1.8 (singletons).** `M_n` is a singleton exactly for
> `n ∈ {0} ∪ {N_j, N_j+1 : j ≥ 0}`, and then `M_0 = {0}`, `M_{N_j} = {2j+1}`,
> `M_{N_j+1} = {2j+2}`. **Every `k ≥ 0` occurs as `M_n = {k}` for exactly one `n`.**

> **Corollary 1.9 (initial segments).** `{n : M_n ⊆ [0,K]} = [0, A(K))` where
> ```
> A(−1) = 0,   A(2j) = N_j = 3·2^j − 2,   A(2j+1) = N_j + 1 = 3·2^j − 1.
> ```

### 1.4 The three laws

> ### **THEOREM 1.10 (the reset law).** `|S_{2^k}| = 4` for **every** `k ≥ 0`.

*Proof.* `supp₂(2^k) = {k}`, and every `M_n` is non-empty, so
`M_n ⊆ {k}` iff `M_n = {k}`. By Corollary 1.8 exactly one `n` qualifies. By
Corollary 1.6, `|S_{2^k}| = 3 + 1 = 4`. ∎

*The mechanism in words.* The Jubilee is a lazy binary counter whose bit `n`
carries the monomial `M_n` of the clock's bits. A power of two lights exactly one
clock bit, and exactly one counter bit is a pure function of that clock bit
alone. **Four = three frame laws + one surviving monomial.**

> ### **THEOREM 1.11 (the crest law).** `|S_{2^k−1}| = 3 + A(k−1)`, i.e.
> `3·2^{⌊(k−1)/2⌋} + 1` for odd `k` and `+ 2` for even `k`. Moreover
> `t = 2^k − 1` is the **unique** maximiser of `|S_t|` over `t < 2^k`.

*Proof.* `supp₂(2^k−1) = [0,k−1]`, so `|S| = 3 + A(k−1)` by Corollary 1.9. With
`k−1 = 2j` (k odd) `A = 3·2^{(k−1)/2} − 2`, giving `3·2^{(k−1)/2}+1`; with
`k−1 = 2j+1` (k even) `A = 3·2^{(k−2)/2} − 1`, giving `3·2^{(k−2)/2}+2`, and
`⌊(k−1)/2⌋ = (k−2)/2` for even `k`. For uniqueness: `W ↦ #{n : M_n ⊆ W}` is
monotone, and if `W ⊊ [0,k−1]` misses a bit `i` then the singleton `M_n = {i}` of
Corollary 1.8 is lost, so the count drops by at least 1. ∎

This also **proves the "√t" reading**: the crest — and the reach — is
`3·2^{⌊(k−1)/2⌋} + O(1) ≍ 1.5·√t`, doubling every *second* power of two exactly
because the substitution of Theorem 1.7 consumes **two** new bits per doubling.

> ### **THEOREM 1.12 (the grading).** Write `w = w(t)` for the binary weight, and
> group the bit positions into the singleton `{0}` and the pairs
> `P_j = {2j+1, 2j+2}`, `j ≥ 0`; put `a_j = |supp₂(t) ∩ P_j|`. Then
> ```
>   F(t) := |S_t| − 3   is computed by   F ← [0 ∈ supp₂(t)],
>   then, for j = 0,1,2,…:   F ← F + a_j          if a_j ≤ 1
>                            F ← 2F + 2           if a_j = 2.
> ```
> Consequently, over **all** `t`:
> * **max** `{|S_t| : w(t)=w}` `= 2^{w/2+1} + 1` for even `w`,
>   `= 3·2^{(w−1)/2} + 1` for odd `w`;
> * **min** `{|S_t| : w(t)=w}` `= w + 3`, for **every** `w`.

*Proof.* The recursion is Theorem 1.7 read as a counting recursion:
`F_{j+1} = F_j·(1 + [a_j = 2]) + a_j` with `F_0 = [0 ∈ W]`, since the level-`(j+1)`
list is the level-`j` list, plus the two singletons `{2j+1},{2j+2}` (contributing
`a_j`), plus a copy of the level-`j` list tagged with `Q_j` (contributing `F_j`
only when both bits of `P_j` are present).

*Max.* Only the multiset of operations matters (`a_j = 0` is the identity and
there are infinitely many `j`), and `F ↦ 2F+2` should follow `F ↦ F+1`, so with
`d` doublings and `s` single steps, `ε_0 + s + 2d = w`, the value is
`2^d(ε_0+s+2) − 2 = 2^d(w+2−2d) − 2`. The ratio test `g(d+1)/g(d) ≥ 1 ⟺ w−2d ≥ 2`
puts the optimum at `d = ⌊w/2⌋`: `2^{w/2}·2 − 2` for even `w` and
`2^{(w−1)/2}·3 − 2` for odd `w`. Add 3.

*Min.* Each operation raises `F` by at least its weight cost:
`+a_j` costs `a_j` for `a_j ≤ 1`, and `2F+2` raises `F` by `F+2 ≥ 2 =` its cost.
Hence `F ≥ w`, with equality realised by `W = {1,3,5,…,2w−1}` (one bit per pair,
never a doubling). ∎

### 1.5 A correction: the published min table is a box artefact *[established]*

`JUBILEE-LAW.md` (3) reports
`min{|S_t| : w(t)=w} = w+3` for `w ≤ 9`, "then 14, 19, 30, 53, 100, 195, 386, 769".

**That tail is an artefact of the search window `t < 2^17`, not a fact about the
Jubilee.** Seventeen bit positions offer only the singleton `{0}` and eight pairs
`P_0,…,P_7`, so at most `1 + 8 = 9` units of weight can be spent without filling a
pair — and a filled pair forces a doubling. For `w ≥ 10` the box *compels* the
expensive operation. Theorem 1.12 gives `min = w+3` for every `w`; the witnesses
for `w = 10,…,16` need 20, 22, 24, 26, 28, 30, 32 bits and are invisible below
`2^17`.

*Certificate (both directions).* Restricted to `t < 2^17` the closed form
reproduces the published tail **exactly** —
`[4,5,6,7,8,9,10,11,12,14,19,30,53,100,195,386,769]` — and the unbounded
witnesses `W = {1,3,5,…}` give `w+3` for every `w`. The max half needs no
correction: its optimum uses `⌊w/2⌋` pairs, which fits inside 17 bits for all
`w ≤ 17`.

> **The width correction, applied to chapter one.** `XFINDINGS.md` §5 re-labelled
> every bounded *glider* search as a narrow-glider statement. The same correction
> reaches the **extremal statistics of the 2-adic sector**: a min-over-a-weight-class
> is a min over the bit positions the window makes available. Here the box was not
> a box in space but a box in **time**, and it bit at exactly the point where the
> published table stops being linear.


### 1.6 The Jubilee in one line *[established]*

The operator `σ` of Lemma 1.4 — *clear the trailing block of 1s, set the first
0* — **is binary increment**. Identifying a finite set with the integer whose
bits it names, `μ_n := Σ_{i∈M_n} 2^i`, the whole recursion collapses to

> ### **THE JUBILEE LAW.**
> ```
>     μ_{−2} = μ_{−1} = 0,       μ_n = ( μ_{n−1}  OR  μ_{n−2} ) + 1
>
>     |S_t|  =  3  +  #{ n ≥ 0 :  μ_n  AND  NOT t  =  0 }
> ```
> i.e. **three, plus the number of terms of the OR-Fibonacci sequence that are
> submasks of `t`**. The sequence is
> `1, 2, 4, 7, 8, 16, 25, 26, 28, 31, 32, 64, 97, 98, 100, 103, …`

The block structure reads `μ_{N_j} = 2^{2j+1}`, `μ_{N_j+1} = 2^{2j+2}`,
`μ_{N_j+2+i} = μ_i + 3·2^{2j+1}`; the three laws of §1.4 are then, respectively:
*exactly one `μ_n` equals each power of two* (reset), *`{n : μ_n ≤ 2^k−1 as a
submask} = [0, A(k−1))`* (crest), and the pair recursion of Theorem 1.12
(grading).

*Certificate*: `μ_n` equals the bitmask of `M_n` for all `n < 2000`; and
`|S_t| = 3 + #{n : μ_n & ~t = 0}` checked against `xnomos.step` for every
`t < 2^13`.

### 1.7 Aperiodicity, now a theorem *[established]*

`nomos2d/RESULTS.md` reports the Jubilee as *"aperiodic through 300 000
fully-hashed steps"*. It is aperiodic, full stop.

> **Theorem 1.13.** The Jubilee orbit never repeats a state; `{S_t : t ≥ 0}` is
> infinite.

*Proof.* By Theorem 1.10 and Corollary 1.8, at `t = 2^k` the state is the frame
plus `WNE@(0,1)` plus a single `WNE@(m_k+1, 1)`, where `m_k` is the unique index
with `μ_{m_k} = 2^k`; by Theorem 1.7, `m_k = 3·2^{⌊(k−1)/2⌋} − 2` or `−1`, which
is strictly increasing in `k`. So the states at `t = 1, 2, 4, 8, …` are pairwise
distinct, the orbit is infinite, and a deterministic map cannot return to an
already-visited state. ∎

The same argument, through Theorem 2.3, gives **aperiodicity of THE ODOMETER**
— previously "no recurrence in 300 000 hashed steps; 179 survivors of a 3-stage
escalation."

---

## 2. TARGET 2 — the four-law coincidence: **CLOSED, and it broke**

*It is not a coincidence and it is not a normal form. **The two machines are the
same machine.** THE ODOMETER is the Jubilee Code running at half speed, with its
carry buffer materialised as laws. The map exists and is exhibited below; the
Odometer's clock law is a corollary of Theorem 1.10.*

Certificates: `python3 proofs/t2_odometer.py --deep` — 11/11.

**Pre-registration Y4 is REFUTED in its main clause** (I predicted 60 % that the
two machines are *not* conjugate) and held in its subordinate one (the "4" is
indeed a fixed frame plus a weight-one counter word). The record stands as
written.

### 2.1 The Odometer's reduction *[established]*

Specimen (`xamend2d/`): two kinds, cross-amendment, three laws.
`A = (O, E, W) → {B}`, `B = (N, NW, SE) → {A, B}`, seed
`A@(0,0)`, `A@(1,0)`, `B@(0,1)`. (`O=(0,0)`, `NW=(−1,−1)`, `SE=(1,1)`.)

> **Lemma 2.1 (the frame).** `A@(0,0)` and `A@(1,0)` stand forever;
> `A@(0,0)` is permanently blocked and `A@(1,0)` is permanently active;
> `B@(0,1)` stands forever; no cell with `x ∉ {0,1}` or `y < 0` is ever occupied;
> `(1,1)` is never occupied.

*Proof.* (Lemmas 2.1 and 2.2 are one induction on `u`; the statements are split
only for readability, and the "column 2 is empty" clause used here is carried
along as part of that induction's hypothesis.)
Kind `A` is created only by an active `B` at `p+(1,1)`, so `(0,0)` would
need `B@(−1,−1)` and `(1,0)` would need `B@(0,−1)`: neither column `−1` nor row
`y<0` is ever reached (kind `B` is created at `p+W` from an `A`, i.e. in column
`x−1`, and at `p+(1,1)` from a `B`), so both frame laws are permanent. `A@(0,0)`
needs `¬occ((1,0))`, which fails forever. `A@(1,0)` needs `¬occ((2,0))`; column 2
is shown empty in Lemma 2.2. `B@(0,1)` can only be toggled by an active `A@(1,1)`,
and `(1,1)` is never occupied because kind `A` and kind `B` appear in column 1
only at `p+(1,1)` for `p = (0,y)` with `y ≥ 1`. ∎

> **Lemma 2.2 (two phases).** Write `D_u ⊆ ℕ` for `{y : B@(0,y)}` at time `2u`.
> Then for every `u ≥ 0`:
> * at time `2u`: the state is the frame plus `{B@(0,y) : y ∈ D_u}`, `1 ∈ D_u`,
>   `0 ∉ D_u`, and column 1 holds only the frame law `A@(1,0)`;
> * at time `2u+1`: the state is the frame, plus `B@(0,0)`, plus
>   `{B@(0,y) : y ∈ D_u}`, plus **both** kinds at `{(1,y+1) : y ∈ α_u}` where
>   `α_u = {y ∈ D_u : y = 1 or y−1 ∈ D_u}` is the set of **pending carries**;
> * `D_{u+1} = D_u Δ (α_u + 1)`.
>
> No law of kind `B` in column 1 is ever active, so column 2 stays empty.

*Proof.* At an even tick: `A@(1,0)` fires and toggles `B` at `(0,0)`, creating
`B@(0,0)`. A law `B@(0,y)` needs `occ((0,y−1))` and `¬occ((−1,y−1))`; column `−1`
is empty, and `(0,0)` carries the permanent `A`, so `B@(0,1)` is always active and
`B@(0,y)`, `y ≥ 2`, is active iff `y−1 ∈ D_u`. Each active one toggles **both**
kinds at `(1,y+1)` — the carry buffer. That is the odd state.

At the odd tick: `A@(1,0)` fires again and *removes* `B@(0,0)`. `B@(0,0)` itself
needs `occ((0,−1))` and is blocked. Each `A@(1,y+1)` of the buffer is active
(guard `O`, and column 2 is empty) and toggles `B` at `(0,y+1)` — writing the
carries back. The `B` laws of the buffer would toggle at `(2,·)`, but they are all
blocked: `B@(1,z)` needs `occ((1,z−1))` and `¬occ((0,z−1))`; `occ((1,z−1))` with
`z−1 ≥ 1` forces `z−1 ∈ α_u+1`, i.e. `z−2 ∈ α_u ⊆ D_u`, so `z−2 ∈ D_u`; but
`z ∈ α_u+1` forces `z−1 ∈ α_u ⊆ D_u`, contradicting `¬occ((0,z−1))`. Meanwhile
the column-0 `B` laws fire exactly as at the even tick, cancelling the buffer they
created. So column 1 empties, column 2 is never written, and
`D_{u+1} = D_u Δ (α_u+1)`. ∎

### 2.2 The map *[established — this is the answer to Target 2]*

> ### **THEOREM 2.3 (the Odometer is the Jubilee).** Put `D = C + 1`. Then the
> Odometer's two-step map on its even-time states is **exactly** the Jubilee's
> one-step carry automaton `K` of Lemma 1.3:
> ```
>       D ↦ D Δ {y+1 : y ∈ D, (y = 1 or y−1 ∈ D)}   ≅   K
> ```
> and, with `C_u` the Jubilee's kind-2 support at time `u`,
> ```
>   κ_O(Φ_O^{2u}(seed_O)) = C_u + 1,        |Φ_O^{2u}(seed_O)| = |Φ_J^u(seed_J)|,
>   |Φ_O^{2u+1}(seed_O)|  = 3 + |C_u| + 2·act(C_u),
> ```
> where `act(C) = #{c ∈ C : c = 0 or c−1 ∈ C}` is the number of **active** laws of
> the carry automaton.

*Proof.* Under `y = c+1`, the condition "`y = 1` or `y−1 ∈ D`" reads "`c = 0` or
`c−1 ∈ C`", and the target `y+1` is the shift of `c+1`: Lemma 2.2's map is
`K` conjugated by `+1`. Both seeds give `C_0 = {0}`, `D_0 = {1}`. The even-time
card is `2` (frame `A`s) `+ |D_u| = 2 + |C_u| = |S^J_u|` by Lemma 1.3. The odd-time
card is `2 + (|D_u| + 1) + 2|α_u| = 3 + |C_u| + 2·act(C_u)`. ∎

> ### **COROLLARY 2.4 (the Odometer's clock law).**
> `|S^O_{2^k}| = |S^J_{2^{k−1}}| = 4` for every `k ≥ 1`, and
> `|S^O_{2^k−1}| = 6 + 3·A(k−2)`, i.e. `9·2^{(k−2)/2}` for even `k ≥ 2` and
> `9·2^{(k−3)/2} + 3` for odd `k ≥ 3` (and `6` at `k = 1`).

*Proof.* The reset is Theorem 1.10 at `k−1`. For the crest, `2^k−1 = 2u+1` with
`u = 2^{k−1}−1`; by Corollary 1.9 the Jubilee's state at `2^{k−1}−1` is the
**contiguous block** `C = [0, A(k−2)]`, on which every law is active, so
`|C| = act(C) = A(k−2)+1` and the odd-time card is `3 + 3(A(k−2)+1)`. ∎

*Certificate*: `6, 9, 12, 18, 21, 36, 39, 72, 75` for `k = 1..9` — the published
crest list of `XFINDINGS.md` §3, now closed-form.

### 2.3 What the coincidence actually was *[interpretation]*

The two constitutions are **not** isomorphic — one is own-kind (out-degree 1),
the other has out-degree 2 — and no conjugacy of *constitutions* exists. What
exists is a **common renormalisation**: both are implementations of the single
one-dimensional automaton

```
      K :  C ↦ C Δ { c+1 : c ∈ C, (c = 0 or c−1 ∈ C) }        (C ⊆ ℕ, 0 ∈ C)
```

and they differ only in *how they schedule the carry*.

* The **Jubilee** is a **one-phase** implementation. Own-kind targeting makes the
  update `𝔽₂`-linear-modulated-by-occupancy, and synchrony computes the whole
  carry set from the old state in a single tick. Its cost is that it needs three
  kinds — two of them a permanently blocked *frame* supplying the boundary
  conditions `y_{−1} = y_{−2} = 1`.
* The **Odometer** is a **two-phase** implementation: *fetch* (materialise the
  pending carries as real laws in column `x = 1`) then *write back*. Its cost is
  a factor of two in time; its saving is one kind. Materialising a carry means
  writing **two** kinds into one cell — a carry marker `A` and its shadow `B` —
  and that is precisely what **out-degree 2** buys. Cross-amendment is not
  incidental here: it is the register file.

So the answer to *"is that a coincidence or a normal form?"* is **neither**: it
is a simulation, and the simulation is exact. The reset constant is

```
        4  =  3  (frame: two permanent laws + the permanent counter cell)
           +  1  (monomials M_n equal to the singleton {k}: exactly one).
```

Both machines carry the same frame size, so both read 4. *The two binary counters
of the field are one counter with two clocks.*

### 2.4 A correction: the Odometer's reach is √t, not (log t)² *[established]*

`xamend2d/RESULTS.md` headline 9 (and its `gallery.py` note) states: *"reach
≈ 0.20 (log₂ t)², = 86 cells at t = 2²⁰ … the slowest clock in the fauna (the
Jubilee code's reach is ≈ 1.5√t)."*

**That is wrong, and Theorem 2.3 says why it had to be**: the Odometer *is* the
Jubilee, so its reach is the Jubilee's, at half the clock. Exactly:

> **Proposition 2.5.** The Odometer's height at `t = 2^k` is `m_{k−1} + 3`, where
> `m_k` is the unique index with `M_{m_k} = {k}` (Corollary 1.8): `m_k = k` for
> `k ≤ 2`, `m_{2j+1} = 3·2^j − 2`, `m_{2j+2} = 3·2^j − 1`. Hence
> height `= 3·2^{⌊(k−2)/2⌋} + O(1) ≍ 1.5·√t`.

*Certificate (`xnomos.step`, engine, `k = 1..16`)*: measured heights
`3, 4, 5, 7, 8, 13, 14, 25, 26, 49, 50, 97, 98, 193, 194, 385` — matching
`m_{k−1}+3` at every one. The published fit gives `12.8` where the engine gives
`25` (`k=8`) and `39.2` where the engine gives `193` (`k=14`); it is already
wrong by 5× inside the range that was run. At `t = 2^20` the height is **1537**,
not 86. `height(2^k)/2^{k/2}` oscillates in `(1.08, 1.57)` — it doubles every
*second* power of two, which is the same Θ(√t) law as the Jubilee's, with the
same constant 1.5.

The qualitative claims that rested on it survive untouched: bounded card,
unbounded reach, hence **aperiodic**. What fails is only the rate, and with it
the epithet "the slowest clock in the fauna" — there is no slower clock, because
there is only one clock.

