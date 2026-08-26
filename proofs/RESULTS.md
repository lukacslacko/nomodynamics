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

Certificates: `python3 proofs/t1_jubilee.py --deep` — 29/29, complete over
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

The whole Jubilee, on one screen (`#` = a law of `y`, i.e. `WNE@(n+1,1)`):

```
t= 0 ......................    t=16 .....#................
t= 1 #.....................    t=17 #....#................
t= 2 .#....................    t=18 .#...#................
t= 3 ##....................    t=19 ##...#................
t= 4 ..#...................    t=20 ..#..#................
t= 5 #.#...................    t=21 #.#..#................
t= 6 .##...................    t=22 .##..#................
t= 7 ####..................    t=23 ####.#................
t= 8 ....#.................    t=24 ....##................
t= 9 #...#.................    t=25 #...###...............
t=10 .#..#.................    t=26 .#..##.#..............
t=11 ##..#.................    t=27 ##..####..............
t=12 ..#.#.................    t=28 ..#.##..#.............
t=13 #.#.#.................    t=29 #.#.###.#.............
t=14 .##.#.................    t=30 .##.##.##.............
t=15 #####.................    t=31 ##########............
                               t=32 ..........#...........
```

Read the left column: `t = 1,2,4,8,16` each show **exactly one** `#`, and rows
`0…7` are reproduced verbatim in rows `8…15` with a `#` added at index 4. That
repetition is Theorem 1.7.

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
over `t < 2^10` (all 512 subsets × 1024 = 524 288 identities, complete box, and
the referee's independent run widened it to all 512 subsets × `t < 2^12`); the
closed form against
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
`M_{N_j+2} = σ({2j+2} ∪ {2j+1}) = σ(∅ ∪ Q_j) = {0} ∪ Q_j = M_0 ∪ Q_j`, which is
clause (3) for `i = 0`. **If `j = 0` then `N_0 = 1` and `i = 0` is the only case,
so we are done**; the next two lines are for `j ≥ 1`, where `N_j ≥ 4`. (The
restriction is not cosmetic: at `j = 0` the line below would read
`M_4 = M_1 ∪ Q_0 = {1,2}`, and in fact `M_4 = {3}` — the shift rule's hypothesis
`M ⊊ [0,2j]` fails for `M = M_0 = {0} = [0,0]`.) For `i = 1`,
`M_{N_j+3} = σ((M_0∪Q_j) ∪ {2j+2}) = σ(M_0 ∪ Q_j) = σ(M_0) ∪ Q_j = M_1 ∪ Q_j`,
the shift rule applying because `M_0 = {0} ⊊ [0,2j]` once `j ≥ 1`; and for
`2 ≤ i < N_j`,
`M_{N_j+2+i} = σ((M_{i−1}∪M_{i−2}) ∪ Q_j) = σ(M_{i−1}∪M_{i−2}) ∪ Q_j = M_i ∪ Q_j`,
the shift rule applying because `M_{i−1}∪M_{i−2} = [0,2j]` would force
`M_i = {2j+1} ⊄ [0,2j]`, contradicting (1). Finally
`M_{N_{j+1}−1} = M_{N_j−1} ∪ Q_j = [0,2j] ∪ Q_j = [0,2j+2]`, and no earlier index
gives `[0,2j+2]`, which is (1) at level `j+1`. ∎

Two consequences used below.

> **Corollary 1.8 (singletons).** `M_n` is a singleton exactly for
> `n ∈ {0} ∪ {N_j, N_j+1 : j ≥ 0}`, and then `M_0 = {0}`, `M_{N_j} = {2j+1}`,
> `M_{N_j+1} = {2j+2}`. **Every `k ≥ 0` occurs as `M_n = {k}` for exactly one `n`.**

*Proof.* Every index other than `0`, `N_j`, `N_j+1` is of the form `N_j+2+i` with
`0 ≤ i < N_j`, and then `M_n = M_i ∪ Q_j` has at least `1 + 2 = 3` elements (the
`M_i` are non-empty and disjoint from `Q_j ⊆ [2j+1, 2j+2]`). The listed indices
give the singletons `{0}`, `{2j+1}`, `{2j+2}` — i.e. each `k ≥ 0` exactly once
(`k = 0` from `M_0`; `k = 2j+1` from `M_{N_j}`; `k = 2j+2` from `M_{N_j+1}`). ∎

> **Corollary 1.9 (initial segments).** `{n : M_n ⊆ [0,K]} = [0, A(K))` where
> ```
> A(−1) = 0,   A(2j) = N_j = 3·2^j − 2,   A(2j+1) = N_j + 1 = 3·2^j − 1.
> ```

*Proof.* By Theorem 1.7(1), `M_n ⊆ [0,2j]` for every `n < N_j`; and every
`n ≥ N_j` has `M_n ∩ [2j+1, 2j+2] ≠ ∅` (`{2j+1}`, `{2j+2}`, or a copy containing
`Q_j` — and for `n ≥ N_{j+1}` induct). So `{n : M_n ⊆ [0,2j]} = [0, N_j)`, and
`{n : M_n ⊆ [0,2j+1]}` adds exactly the index `N_j`, whose monomial is `{2j+1}`.
Both sets are initial segments. ∎

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

This also **proves the "√t" reading**, which `nomos2d/RESULTS.md` reports as a
measurement (*"sweeping the entire ~1.5√t-cell extent"*). Exactly: at `t = 2^k`
the state is the frame plus `WNE@(0,1)` and `WNE@(m_k+1, 1)`, so the

> **reach at `t = 2^k` is exactly `m_k + 1 = 3·2^{⌊(k−1)/2⌋} − 1` (odd `k`) or
> `3·2^{(k−2)/2}` (even `k`)** — `1, 2, 3, 5, 6, 11, 12, 23, 24, 47, 48, 95, 96,
> 191, …` — engine-verified for `k = 0..14`,

and the crest is `3·2^{⌊(k−1)/2⌋} + O(1) = Θ(√t)` — precisely,
`|S_{2^k−1}| / 2^{k/2}` oscillates between `3/2 = 1.5` (even `k`) and
`3/√2 ≈ 2.12` (odd `k`), doubling every *second* power of two exactly because the
substitution of Theorem 1.7 consumes **two** new bits per doubling. (`nomos2d`'s
"≈ 1.5√t" is the lower envelope.)

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

*Max.* Order is what matters, and every order is available: `a_j = 0` is the
identity and there are infinitely many `j`, so any multiset of non-identity
operations can be applied in any order we like. Within a fixed multiset the
`+1`s should come first, by the exchange computation
`(+1 then double) = 2(F+1)+2 = 2F+4 > 2F+3 = (double then +1)`. So with
`d` doublings and `s` single steps, `ε_0 + s + 2d = w`, the value is
`2^d(ε_0+s+2) − 2 = 2^d(w+2−2d) − 2`. The ratio test `g(d+1)/g(d) ≥ 1 ⟺ w−2d ≥ 2`
puts the optimum at `d = ⌊w/2⌋`: `2^{w/2}·2 − 2` for even `w` and
`2^{(w−1)/2}·3 − 2` for odd `w`. Add 3.

*Min.* Each operation raises `F` by at least its weight cost:
`+a_j` costs `a_j` for `a_j ≤ 1`, and `2F+2` raises `F` by `F+2 ≥ 2 =` its cost.
Hence `F ≥ w`, with equality realised by `W = {1,3,5,…,2w−1}` (one bit per pair,
never a doubling). ∎

This also explains `JUBILEE-LAW.md`'s remark that *"the record-holders are the
nearly-all-ones times; the all-ones time `2^w − 1` is the maximum in its class for
odd `w` only."* For odd `w` the optimum forces `d = (w−1)/2` doublings and
`ε_0 + s = 1`, whose realisation `ε_0 = 1` is `W = [0, w−1]` — exactly the
all-ones time `2^w − 1`. For even `w` an all-ones `W` wastes bit 0 on the
initial value instead of on a pair; the optimum needs `ε_0 + s ∈ {0, 2}` and is
attained by several `W`, among them `W = [1, w]` (`t = 2^{w+1} − 2`, all ones
*except the last*) and `W = {0,1} ∪ [3,w]` — all of them **nearly**-all-ones
times, exactly as the measurement reported. *Certificate*: brute force over
`t < 2^18` gives maxima `4, 5, 7, 9, 13, 17, 25, 33, 49, 65, 97` for `w = 1..11`,
matching the formula, with the smallest maximiser `2^w − 1` for every odd `w` and
for no even `w ≥ 4` (`w = 2` ties: both `W = {0,1}` and `W = {1,2}` give `F = 2`).

### 1.5 A correction: the published min table is a box artefact *[established]*

`JUBILEE-LAW.md` (3) reports
`min{|S_t| : w(t)=w} = w+3` for `w ≤ 9`, "then 14, 19, 30, 53, 100, 195, 386, 769".

**That tail is an artefact of the search window `t < 2^17`, not a fact about the
Jubilee.** Seventeen bit positions offer only the singleton `{0}` and eight pairs
`P_0,…,P_7`, so at most `1 + 8 = 9` units of weight can be spent without filling a
pair — and a filled pair forces a doubling. For `w ≥ 10` the box *compels* the
expensive operation. Theorem 1.12 gives `min = w+3` for every `w`; the witnesses
for `w = 10,…,16` used here — `W = {1,3,…,2w−1}` — occupy 20, 22, 24, 26, 28,
30, 32 bits. (They are not the cheapest: `W = {0,1,3,5,…,2w−3}` also attains
`w+3` and needs only `2w−2` bits, so `w = 10` is already visible at `t < 2^18`.
What no 17-bit window can show is `w+3` for **any** `w ≥ 10`.)

*Certificate on the engine, at a scale the engine can reach.* Take `w = 8` and the
box `t < 2^13` (thirteen bit positions: `{0}` plus six pairs, so `1+6 = 7` cheap
units — one short of 8). Running `xnomos.step` from the Jubilee seed:

```
   min{ |S_t| : t < 2^13,  w(t) = 8 }   =  12  =  w + 4      (the box's answer)
   |S_43690|,  43690 = 0b1010101010101010,  w = 8   =  11  =  w + 3   (the truth)
```

The true minimiser needs 16 bits and is invisible to the box — the same failure
one octave down, demonstrated directly rather than through the closed form.

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
with `μ_{m_k} = 2^k`; by Theorem 1.7, `m_k = k` for `k ≤ 2` and thereafter
`m_{2j+1} = 3·2^j − 2`, `m_{2j+2} = 3·2^j − 1`, which is strictly increasing in
`k` (`0,1,2,4,5,10,11,22,23,46,47,…`). So the states at `t = 1, 2, 4, 8, …` are pairwise
distinct, so the orbit is infinite — and an eventually periodic orbit has
finitely many states. ∎

The same argument, through Theorem 2.3, gives **aperiodicity of the Odometer
`O⁻`** (§2.0 says which machine that is) — previously "no recurrence in 300 000
hashed steps; 179 survivors of a 3-stage escalation." For the other reading `O⁺`
aperiodicity stays a measurement; nothing here bears on it.

### 1.8 Why four: the general law, and a new family *[established]*

The reset law is not a fact about *this* specimen. Nothing in §1.2 used the
particular shape of the rule beyond "bit `n` flips when a fixed finite set of
lower bits are all set". So let `I ⊆ {1,2,3,…}` be finite and consider the
**lazy counter of profile `I`**:

```
    y_n(t+1) = y_n(t) ⊕ ∏_{i ∈ I} y_{n−i}(t),      y_{−1} ≡ y_{−2} ≡ … ≡ 1,  y(0)=0.
```

Lemma 1.4 applies verbatim, so `y_n(t) = f_{M_n}(t)` with, in integer form,

```
        μ_n = ( OR_{i ∈ I} μ_{n−i} ) + 1,          μ_{<0} = 0.
```

> ### **THEOREM 1.14 (the lazy-counter reset law).** If `1 ∈ I` then `(μ_n)` is
> **strictly increasing** and contains **every power of two exactly once**. Hence
> `wt(y(2^k)) = 1` for every `k ≥ 0`: every lazy counter with `1 ∈ I` resets.

*Proof.* Strictly increasing: `1 ∈ I` gives `μ_n ≥ μ_{n−1} + 1`. Every power of
two is hit: fix `k` and let `n` be least with `μ_n ≥ 2^k` (it exists, the sequence
being strictly increasing in ℤ, hence unbounded). Every earlier term is `< 2^k`,
so none has a bit at a position `≥ k`, so neither does their OR; therefore
`μ_n = (OR) + 1 ≤ (2^k − 1) + 1 = 2^k`. Together with `μ_n ≥ 2^k` this gives
`μ_n = 2^k`. Uniqueness is monotonicity. ∎

**That is the reason there are four laws.** *A carry sequence cannot step over a
power of two* — the `+1` is a carry, an OR of numbers below `2^k` stays below
`2^k`, so the first term to reach `2^k` lands on it exactly. Everything else in
the Jubilee — the block substitution, the `√t` crest, the pair recursion — is
decoration on that one sentence.

> **Corollary.** `I = {1}` gives `μ_n = n+1`, so
> `wt(y(t)) = #{n : n+1 ⊑ t} = 2^{w(t)} − 1`.

*[interpretation]* That is chapter one's **Pascal column** law, `2^{popcount(t)}`,
one frame apart: in the Jubilee's frame the depth-1 counter would read
`|S_t| = 3 + 2^{w(t)} − 1 = 2^{w(t)} + 2`, whereas `nomos2d`'s perpendicular
colonizer — a *different, one-law* specimen — reads `2^{popcount(t)}` on the nose.
What is a theorem is that the same counter word drives both. **The Pascal growers
and the Jubilee clock are the depth-1 and depth-2 members of one family**, and the
reset law of Theorem 1.14 holds in both — unbounded in the first, bounded in the
second.

*Certificate*: complete over all **32** profiles `I ⊆ [1,6]` with `1 ∈ I` (strict
monotonicity and one-hit-per-power-of-two over 3 000 terms each); the hypothesis
`1 ∈ I` is necessary — `I = {2}` gives `1,1,2,2,3,3,…`, hitting each power of two
twice; `I = {1}` reproduces `2^{popcount(t)} − 1` for all `t < 2^12`.

#### A prediction, then the engine

Moving the Jubilee's *precedent* guard `s` cells west — kind 2 becomes
`((−s,0), N, E)`, seeded with kind 2 at `c = 0,…,max(s,1)−1` — realises profile
`I = {1, s+1}` with a frame of `2 + max(s,1)` permanent laws (all blocked except
the kind-2 law at `c = max(s,1) − 1`, which is permanently *active* and supplies
the boundary condition). Theorem
1.14 therefore predicts, **before running anything**:

> `|S_{2^k}| = max(s,1) + 3`, constant in `k`, for every `s ≥ 0`.

Engine result (`xnomos.step`, `k = 1..12`):

| s | 0 | 1 (**the Jubilee**) | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| `\|S_{2^k}\|` | 4 | **4** | 5 | 6 | 7 | 8 |

Exact, at every `k = 1..12`, for every `s`. The Jubilee Code is `s = 1` of an infinite
family of jubilee clocks, and its celebrated **4** is `1 + 3` — one surviving
monomial on top of a three-law frame.

---

## 2. TARGET 2 — the four-law coincidence: **CLOSED, and it broke twice**

*The coincidence dissolves, and not in the way the question expected. There are
**two** machines in the repository under the name THE ODOMETER, because two files
use opposite vertical compasses. Exactly one of them has the four-law reset — and
that one **is the Jubilee Code**, at half speed, by an exact conjugacy exhibited
below. The other, the machine whose table `xamend2d/RESULTS.md` §11.2 actually
publishes, does **not** reset to four laws at every power of two.*

Certificates: `python3 proofs/t2_odometer.py --deep` — 15/15.
*(Repository under concurrent edit; all quotations re-checked at commit `42e40ca`.)*

### 2.0 Two Odometers *[established — read this first]*

`xamend2d/xa2d.py` sets `N = (0,+1)`, `S = (0,−1)`, `NW = (−1,+1)`, `SE = (1,−1)`.
The root `verify.py` and `nomos2d/` set `N = (0,−1)`, `S = (0,+1)`,
`NW = (−1,−1)`, `SE = (1,+1)`. The **rules** of a specimen are written in compass
letters, but the **seed** `A@(0,0), A@(1,0), B@(0,1)` is written in coordinates —
so flipping the compass without flipping the seed is *not* a symmetry. The string
`OEW>B NQR>AB` therefore names two genuinely different dynamical systems:

| | rules as offsets | where it appears | `\|S_{2^k}\|`, k = 1…17 |
|---|---|---|---|
| **O⁺** = `OEW>B NQR>AB` in `xa2d` letters | `((0,0),(1,0),(−1,0))`, `((0,1),(−1,1),(1,−1))` | `xamend2d/RESULTS.md` §11.2's table, `gallery.py`, the demo | `5,5,6,4,6,4,4,6,4,4,4,6,4,4,4,4,6` |
| **O⁻** = the same string in root letters (`OEW>B STP>AB` in `xa2d` letters) | `((0,0),(1,0),(−1,0))`, `((0,−1),(−1,−1),(1,1))` | root `verify.py`'s battery entry, `XFINDINGS.md` §3's crest list | `4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4` |

Both rows are from one engine (`xnomos.step`), one seed, `t ≤ 2^17`. And the two
**engines** agree: `xnomos.step` and `xa2d.step` run in lockstep on identical
constitutions with **0 divergences in 400 random 2-D systems × 6 steps**. The
clash is the offset dictionary, nothing else.

**Consequence for the target as posed.** Target 2 asked about a machine that
"returns to exactly four laws at every `t = 2^k` … with reach growing like
`(log t)²`". *No machine does both.* `O⁻` has the reset (`XFINDINGS.md` §3's crest
list `6, 9, 12, 18, 21, 36, 39, 72, 75` is `O⁻`'s, verbatim); `O⁺` has the
`(log t)²`-looking reach and does not reset. So the "coincidence" was a composite
of two different objects, and it dissolves twice over:

* on `O⁺` there is nothing to explain — it does **not** quiesce to four laws;
* on `O⁻` there is everything to explain, and the explanation is total:
  **`O⁻` is the Jubilee Code.** Sections 2.1–2.3 prove it.

Everything from here to §2.3 is about **`O⁻`** — the machine that carries the
four-law reset and that the field's own battery registers under that name. §2.4
returns to `O⁺` and says what must be repaired in the published record.

**Pre-registration Y4, scored honestly.** Y4 predicted (60 %) that the two
machines are *not* conjugate. On `O⁻` it is **REFUTED**: they are conjugate, and
the conjugacy is exact. On `O⁺` the prediction is **vacuous**, because `O⁺` never
had the property the coincidence was about. Y4's subordinate clause — that the
`4` is a fixed frame plus a weight-one counter word — **held**. The record stands
as written.

### 2.1 The Odometer's reduction *[established]*

Specimen (`xamend2d/`): two kinds, cross-amendment, three laws.
`A = (O, E, W) → {B}`, `B = (N, NW, SE) → {A, B}`, seed
`A@(0,0)`, `A@(1,0)`, `B@(0,1)`.

> **Which Odometer.** `O⁻` throughout §§2.1–2.3 (see §2.0): compass
> `O=(0,0)`, `E=(1,0)`, `W=(−1,0)`, `N=(0,−1)`, `S=(0,1)`, `NW=(−1,−1)`,
> `SE=(1,1)` — the reading of the root `verify.py` and `nomos2d/`, and the one
> that carries the four-law reset.

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
is shown empty in Lemma 2.2. `B@(0,1)` has exactly two possible authors — an active `A@(1,1)` (which writes
`B` at `p+W`) and an active `B@(−1,0)` (which writes `B` at `p+(1,1)`). Column
`−1` is empty, and `(1,1)` is never occupied, because laws appear in column 1
only at `p+(1,1)` for `p = (0,y)` with `y ≥ 1`, i.e. only at heights `≥ 2`. So
`B@(0,1)` is permanent too. ∎

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
blocked, and in one line: a buffer law sits at `z ∈ α_u + 1`, so `z−1 ∈ α_u ⊆ D_u`,
so `(0,z−1)` **is** occupied — and `B@(1,z)`'s vacancy clause asks precisely for
`¬occ((0,z−1))`. *The carry marker is blocked by the very digit that raised it.*
Meanwhile the column-0 `B` laws fire exactly as at the even tick, cancelling the
buffer they created. So column 1 empties, column 2 is never written, and
`D_{u+1} = D_u Δ (α_u+1)`. ∎

### 2.2 The map *[established — this is the answer to Target 2]*

> ### **THEOREM 2.3 (`O⁻` is the Jubilee).** Put `D = C + 1`. Then `O⁻`'s
> two-step map on its even-time states is **exactly** the Jubilee's
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

> ### **COROLLARY 2.4 (`O⁻`'s clock law — `XFINDINGS.md` §3's measurement, proved).**
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

The Jubilee and `O⁻` are **not** isomorphic as constitutions — one is own-kind
(out-degree 1), the other has out-degree 2 — and no conjugacy of *constitutions*
exists. What exists is a **common renormalisation**: both are implementations of
the single one-dimensional automaton

```
      K :  C ↦ C Δ { c+1 : c ∈ C, (c = 0 or c−1 ∈ C) }        (C ⊆ ℕ, 0 ∈ C)
```

and they differ only in *how they schedule the carry*.

* The **Jubilee** is a **one-phase** implementation. Own-kind targeting makes the
  update `𝔽₂`-linear-modulated-by-occupancy, and synchrony computes the whole
  carry set from the old state in a single tick. Its cost is that it needs three
  kinds — a three-law *frame*: two permanently blocked laws and one permanently
  active counter cell `WNE@(0,1)`, which is what supplies the boundary condition
  `y_{−1} = y_{−2} = 1`.
* **`O⁻`** is a **two-phase** implementation: *fetch* (materialise the
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

Both carry the same frame size, so both read 4. *The two binary counters of the
field are one counter with two clocks.*

And that also settles the target's fallback question — *"if they are genuinely
different, explain why 4 is forced in each"*. It is not forced at all: Theorem
1.14 and Corollary 1.15 exhibit machines in the same family whose reset constant
is 5, 6, 7, 8. What **is** forced, for every lazy counter with `1 ∈ I`, is the
`+1`: the counter word has weight exactly one at every power of two, and the rest
of the constant is bookkeeping.

### 2.4 What must be repaired in the published record *[established]*

*(Repository under concurrent edit; every quotation re-checked in the working
tree at commit `42e40ca`, where both appear verbatim.)*

**(i) `xamend2d/RESULTS.md` headline 9's four-law clause is false for the machine
it tabulates.** Headline 9 says of `OEW>B NQR>AB`: *"Card collapses to **four
laws** at every `t = 2^k` … reach ≈ 0.20 (log₂ t)², = 86 cells at `t = 2²⁰`."*
Read in `xamend2d`'s own compass, that specimen is `O⁺`, and

```
   |S_{2^k}|  for k = 0..17 :  4, 5, 5, 6, 4, 6, 4, 4, 6, 4, 4, 4, 6, 4, 4, 4, 4, 6
```

— six laws at `k = 3, 5, 8, 12, 17`, five at `k = 1, 2`. The counterexample is
**printed in the report's own table two pages later** (§11.2 records `card = 6` at
`t = 2^12`) and was not read. The *reach* half of headline 9 is fine: `O⁺`'s
heights at `k = 10, 12, 14, 15, 16, 17` are `20, 26, 38, 44, 47, 50`, exactly as
published, and §11.2's crest row `57, 75, 111, 138` and width row `2, 3, 2, 2`
reproduce entry for entry on `xnomos.step`. Whether that reach is genuinely
`Θ((log t)²)` is `xamend2d`'s own open item §11.3(7) and **stays open**; nothing
here bears on it. (The advertised fit quality is optimistic — the residual at
`k = 17` is `0.20·17² = 57.8` against a measured `50`, about +16 %, not "within
8 %".)

**(ii) `XFINDINGS.md` §3's Odometer paragraph mixes the two machines.** Its
crest list `6, 9, 12, 18, 21, 36, 39, 72, 75` and its "returns to **exactly four
laws** at every `t = 2^k` (14/14 verified)" are `O⁻`'s and are **correct — now a
theorem** (Corollary 2.4). Its "reach ≈ 0.20 (log₂ t)² out to `t = 2²⁰`" is
`O⁺`'s. The sentence that follows — *"Two machines found in different sectors by
different methods both quiesce to exactly four laws at every power of two
[interpretation: unexplained, and the most suggestive coincidence on the
board]"* — is the one this expedition was sent to explain, and the explanation is
that **there are not two machines**: the one that quiesces to four laws is the
Jubilee.

**(iii) The root `verify.py` battery entry is `O⁻`.** Its check ("THE ODOMETER:
|S| = 4 at every power of two") passes, and is now a theorem for every `k`, not a
measurement to `2^{12}`.

**(iv) Recommended repo fixes** — not applied here; this expedition does not edit
other expeditions' records:

1. Give the two compasses distinct names, or print the compass with every
   specimen string. The clash silently renames any specimen whose **seed** is not
   symmetric under `y ↦ −y`; the Odometer is such a specimen, and there may be
   others in the shared battery.
2. Re-label `xamend2d` headline 9: drop the four-law clause, or state it for
   `O⁻ = OEW>B STP>AB` (in `xa2d` letters), which is the machine that has it.
3. Split `XFINDINGS.md` §3's Odometer paragraph in two along the same line.
4. `gallery.py` §9b/9c and the demo pages (`docs/index.html`,
   `demo/nomodynamics.html`) inherit headline 9's text and need the same split.

> **The methodological point.** `XFINDINGS.md` §5 taught the field that a bounded
> search decides a box, not a question. This is the same lesson one level down:
> **a specimen name decides an object only together with its coordinate
> convention.** Two files, two compasses, one name — and a coincidence appeared
> between an object that had the property and an object that had the other
> property. Neither measurement was wrong. The *join* was.

---

## 3. TARGET 3 — the width-free speed cap: **REFUTED**

*The hardest target was not hard in the end, because the statement is false. The
**Single-Field Cap** — `|d| ≤ 2` under parity, `|d| ≤ 1` under OR at two channels,
"for any number of channels and at any width" — fails at three kinds under parity
and at three kinds under OR. The certified record at window 1 in the single-field
sector is `|d₀| = 128`, carried by **four** kinds. And the "tension" with the
Dilation Theorem was never a tension: it is an equivocation on the word* width.

Certificates: `python3 proofs/t3_verify.py` — 14/14, every specimen re-certified
through `xnomos.verify_glider` **and** `xnomos.classify` **and** an independent
primitivity test (no proper divisor of `(p,d)` works). Deeper machinery and the
complete censuses: `t3_core.py`, `t3_decide.py`, `t3_theory.py`, `t3_gensweep.py`
(§8 lists them; **35 209 width-unbounded decisions, 0 undecided**).

### 3.1 The counterexamples *[established — certified specimens]*

Single field means `T_k = K` for every kind: all kinds are written together, so
the code is a one-bit automaton with `n` channels. All rows below are `W = 1`,
single field, and `(p₀,d₀)` is the **minimal** period and the displacement across
it.

| name | kinds | rules | seed | res. | `(p₀,d₀)` |
|---|---|---|---|---|---|
| **QUINT-3/5** | 5 | `(0,−1,0) (0,−1,1) (0,1,−1) (0,1,0) (0,1,1)` | **one cell** | parity | **(5, 3)** |
| **TRIAD-4/4** | **3** | `(1,−1,0) (−1,1,−1) (−1,1,1)` | `{0..4}` | parity | **(4, 4)** |
| **QUINT-5/5** | 5 | `(0,−1,0) (0,−1,1) (0,1,0) (−1,1,−1) (−1,1,1)` | **one cell** | parity | (5, 5) |
| **SEPTET-7/7** | 5 | `(0,−1,0) (0,−1,1) (0,1,−1) (0,1,0) (−1,1,1)` | `{0,6}` | parity | (7, 7) |
| **HALFTONE-32** | 4 | `(0,−1,0) (0,1,−1) (0,1,0) (0,1,1)` | `{0,1,6,8}` | parity | (32, 32) |
| **ODOMETER-64** | 4 | `(0,−1,−1) (0,−1,0) (0,−1,1) (0,1,0)` | 7 cells, span 11 | parity | (64, −64) |
| **ODOMETER-128** | 4 | *same* | 14 cells, span 16 | parity | **(128, −128)** |
| **OR-ODOMETER-16** | **3** | `(0,−1,−1) (−1,1,0) (1,−1,0)` | 11 cells, span 15 | **or** | **(16, −16)** |

**QUINT-3/5 is the one that needs no argument at all.** Five kinds stacked in a
**single cell**; `Φ⁵ = σ³`; `gcd(5,3) = 1`, so `(5,3)` is primitive on arithmetic
alone — no minimality inference is required to read it. `|d| = 3 > 2`.
Its five ticks:

```
   .#....       {1}
   ##....       {0,1}
   ###...       {0,1,2}
   .#.#..       {1,3}
   ####..       {0,1,2,3}
   ....#.       {4}      = t = 0, shifted by +3
```

**TRIAD-4/4 is the sharpest**: three kinds, five cells, `Φ⁴ = σ⁴` while `Φ¹ ≠ σ¹`
and `Φ² ≠ σ²` — it lands squarely in the `n = 3` cell that the published table
gives as `|d| ≤ 2`, with `|d₀| = 4`.

**The Field-Count Threshold goes with it.** `XFINDINGS.md` §5 says *"the resource
that buys `|d| ≥ 3` is another 𝔽₂ **field**, not another kind"*. Every specimen
above is single-field — one field, `rank_{𝔽₂} = 1`. What buys `|d| ≥ 3` is a
third kind.

*What survives, and is now stronger.* The companion no-go is not only intact but
generalised: **`(4,3)` is impossible for every number of kinds**, not merely for
`n ≤ 4` — a complete decision over all 512 parity classes (§3.2), with no bound
on the pattern span. So the original observation *"four kinds in one field cannot
reach (4,3) at any width"* was right, and is now a theorem about the whole sector.

### 3.2 What replaces the cap: the sector is **finite** *[established]*

The reason "for any number of channels" could be asserted at all is real, and it
is better than the cap it was used to support.

> **Theorem A (Type Reduction, `W = 1`, single field).** A `W = 1` law is live
> only for four guard pairs, and each is a statement about the two neighbours
> `λ = [i−1 ∈ S]`, `ρ = [i+1 ∈ S]` of the cell it stands on:
> `(0,−1)` fires iff `λ=0`; `(0,+1)` iff `ρ=0`; `(−1,+1)` iff `λ=1, ρ=0`;
> `(+1,−1)` iff `ρ=1, λ=0`. Hence a cell's **entire** emission depends only on its
> **type**:
>
> | type | `(λ,ρ)` | emits |
> |---|---|---|
> | isolated | (0,0) | `u` |
> | left end | (0,1) | `v` |
> | right end | (1,0) | `w` |
> | **interior** | (1,1) | **`0`** — Gridlock, as a type |
>
> with `u,v,w ∈ 𝔽₂³` indexed by the offset `c ∈ {−1,0,1}`. So the whole dynamics
> is the triple `(u,v,w)`: **exactly 512 parity dynamics and 343 OR dynamics**,
> every one realised by a constitution with **at most six kinds**.

*Consequence.* "For any number of channels" is a **finite** question, and it can
be *decided* rather than sampled. `xspeed`'s 33 630 constitutions with `n ≤ 5`
reach 485 of the 512 parity classes and 335 of the 343 OR classes; the 27 + 8
classes they miss are exactly those that need six kinds. *The census was a large
sample of a small set, and nobody knew the set was small.*

> **Theorem B (front speed).** For any window `W`, any resolution:
> `max Φ(S) ≤ max S + W` and `min Φ(S) ≥ min S − W`. Hence **`|d| ≤ p·W`** for
> every glider — and at `W = 1`, `|d| ≤ p`.
>
> *Proof.* A cell `j` is toggled only by an active law at `j − c_k`, and that law
> stands on an occupied cell, so `j ≤ max S + W`. ∎

**This is the only width-free bound in the sector, and it is attained — by two
laws, from any seed at all.**

> **CONVEYOR.** `A = (0,−1,0)`, `B = (0,1,1)`, single field. Then
> `Φ(S) = σ(S)` **identically**, for every finite code `S` and in **both**
> resolutions.
>
> *Proof.* An emission reaches `j` from the kind-`A` law at `j` (needs `j ∈ S`,
> `j−1 ∉ S`) and from the kind-`B` law at `j−1` (needs `j−1 ∈ S`, `j ∉ S`); the
> two are mutually exclusive, so parity ≡ OR here and
> `N(j) = [j ∈ S] ⊕ [j−1 ∈ S]`. Then `s'_j = s_j ⊕ N(j) = s_{j−1}`. ∎
>
> *"While I stand and my left is vacant, repeal me; while I stand and my right is
> vacant, enact my successor."* The rear evaporates, the front paves: **every
> statute book in this universe marches at speed 1 forever.** Certificate: 2 000
> random codes × 2 resolutions, 0 exceptions.

### 3.3 The corrected census *[measured — complete decisions, no pattern-width bound, every number of kinds]*

Decided by a column-subshift generator decider carrying **no** bound on the
pattern span, augmented with one flag per prime `q | gcd(p,d)` so that it answers
*"is `(p,d)` a **minimal**-period generator?"* rather than *"does `Φ^p = σ^d`?"*.
Brute-force validated against a 13-cell box: 1 260 questions, 19 positives, 0 misses.

**Parity, `W = 1`, single field, all 512 classes, `p₀ ≤ 6`:**
realisable `(1,1) (2,1) (2,2) (3,1) (3,2) (3,3) (4,1) (4,2) (4,4) (5,2) (5,3)
(5,5) (6,2) (6,6)`; impossible at any span and any number of kinds
`(4,3) (5,1) (5,4) (6,1) (6,3) (6,4) (6,5)`.

**OR, `W = 1`, single field, all 343 classes, `p₀ ≤ 6`:** realisable
`(1,1) (2,1) (2,2) (3,3) (4,4)` and **nothing else** — reduced speeds `{1, 1/2}`
only. *The OR sector is far more rigid in speed than parity; this is a fifth
parity/OR split, and the sharpest structural one yet.*

**By number of kinds** (complete, `p₀ ≤ 6`, any span):

| kinds | parity max `\|d₀\|` | OR max `\|d₀\|` |
|---|---|---|
| ≤ 2 | **2** ✓ (confirms the published cap) | **1** ✓ (confirms it) |
| ≤ 3 | **4** ✗ | **4** ✗ |
| any | ≥ 128 (certified) | ≥ 16 (certified) |

Beyond `p₀ = 6`, certified `|d₀|` values at `W = 1`: parity
**3, 4, 5, 6, 7, 8, 15, 16, 18, 32, 38, 64, 128**; OR **3, 4, 8, 16**. Against
code span, in one four-kind universe:

```
   span    4    6    8   10   12   14   16   18   20
   |d₀|    8    8   16   32   64   64  128   64  128
```

— powers of two, growing with the span.

### 3.4 The diagnosis, and the dilation tension *[established]*

**One unchecked sentence.** `xspeed/RESULTS.md` §4 reads:

> *"`(2,2), (3,3), (4,4), (5,5)` also solve `Φᵖ = σᵈ` but are iterates of the
> period-1 TANDEM glider, not minimal-period objects."*

The inference is invalid: *a `(1,1)` glider existing somewhere in a universe does
not make every `(p,p)` solution in that universe its iterate* — the `(p,p)`
solution is a **different pattern**. The four-kind universe
`{(−1,1,−1),(1,−1,0),(0,1,1),(1,−1,1)}` has both a `(1,1)` glider (seed `{0,1,2}`)
and, from seed `{0,1}`, a genuinely minimal period-3 glider with `d₀ = 3`. The
diagonal entries `(3,3)`, `(4,4)`, `(5,5)`, `(6,6)` are **already in `xspeed`'s
own Table A** in the *realisable* column. **The data was right; only the reading
was wrong.** At `n ≤ 2` the inference happens to be correct; it first bites at
three kinds, which is exactly where the cap was asserted.

> **The dual of the width correction.** `XFINDINGS.md` §5 warned that a
> coprime-only sweep is blind to `Φ⁴ = σ²`. The **opposite** blindness — reading
> the non-coprime diagonal as automatically imprimitive — was not guarded, and
> that is precisely where the counterexamples live. *Minimal period must be
> decided, not inferred from a witness.*

**The dilation "tension" is an equivocation.** Three candidate escapes were
tested and **all three are false**:

* *"dilation does not preserve the single-field sector"* — **false** (this was my
  pre-registered guess Y5, and it is wrong): dilation rescales offsets and leaves
  the target sets alone, so `T_k = K` stays `T_k = K`. Certified: ODOMETER-64
  dilated by `r = 2, 3` is single-field at `W = 2, 3` with `(p,d) = (64, −128)`
  and `(64, −192)`.
* *"the dilated object is not a glider of the same kind"* — **false**: `i ↦ r·i`
  is injective, so the generator maps `(p₀,d₀) ↦ (p₀, r·d₀)` exactly.
* *"the `W = 2` three-kind `|d| = 5` example is not single-field"* — **false**:
  its targets are `{0,1,2}` for all three kinds.

> **The resolution.** The corpus uses "width" for two different things: the
> **window** `W` (the offset radius of the rules) and the **pattern span** (what
> the subshift decider removes the bound on — `sft.py`'s docstring says "with NO
> bound on the width of the pattern"). The Single-Field Cap is a statement at
> **fixed window `W = 1`** over patterns of unbounded **span**; the Dilation
> Theorem moves the **window**. *The two statements never met.* `README.md` and
> `XFINDINGS.md` §5 should read **"at any pattern span, at window 1"**.

And with the true `W = 1` record at `|d₀| = 128`, dilation now supplies
`|d₀| ≥ 128r` at window `r` — ≥ 256 at `W = 2`, ≥ 384 at `W = 3` (`r = 2,3`
certified). That retires the puzzle `xspeed` §15 posed — *"at `W = 2` with three
kinds displacements reach at least 5 > 2W, so why does the cap not scale?"* —
**there was no cap to scale.**

### 3.5 What stays conjectural, and the obstruction *[original proposal]*

> **Conjecture T3-U.** In the single-field sector at `W = 1`, `sup |d₀| = ∞`:
> there is **no** width-free cap on displacement per minimal period, in either
> resolution. The only universal bound is Theorem B's `|d| ≤ p·W`, attained at
> both ends — by CONVEYOR at `p₀ = 1` and by ODOMETER-128 at `p₀ = 128`.

*Evidence*: the certified ladder `8, 16, 32, 64, 128` growing with the code span
inside one four-kind universe; the values are `2^k` and elsewhere `2^k − 1` — the
signature of orders of polynomials over `𝔽₂`, the same arithmetic that produced
the Sunset Parliament's exact periods 15, 63, 341.

**The obstruction, named.** Theorem C (front trichotomy) shows that when the
front advances at *every* step, a glider has `d = p`, i.e. it is a **finite
periodic point of `Ψ = σ^{−1}∘Φ`**, and `d₀ = p₀` is its minimal `Ψ`-period. So a
cap `|d₀| ≤ C` would assert that *every finite periodic point of each of 226
explicitly given cellular automata has period ≤ C* — a CA periodic-point
question, for which no monovariant is available. Two concrete walls:

1. **Decision cost.** The column subshift for `(q,q)` has state space `2^{4q}`;
   the decider returns CAP from `q = 8` up. The `q = 32, 64, 128` objects were
   found by simulation, not decided.
2. **Nonlinearity is forced, and Gridlock forces it.** Writing the emission out,
   `E_c(i) = s_i[u_c + (u_c+w_c)s_{i−1} + (u_c+v_c)s_{i+1} + (u_c+v_c+w_c)s_{i−1}s_{i+1}]`.
   `Φ` is `𝔽₂`-linear **only** when `u = v = w = 0`, i.e. only when it is trivial:
   the interior type's silence — **Gridlock** — is exactly the quadratic term. So
   the polynomial-order machinery that closed the Sunset Parliament cannot be
   applied verbatim, even though the observed periods look exactly like its
   output.

*The sharpest next step in this sector*: find the algebraic conjugacy that
explains the `2^k` minimal periods of ODOMETER-64/128. It would settle T3-U, and
— given §1 — it is hard not to suspect it lands on the same carry automaton.

