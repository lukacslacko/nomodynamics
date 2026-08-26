# Expedition Y-A — the citation sector

*Chapter three of nomodynamics. Scored against `CITATION.md` (frozen
2026-08-26, before this expedition ran). Honesty tiers throughout:
**[established]** = proved here or cited from a proved result;
**[measured]** = machine-checked over a stated box, with the box stated;
**[interpretation]** = reading of an established fact;
**[original proposal]** = conjecture or construction sketch, not completed.*

---

## 0. Pre-registration

*Written before the first census run, from armchair reading of the definition
in `CITATION.md` §2 and of `xnomos.enabled`. Kept verbatim whatever happens.
Where an expectation was already close to a proof when written, that is said so
here, so that a later "confirmed" cannot be read as a lucky guess.*

**P1 — Citation is inert at one kind.** With `|K| = 1`, "a law of kind 0 stands
at `i+a`" and "some law stands at `i+a`" are the same predicate, so the whole
citation alphabet collapses. The smallest sector where citation can do anything
is `n = 2`. (Believed near-certain; a one-line argument.)

**P2 — The plenum theorem (Y1) holds but nearly empties out.** The full plenum
is frozen because every exception clause, whatever it names, is satisfied by a
cell that carries every kind. But the *sharp* criterion will not be "the code is
full": it will be "every cell of the region carries the **exception image**
`E(C) = {h_k : h_k ≠ any}`". Expected consequence: Y1 is technically true and
practically vacuous, because `E(C)` can contain kinds that the dynamics never
enacts. Confidence high.

**P3 — Gridlock's epitaph is a condition on the citation digraph.** I expect a
clean iff: *every solid region is interior-frozen* ⟺ for every kind `k`,
`h_k ∈ {any, k, g_k}`. Confidence ≈ 0.75 that exactly this condition comes out.

**P4 — The bulk is a 0-dimensional dynamical system.** In a region where every
cell carries the same kind-set `U`, offsets are invisible, so the interior
should evolve by a map `β : 2^K → 2^K` depending only on the guards and target
sets. Prediction: this map is exact on homogeneous ring codes for *every*
modulus, giving certified oscillators inside solid code with periods up to
`2^n`, and `β(K) = K` always (which is Y1). Confidence high.

**P5 — Y2 (Out-Degree Law survives) holds.** The monovariant argument only ever
uses "the only laws that can toggle kind `t` at cell `j` are placed laws of
kinds `k` with `t ∈ T_k` at `j − c_k`", which never mentions the guard. I
therefore expect Y2 to survive **verbatim**, and I expect the serious search to
find nothing. Confidence 0.9. *I flag in advance that the charter's stated
reason ("guards only thin the actor set") is **wrong** — citation can make
strictly more laws active than occupancy does; the right reason is that the
proof never reads the guard at all.*

**P6 — Citation buys the unconditionally active law, and that is the whole
mechanism.** Under occupancy no law is ever active regardless of context (the
exception cell, if occupied, always blocks). Under citation, naming a kind that
is never enacted makes the exception clause vacuous. Prediction: this single
device explains Gridlock's death, and it will let citation constitutions realise
**𝔽₂-linear cellular automata** — hence Sierpinski growth on ℤ with *own-kind*
targeting, which chapter one proved impossible in its sector. Confidence 0.8.

**P7 — Y5 (a replicator) falls out of P6.** If the linearisation works, `Φ` is
`I + N` over 𝔽₂ and Frobenius gives `Φ^{2^j} = I + N^{2^j}`: at `t = 2^j` every
finite seed stands beside a disjoint copy of itself. Prediction: a replicator
exists, is provable rather than found, and replicates *every* seed. Confidence
0.7 conditional on P6.

**P8 — Y3 (computational substrate).** The citation guard is literally
`p ∧ ¬q` on kind-fields, and parity resolution is XOR, so I expect a full gate
inventory and, beyond the charter's prediction, an exact simulation of arbitrary
1-D cellular automata at O(1) steps per CA step. Confidence 0.6 for the full CA
simulation, 0.85 for the gate inventory. Turing-universality on ℤ needs a
gate-laying front that outruns the computation; I expect to sketch it and
**not** complete it.

**P9 — Census shape.** Over the complete `n = 2`, `W = 1` citation box I expect:
a large majority extinct/fixed; gliders present but rarer *per constitution*
than in the occupancy corner (citation more often kills the guard than helps
it); and a new, sizeable class the earlier chapters could not produce —
codes that are solid and still moving. I expect the residue of unresolved
trajectories to be small (< 1%).

**P10 — Y4 (linear growth) is a triviality.** `|S_t| ≤ n·(span_0 + 2Wt + 1)` in
1-D holds for *any* constitution, citation or not, because the light cone grows
by `W` per side per step and a cell holds at most `n` laws. Confidence: this is
a proof, not a prediction. What is *not* trivial is whether the rate `2Wn` is
attained; I expect it is.

**P11 — Self-citation is degenerate at offset 0.** `g_k = k` with `a_k = 0` is a
tautology (the law stands at its own cell) and `h_k = k` with `b_k = 0` is a
contradiction. So the interesting self-citation is at nonzero offset, and I
expect self-citation to behave qualitatively differently from cross-citation:
self-citation cannot make a law unconditionally active in a region that contains
its own kind, cross-citation can.

**Anti-predictions (things I expect NOT to find).** No glider at out-degree ≤ 1
(P5). No super-linear growth in 1-D (P10). No violation of Single Author,
Dead Letter (OR), Anchor (own-kind), Path-Sum Confinement, or the Balance
cohort criterion — all of these read only the target sets, never the guard.

---

## 1. Headline

**Citation is not a relabelling: it is the door out of the whole occupancy
world.** Under occupancy guards no law is ever *unconditionally* active — its
exception cell, once occupied, blocks it, and that single fact is chapter one's
Gridlock. Citation lets a law name a kind that is never enacted, and the
exception clause goes vacuous. From that one device:

| | |
|---|---|
| **Gridlock's epitaph** | Gridlock survives for a constitution **iff `h_k ∈ {any, k, g_k}` for every kind** — an exact condition on the citation digraph. The surviving fraction is `((3n+1)/(n+1)²)^n`: 100 % at one kind, **60.49 %** at two, **24.41 %** at three, 7.31 % at four. |
| **The Plenum Theorem (Y1)** | **Holds**, and sharpens: a region is frozen as soon as every cell carries the **exception image** `E(C) = {h_k : h_k ≠ any}`. But it also nearly empties out — `E(C)` may contain kinds the dynamics can never enact, so "total law" is now a property the *constitution* chooses, not one a full code enjoys. |
| **The bulk map** | Inside a region whose cells all carry the same kind-set `U`, the offsets are invisible and the interior evolves by a map `β : 2^K → 2^K`. It is exact on homogeneous ring codes at **every** modulus. `β(K) = K` **is** Y1. Complete census: max bulk period `2` at `n = 2`, **`6 = 2³−2`** at `n = 3`. |
| **The Out-Degree Law (Y2)** | **Survives verbatim** — proof audited line by line and re-verified. 51.0 M complete classifications at out-degree ≤ 1 and 80,000 deep random runs: **zero gliders**. *But the charter's stated reason is wrong* (see §3.3). |
| **Linearisation** | A tautologous guard makes the step map exactly `F ↦ (I+N)F` over 𝔽₂. **Every additive CA of that shape lives in the citation sector** — including Sierpinski growth on ℤ with **own-kind** targeting, out-degree 1, window 1: chapter one's tamest corner, which chapter one proved contains only colonizers and blinkers. |
| **A replicator (Y5)** | `(I+N)^{2^j} = I + N^{2^j}`, so at every `t = 2^j` past the seed's span **every finite code** stands beside a disjoint copy of itself. Proved, not found; universal, not special. |
| **The substrate (Y3)** | Gate inventory complete (BUFFER, NOT, AND-NOT, AND, XOR, OR, FAN-OUT, all one step, all truth tables machine-checked) and, beyond the charter's prediction, **all 256 elementary cellular automata are simulated exactly** by citation constitutions with ≤ 15 kinds and window 1, at two nomodynamics steps per CA step. Rule 110 runs inside nomodynamics. |
| **A counter on the line** | **THE LEDGER** — three laws, two kinds, window 1, on ℤ: bounded population, unbounded reach, aperiodic, and `S(4^j) = {A@0,B@0,B@2} ⊔ {A@(2^j+2),B@(2^j+2)}` **exactly** — card 5 and reach `√t + 3` at every power of four. The first 1-D binary counter in the field, and it fixes prediction Y6's normal form (*head ⊔ doubling marker*), while refuting the claim that the reset number 4 is forced. |
| **New fauna** | **LACUNA** — a hole running at the speed of light through a *completely occupied* code, occupancy never changing. **THE SIX SESSIONS** — a solid block whose interior cycles with period 6 while its **surface is frozen**: the exact inversion of "all dynamics is surface dynamics". **THE WRIT / PROCESSION** — a signal, and a full ring that revolves by one cell per step. **THE CONVERSION FRONT** — one solid phase eating another. |
| **A casualty nobody flagged** | **Cryptic Unipotency** (`xtheory` Thm 6) and the whole 𝔽₂-linear front layer of chapters one and two **fail under citation**: they assume the guard is a function of occupancy alone, so that freezing occupancy freezes the guard mask. Under citation the guard is a function of the evolving kind-fields and the step map is a **degree-3 polynomial** map, not an occupancy-modulated linear one. |

The risk clause of `CITATION.md` §5 is defeated on both counts: citation is not
inert (Gridlock is a theorem of the occupancy world and is false here; the
sector is CA-complete cell-for-cell), and it is not structureless (six theorems
below, two of them exact iff-criteria, and one complete census with no box).

---

## 2. The object, and the one thing citation buys

Write `Û = U ∪ {any}` for a nonempty kind-set `U`. A placed law `(i,k)` is
active iff

> `[a law of kind g_k stands at i+a_k]` **and** `[no law of kind h_k stands at i+b_k]`,

with `any` reading "some law of any kind". Two immediate structural facts.

**Lemma 0 (citation is inert at one kind).** With `|K| = 1`, `occ(j)` and "a
kind-0 law stands at `j`" are the same predicate, so all four guard choices give
the same dynamics. *[established; battery **T1**, complete: all 216 one-kind constitutions —
27 rules × 2 target sets × 4 guard pairs]* The smallest sector where citation can do
anything is `n = 2`. (Pre-registration **P1** confirmed.)

**Lemma 1 (self-citation at offset zero is degenerate).** `g_k = k` with
`a_k = 0` is a tautology — the law stands at its own cell — so the precedent
clause is vacuous. `h_k = k` with `b_k = 0` is a contradiction, so the law is a
dead letter. *[established; battery **T6**]* (Pre-registration **P11**
confirmed. In a written code, a section that cites *itself at its own location*
either says nothing or contradicts itself.)

**Lemma 2 (the phantom, and what occupancy cannot do).** Call `φ` a **phantom**
of an orbit if no kind-`φ` law is ever placed. Then `h_k = φ` makes the
exception clause vacuously true. By contrast, under **occupancy** guards no law
is ever unconditionally active: `(i,k)` is inactive whenever `i+b_k` is
occupied, and `i+b_k` can always be occupied (if `b_k = 0` it is occupied by the
law itself). *[established]*

> **This is the whole mechanism of chapter three.** Everything below —
> Gridlock's death, the living bulk, the linear sector, the replicator, the
> machine — is a consequence of *a law that can act regardless of its
> neighbourhood*, which is exactly what a named exception buys and an anonymous
> one cannot.

---

## 3. The survival audit

Every chapter-one and chapter-two theorem, with the verdict, the load-bearing
hypothesis, and the check. A proof audit of the originals (`xamend1d`,
`xtheory`, `xspeed`, `glider-question`) was run line by line before the
searches; the two properties that must be kept apart are

* **(D)** *a placed law occupies its cell* — definitional, **true** under citation;
* **(G)** *an occupied cell blocks any vacancy clause pointing at it* — **false** under citation.

Nearly every "occupancy" step in the earlier proofs is (D), not (G). That is why
the audit comes out mostly clean.

| theorem | verdict under citation | load-bearing step | check |
|---|---|---|---|
| **Gridlock** | **DIES** — replaced by Theorem G below | pure (G) | §3.1 |
| **Single Author** (in-degree ≤ 1 ⟹ parity ≡ OR) | **survives verbatim** | counts *potential* authors `{(j−c_k,k) : t ∈ T_k}`, guard-free | **S1** |
| **Dead Letter** (fixed ⟺ every law blocked) | **survives verbatim under OR, fails under parity** — exactly as in chapter two | a criterion on the *resolution*, not the guard | **S2** |
| **Balance / cohort structure** | **survives verbatim** | parity of the toggle multiset; guard-free | **S3** |
| **Anchor** (own-kind, ℤ) | **survives verbatim** — its own hypothesis audit already allowed *any* guard predicate, kind guards included | toggles of kind `t` land only at `t`'s offset | **S4** |
| **Out-Degree Law** | **survives verbatim** (Y2) | Lemmas S/R: only *placed* laws toggle; guard never read | §3.3, **S7** |
| **Tropical Speed Law**, Zero-Cycle, Unique-Cycle | **survive verbatim** | same monovariant substrate | §3.3 |
| **Path-Sum Confinement**, Zero-Sum No-Go, displacement law | **survive verbatim** — the theorem's own hypothesis line says "the guard … otherwise arbitrary" | support containment | **S5** |
| **α ≤ 1 ⟺ out-degree ≤ 1**; linear growth in 1-D (Y4) | **survives verbatim**, and the bound is **tight** | light cone + `n` laws per cell | **S5**, **S5'** |
| **Twin-Kind Lemma / Even-Support Law (Thm K)** | **survive verbatim** — the active set is left abstract | `|T_k ∩ U|` even | (audit) |
| **Dilation Theorem** | **survives with a one-word amendment**: "reads occupancy" → "reads cell content" | needs the guard to read exactly the two offset cells | **S6** |
| **Supersession No-Go** | **survives citation of the guard**; would **die** under citation of the supersession *trigger* | F1/F2 are facts about the *effect* rule reading `occ` of the target cell | (audit) |
| **Cryptic Unipotency** (`xtheory` Thm 6) and the 𝔽₂-linear front layer | **FAIL** | assume the guard is a function of `occ` alone | §3.4 |
| **Cycle-Length Law** (`𝔽₂[y]/(y^L−1)` local iff `L = 2^a`) | **survives only where it applies** — its hypothesis "frozen occupancy" must be strengthened to "frozen cited fields" | same linearisation | §3.4 |
| **`rings` Lemma 0′** (15 of the 27 `W=1` rules are unconditional dead letters) | **FAILS**, and every count derived from it must be recomputed | `b=0` and `a=b` are only contradictions for occupancy | Lemma 1, Lemma 2 |

### 3.1 The plenum, and Gridlock's exact epitaph

Write `E(C) = {h_k : k ∈ K, h_k ≠ any}` for the **exception image** of the
citation digraph.

> **Theorem P (Plenum; prediction Y1).** *Let `R` be a region every cell of
> which is nonempty and carries every kind of `E(C)`. Then every placed law
> `(i,k)` whose exception cell `i+b_k` lies in `R` is blocked.*
>
> *Proof.* If `h_k = any`, the cell `i+b_k ∈ R` is nonempty, so the vacancy
> clause fails. If `h_k = j ≠ any`, then `j ∈ E(C)` stands at `i+b_k ∈ R`, so
> the vacancy clause fails. ∎
>
> **Corollary (Y1 as stated).** A *saturated* region — every kind at every cell
> — is frozen: `E(C) ⊆ K`, so the hypothesis holds. In bulk-map language,
> `β(K) = K` for every constitution and either resolution. *[established;
> battery **T2** (20,000 random constitutions, `n ≤ 5`), **T2'** for the sharp
> form]*

**Y1 is therefore CONFIRMED — and its content collapses**, exactly as
pre-registered in **P2**. Chapter one's Gridlock was a statement about *states*:
any occupied region is inert, and "occupied" is cheap. Theorem P is a statement
about a *constitution-dependent* set `E(C)`, which can contain kinds that no
reachable state ever carries. *Total law is still total stasis, but "total" is
now whatever the constitution's exception clauses happen to name — including
provisions that were never enacted.*

The exact death certificate. Call a solid region **uniform** if every cell
carries the same kind-set `U` (the coordinator's motivating example — a solid
block of ten kind-0 laws — is uniform with `U = {0}`).

> **Theorem G (Gridlock's epitaph).** *The following are equivalent.*
> 1. *Every uniform solid region is interior-frozen.*
> 2. *`A(U) = ∅` for every nonempty `U ⊆ K`, where `A(U) = {k ∈ U : g_k ∈ Û and h_k ∉ Û}`.*
> 3. ***For every kind `k`, `h_k ∈ {any, k, g_k}`.***
>
> *Proof.* (1)⇔(2): the interior of a uniform solid region is exactly a
> `U`-plenum, and by Theorem B below its active set is `A(U)`.
> (2)⇒(3): take `U = {k} ∪ ({g_k} if g_k ≠ any)`. Then `g_k ∈ Û` and `k ∈ U`, so
> `A(U) = ∅` forces `h_k ∈ Û = U ∪ {any}`, i.e. `h_k ∈ {any, k, g_k}`.
> (3)⇒(2): for `k ∈ U`, `k ∈ Û` and `any ∈ Û`, and `g_k ∈ Û` is required for
> activity; in each of the three cases `h_k ∈ Û`, so `k ∉ A(U)`. ∎
>
> *[established; battery **T3**: closed form ≡ brute force over all `U`, 30,000
> random constitutions with `n ≤ 5`]*

**Pre-registration P3 confirmed exactly.** Read aloud: *a full code freezes only
if every provision's exception clause refers to nothing in particular, to
itself, or to its own precedent. Name a third party and the interior wakes up.*

Counting: per kind, the pairs `(g,h)` with `h ∈ {any, k, g}` number `3n+1` out of
`(n+1)²`, so

> **Corollary.** The fraction of `n`-kind citation constitutions for which
> Gridlock survives is exactly `((3n+1)/(n+1)²)^n` — `1`, `49/81 = 60.4938 %`,
> `125/512 = 24.4141 %`, `28561/390625 = 7.3116 %`, `1.7342 %`, `0.3399 %` for
> `n = 1…6`. *[established; battery **T3'** verifies the count by complete
> enumeration at `n = 1,2,3`]*

*(A remark on the stronger reading. If "solid" is allowed to be heterogeneous —
different cells carrying different kinds — then interior-freezing for **all**
solid regions holds iff every kind is either occupancy-blocked (`h_k = any`) or
a universal dead letter — battery **T7** checks this exhaustively over all
`W = 1` rules, guards and kinds at `n = 2` and `n = 3` against every three-cell
neighbourhood: 1,782 cases, 0 counterexamples.
Theorem G is the uniform statement, which is the one that matches the bulk map
and the motivating example.)*

### 3.2 The bulk map — a new invariant, and a habitat

> **Theorem B (the bulk map).** *In a region every cell of which carries exactly
> the kind-set `U`, the active kinds are `A(U) = {k ∈ U : g_k ∈ Û, h_k ∉ Û}` —
> independently of the offsets `(a,b,c)` — and the region's next kind-set is*
> ```
> β(U) = U Δ ( ⊕_{k∈A(U)} 1_{T_k} )   [parity]        β(U) = U Δ ( ⋃_{k∈A(U)} T_k )   [OR]
> ```
> *On the ring ℤ/m the homogeneous code `S_U = {(i,k) : i ∈ ℤ/m, k ∈ U}` satisfies
> `Φ(S_U) = S_{β(U)}` **exactly, for every modulus `m ≥ 1`**. On ℤ the same holds
> in the interior: if a code agrees with the `U`-plenum on `[i−R, i+R]` then cell
> `i` carries `β^t(U)` for all `t ≤ R/W`.*
>
> *Proof.* Every cell of a `U`-plenum has the same neighbourhood, so the guard
> of a kind-`k` law is the same at every cell and equals `[g_k ∈ Û] ∧ [h_k ∉ Û]`.
> Cell `j` receives, for each `k ∈ A(U)`, one toggle of every `t ∈ T_k` from the
> (active) kind-`k` law at `j − c_k`. Summing by parity gives `β`. ∎
>
> *[established; battery **T4**: 2,000 random constitutions × 7 moduli × 2
> resolutions, bulk map ≡ ring dynamics]*

`β` depends **only** on the guards and target sets, never on the offsets and
never on the modulus. So the census of bulk behaviour is *finite and complete*,
with no box caveat at all: there are exactly `((n+1)²·2^n)^n` distinct bulk
data.

> **THE BULK CENSUS — complete, `n = 2` and `n = 3`, both resolutions**
>
> | | `n = 2` (1,296 constitutions) | `n = 3` (2,097,152 constitutions) |
> |---|---|---|
> | Gridlock survives | 784 = **60.4938 %** | 512,000 = **24.4141 %** |
> | living bulk | 512 = **39.5062 %** | 1,585,152 = **75.5859 %** |
> | max bulk period 1 | 1,292 (99.6914 %) | 1,904,120 (90.7955 %) |
> | 2 | 4 (0.3086 %) | 186,068 (8.8724 %) |
> | 3 | — | 4,516 (0.2153 %) |
> | 4 | — | 2,208 (0.1053 %) |
> | 5 | — | 192 (0.0092 %) |
> | 6 | — | 48 (0.0023 %) |
>
> (OR figures are the same for the Gridlock split and nearly the same for the
> periods: 1,900,634 / 192,266 / 1,228 / 2,928 / 48 / 48 at `n = 3`.)
>
> `β` fixes both `∅` and `K`, so a bulk cycle lives in the other `2^n − 2`
> subsets and **`period ≤ 2^n − 2`**. That bound is **attained** at `n = 2`
> (period 2) and `n = 3` (period **6**). *[established for the bound; complete
> census for `n ≤ 3`; battery **T5**]* At `n = 4, 5, 6` a random search
> (`python3 bulk.py sample`; 400 k / 200 k / 200 k random bulk data, recorded in
> `data/bulk_sample.json`) found maxima **11, 14, 16** against the bounds
> 14, 30, 62 — **[measured, sampled]**; whether `2^n − 2` is attained for
> `n ≥ 4` is open, and the gap widens fast with `n`.

Pre-registration **P4** confirmed in full.

### 3.3 Y2 — the Out-Degree Law survives, and the charter's reason for it is wrong

The charter predicted Y2 "because guards only thin the actor set". **That
premise is false**: citation can make strictly *more* laws active than occupancy
does — that is precisely Gridlock's death, where a solid block goes from one
active law to ten. The correct reason is stronger and was pre-registered as
**P5**: the proof never reads the guard at all.

The monovariant argument rests on two lemmas:

* **Lemma S.** `supp_m(n+1) ⊆ supp_m(n) ∪ ⋃_{k : m ∈ T_k} (supp_k(n) + c_k)`.
* **Lemma R.** A toggle of kind `m` at cell `j` requires an **active** law of
  some kind `k` with `m ∈ T_k` at `j − c_k`.

Lemma S uses only *(D)*: an emitting law is a placed law. Lemma R uses "active
⟹ placed", i.e. `active ⊆ placed` — true for **any** activity predicate.
Neither mentions `occ`, monotonicity, or the exception clause. The weights
`w_k ≤ w_{t(k)} + c_k`, the monovariant `Ψ(n) = min_m(α_m(n) + w_m)`, the tight
cycle argument and the Bellman–Ford feasibility criterion are all statements
about the amendment digraph `D[C]`, which **citation does not touch** (it
changes `(g,h)`, not `T`). Therefore:

> **Y2 — CONFIRMED.** *The Out-Degree Law, the Tropical Speed Law, the
> Zero-Cycle and Unique-Cycle theorems, Path-Sum Confinement, the Zero-Sum
> No-Go, the displacement law, the Twin-Kind Lemma and the Even-Support Law all
> survive citation verbatim.* *[established, by proof audit]*

The searches agree, and they were run hard because the program's own width
correction demands it:

* **Complete**, over the whole census box (§6.1): all 531,441 constitutions with
  out-degree ≤ 1 (that is `(27·3·9)²`), × 48 seeds × 2 resolutions =
  **51,018,336 certified classifications**, budgets 200 steps / card 200 /
  span 120, then the entire growing-or-unresolved residue re-run at
  **1500 steps / card 1200 / span 1500**. **Zero gliders.**
* **Deep random**, `n = 2…4`, single-target, seeds up to 6 laws over 5 cells,
  600 steps / card 400 / span 400: **80,000 runs, zero gliders** (battery
  **S7**).

Both are box statements and are labelled as such; the *theorem* is the audit.
For comparison the same census found **13,300 / 14,036** certified glider runs
(parity / OR) at out-degree 2. The threshold is exactly where chapter two put
it, and citation does not move it.

### 3.4 The casualty: the 𝔽₂-linear layer

`xtheory` Theorem 6 (*Cryptic Unipotency*) and the front theory of
`glider-question` §3 both begin: *"fix the occupancy trajectory `O_n`; then each
kind's field evolves linearly, with mask `g_k(i) = O_n(i+a_k)(1 − O_n(i+b_k))`;
kinds couple only through `occ`."* Under citation the mask is
`g_k(i) = x(i+a_k, g_k)·(1 − x(i+b_k, h_k))` — a function of the very fields
being evolved. Freezing occupancy no longer freezes the mask, `I + N` is not a
linear operator, and the nilpotency/power-of-two conclusion has no proof.

> **The citation step map is a polynomial map of degree ≤ 3 over
> `𝔽₂^{K×ℤ}`**: `x(i,k)·x(i+a_k, g_k)·(1 − x(i+b_k, h_k))`. Occupancy
> nomodynamics is the special case where the two guard factors are functions of
> `⋁_k x(·,k)`. *[established]* **This is the largest structural casualty after
> Gridlock and `CITATION.md` does not flag it.**

And then the twist. The general theory loses linearity — but *citation can buy
it back exactly*, which occupancy cannot (Lemma 2):

> **Theorem L (Unconditional Law / Linearisation).** *Let `φ` be a phantom kind.
> If every non-phantom kind `k` has `a_k = 0`, `g_k = k`, and `h_k = φ`, then
> every placed law is active at every time, and the step map is the 𝔽₂-linear
> map*
> ```
>     F ↦ (I + N) F ,        N_{t,k} = x^{c_k} · [ t ∈ T_k ] ,
> ```
> *a Laurent-polynomial matrix over `𝔽₂`. Conversely, no occupancy constitution
> has an unconditionally active law. Hence **every additive cellular automaton of
> the form `I + N` is realised in the citation sector**, on `n` channels plus one
> phantom kind, at window `W = max|c_k|`.* *[established; Lemma 2 and direct
> computation]*

Pre-registration **P6** confirmed.

---

## 4. The linear sector, and a replicator (Y5)

Theorem L hands citation the whole additive world. Two consequences, both
provable and both impossible in chapter one's sector.

### 4.1 THE PASCAL CLAUSE — Sierpinski on ℤ, own-kind, out-degree 1

```
0 : (0,0,1)  cite(0,1)  ->{0}        "while a section-0 law stands at my own cell
                                       — always, I am one — and no section-1 law
                                       stands here — never, section 1 is never
                                       enacted — enact section 0 to my right"
1 : anything                          THE PHANTOM: never placed
seed: one kind-0 law
```

The guard is a tautology, so `F ← F ⊕ (F ≪ 1)`: the additive rule 60.

```
 t=0 |A................|  card=  1
 t=1 |AA...............|  card=  2
 t=2 |A.A..............|  card=  2
 t=3 |AAAA.............|  card=  4
 t=4 |A...A............|  card=  2
 t=5 |AA..AA...........|  card=  4
 t=6 |A.A.A.A..........|  card=  4
 t=7 |AAAAAAAA.........|  card=  8
 t=8 |A.......A........|  card=  2      |S_t| = 2^popcount(t)
```

This is **own-kind targeting, out-degree 1, window 1, on ℤ** — the exactly
solvable sector of chapter one, whose entire 1-D fauna was colonizers, sunset
blinkers, welds and refraction. One named exception clause puts a Sierpinski
gasket in it. *[established; battery **F3**: `|S_t| = 2^popcount(t)` for
`t ≤ 256`, cross-checked on `xnomos` to `t ≤ 64`]*

It also shows how little of the earlier tameness was about *own-kind*: the
Anchor Theorem still holds here (nothing travels — `c_0 = +1 > 0`, the trailing
law is permanent), `α ≤ 1` still holds (`|S_t| ≤ t+1`), and yet the sector is no
longer solvable in chapter one's sense.

### 4.2 THE COPY — a universal replicator (Y5)

Over `𝔽₂`, `I` and `N` commute and the Frobenius map is additive, so
`(I+N)^{2^j} = I + N^{2^j}`. In the Pascal clause `N = x`, hence

> **Theorem R (universal replication).** *In the Pascal clause, for every finite
> code `S₀` and every `2^j > span(S₀)`,*
> ```
>     S_{2^j}  =  S₀  ⊔  (S₀ + 2^j)
> ```
> *— two disjoint translates of the seed. Every code replicates, at every
> sufficiently large power of two, forever.* *[established; battery **F4**: 200
> random seeds, all valid `j`; `xnomos` cross-check]*

**Prediction Y5 — CONFIRMED**, and in the strongest available form: the
replicator is not a special organism but a property of the *constitution*, and
it is proved rather than found. Pre-registration **P7** confirmed. (The general
`I+N` gives `S_{2^j} = S₀ Δ N^{2^j}S₀`; disjointness needs the displacement
`2^j·c` to clear the span, and multi-channel `N` replicates the whole tuple of
fields at once.)

This is also the missing explanation of a chapter-one/two coincidence, offered
at the **[interpretation]** tier: `card(S_{2^j}) = 2·card(S₀)` is the Fredkin
signature, and it is exactly what a "return to a fixed small number of laws at
every power of two" looks like from outside. See §9, Y6, for what the Odometer
actually does.

---

## 5. The fauna of the living bulk

Chapter one's slogan was *all dynamics is surface dynamics*. Under citation the
interior is a habitat. Every specimen below is produced by `specimens.py`,
certified by `cite.py`, and re-verified by the repository's independent
`xnomos.py` engine (battery **F1–F7**).

### 5.1 GRIDLOCK DIES (the coordinator's observation, restated exactly)

A solid block of ten kind-0 laws, kind `0 = (0,1,1)`, under the two guards:

```
occupancy   h = any     active laws:  1        citation  h = kind 1   active laws: 10
   |AAAAAAAAAA....|                              |AAAAAAAAAA....|
   |AAAAAAAAAAA...|                              |A.........A...|
   |AAAAAAAAAAAA..|                              |AA........AA..|
   |AAAAAAAAAAAAA.|                              |A.A.......A.A.|
```

On the left the block grows at its surface and its interior never changes; on
the right every one of the ten laws fires at once and the block turns into a
Pascal triangle — because with `h_0 = 1` and kind 1 never enacted, kind 0 is
unconditionally active and the step map is `F ↦ F ⊕ (F≪1)` (Theorem L).
`h_0 = 1 ∉ {any, 0, g_0} = {any, 0}`, so Theorem G says Gridlock is dead for
this constitution — and it is.

### 5.2 LACUNA — a hole travelling through a *completely occupied* code

```
0 : (0,-1,0)  cite(any,0) ->{0}    "while no section-0 law stands one to my left,
                                     repeal section 0 here"
1 : (0, 0,0)  cite(any,0) ->{0}    "while no section-0 law stands here,
                                     enact section 0 here"
seed on Z/m : every cell carries sections 0 and 1, except one cell which is
              missing section 0
```

```
ring Z/13, unrolled   (# = both sections stand,  o = the LACUNA)
  t=0 |o############|
  t=1 |#o###########|
  t=2 |##o##########|
  t=3 |###o#########|
  t=4 |####o########|
  t=5 |#####o#######|
  ...   Phi = rot_(+1) exactly; period m
```

Section 1 refills the gap; section 0, one cell along and now un-blocked, repeals
itself. **Every cell of the ring is occupied at every step** — this is a solid,
complete code in perpetual motion, and it moves at the light-cone maximum
(`r = 1 ≤ p·W = 1`, so it passes the transport test that X-C's retraction
demands: it is not a barber pole). Verified at `m ∈ {5,7,8,11,13,16,21,32}` on
both engines, occupancy constant throughout. *[established; battery **F1**]*

On ℤ the same code is a **LACUNA GUN**: the left end of a finite block emits a
hole every two steps and each runs off to the right, so the block is eaten from
within while its outline never moves.

```
  t=0 |###o############|  card=31
  t=1 |o###o###########|  card=30
  t=2 |#o###o##########|  card=30
  t=3 |o#o###o#########|  card=29
  t=4 |#o#o###o########|  card=29
  t=5 |o#o#o###o#######|  card=28
```

The smallest travelling defect found in the complete `n = 2` hunt (§6.3);
2 kinds, window 1, and no chapter-one or chapter-two analogue, because in both
of those a solid ring is frozen.

### 5.3 THE SIX SESSIONS — a bulk oscillator, with a frozen surface

```
0 : (-1,1,0)  cite(any,1) ->{0,1}
1 : (-1,1,0)  cite(any,2) ->{1,2}
2 : (-1,1,0)  cite(any,0) ->{0,1,2}
seed: a solid block of kind-0 laws
```

Bulk period `6 = 2³ − 2`, the maximum possible at three kinds. Cell contents as
hex kind-sets (`1={0} 2={1} 4={2} 3={0,1} 5={0,2} 6={1,2} 7={0,1,2}`):

```
  t=0 |1111111111111|  card=13
  t=1 |1222222222222|  card=13
  t=2 |1444444444444|  card=13
  t=3 |1333333333333|  card=25
  t=4 |1555555555556|  card=25
  t=5 |1666666666627|  card=25
  t=6 |1111111111725|  card=16
```

The interior runs through `{0} → {1} → {2} → {0,1} → {0,2} → {1,2} → {0}` while
**the left edge never changes**: the exact inversion of chapter one's slogan.
On ℤ/m the whole ring is bulk and the period is exactly 6 for every
`m = 2…13`, on both engines. *[established; battery **F2**]*

### 5.4 THE WRIT and PROCESSION — a wire, and a full ring that revolves

```
0 = Z    the signal          cite(3,3)          never active: pure data
1 = G    the relay  (0,0,1)  cite(0,3) ->{0}    copy Z one cell right
2 = E    the eraser (0,0,0)  cite(0,3) ->{0}    clear Z here
3 = phi  the phantom, never enacted
```

`Z(i)' = Z(i) ⊕ Z(i) ⊕ Z(i−1) = Z(i−1)`: a shift register. The relay and the
eraser stand at every cell and **nobody amends them**, so the wire is entrenched
and the signal is ordinary law.

```
  t=0 |::X:::::::::::::|  card=33      : = the entrenched relay+eraser pair
  t=1 |:::X::::::::::::|  card=33      X = the signal
  t=2 |::::X:::::::::::|  card=33
  t=3 |:::::X::::::::::|  card=33
  ...  speed exactly 1, through fully occupied code
```

*[established; battery **F5**: `Z' = Z ≪ 1` exactly, on 400 random signal
patterns over 24 cells]*

**PROCESSION.** Put the relay and eraser at every cell of ℤ/m and one signal
anywhere: `Φ = rot_(+1)` **exactly**, on a ring every cell of which is occupied
at every step. The code revolves; its occupancy never changes. Chapter one's
ring rotors were retracted as barber poles; this one is inside the light cone
and carries a genuine mark around the ring. Verified `m = 3…19`, both engines.
*[established; battery **F6**]*

### 5.5 THE CONVERSION FRONT — one solid phase eating another

```
0 : (-1,-1,-1)  cite(any,0) ->{0,1}
1 : (-1,-1,-1)  cite(any,1) ->{0,1}
```

`{0}` and `{1}` are both fixed points of the bulk map, so each solid region is
frozen on its own. At the seam each side's exception clause is satisfied by the
other side, and the boundary advances one cell per step:

```
  t=0 |aaaaaaaaaabbbbbbbbbb|
  t=1 |aaaaaaaaabbbbbbbbbbb|
  t=2 |aaaaaaaabbbbbbbbbbbb|
  t=3 |aaaaaaabbbbbbbbbbbbb|
  t=4 |aaaaaabbbbbbbbbbbbbb|
```

Occupancy never changes; only the *doctrine* does. Chapter one had one
conversion wave, at speed 2/3, on empty ground and anchored at a point defect.
This one runs at the speed of light **through written code**, and it converts.
*[established; battery **F7**: 14 steps, seam speed exactly 1, occupancy
constant]*

### 5.6 THE LEDGER — a binary counter on the line

Found in the census residue (§6.4), which is what a residue is for.

```
0 : (-1,-1,0)  cite(1,0) ->{1}
1 : ( 0, 0,1)  cite(1,0) ->{0,1}
seed: sections 0 and 1 at cell 0, section 1 at cell 2      (three laws)
```

```
   t= 0 |...#.B............|      # = both sections
   t= 1 |...#.B#...........|      A = section 0 only
   t= 2 |...#.BB...........|      B = section 1 only
   t= 3 |...#.BA#..........|
   t= 4 |...#.B.#..........|
   t= 5 |...#.B##..........|
   t= 6 |...#.BB#..........|
   t= 7 |...#.BAB..........|
   t= 8 |...#.B.B#.........|
   t= 9 |...#.B#BB.........|
   t=10 |...#.BBBA#........|
   t=11 |...#.BAA.#........|
```

Bounded population (card ∈ [3, 139] over 400,000 fully hashed steps, no exact
recurrence), unbounded reach — hence **aperiodic**. And the reset is exact:

> **The Ledger's law.** *For every `j ≥ 1`,*
> ```
>     S(4^j)  =  { A@0, B@0, B@2 }  ⊔  { A@(2^j+2), B@(2^j+2) }
> ```
> *— a fixed three-law head plus a two-law marker at distance `2^j + 2`. Hence
> `card(S(4^j)) = 5` and `reach(S(4^j)) = √t + 3`, exactly, at every power of
> four.* *[established by computation; verified `j = 1…11`, i.e. to
> `t = 4,194,304`; battery **F8**, **F9**]*

This is the **first binary counter of nomodynamics in one dimension**. The
Jubilee Code (chapter one, 2-D, ~26 laws) and the Odometer (chapter two, 2-D,
3 laws) are both planar; the Ledger is three laws and two kinds on ℤ. The
citation guard is doing all the work, and the control is one line long: **strip
the citations from exactly these rules and this seed — replace `cite(1,0)` by
`cite(any,any)` — and the code is a dead letter at `t = 0`**, fixed with zero
active laws. Same offsets, same targets, same seed; anonymous guard, nothing
happens; named guard, a counter that is still running at `t = 4,194,304`.
See §9, Y6, for what it says about the "four-law reset".

---

## 6. The census

### 6.1 The box, stated exactly

> **THE CITATION BOX.** `n = 2` kinds; dimension 1 on ℤ; window `W = 1`
> (offsets in `{−1,0,1}`); every rule `(a,b,c)` — 27; every target set
> `T ⊆ {0,1}` — 4; every citation pair `(g,h) ∈ ({0,1} ∪ {any})²` — 9. So
> **972 kinds per slot and `972² = 944,784` constitutions**, of which
> `108² = 11,664` are the pure-occupancy corner of chapters one and two.
> Seeds: every nonempty code of span ≤ 3 with the leftmost cell occupied —
> **48 seeds**. Both resolutions.
>
> **Stage 1** (complete): 200 steps, card ≤ 200, span ≤ 120 →
> **90,699,264 weighted classifications**.
> **Stage 2**: every growing-or-unresolved run re-run at 1500 steps,
> card ≤ 1200, span ≤ 1500 — **1,790,842 representative runs**.

Nothing here is a statement about "citation universes" in general. It is a
statement about that box, and every number below carries it. In particular
**the seed span cap of 3 is the binding constraint**: chapter two's MIRROR
gliders have spans up to 616 and would be invisible here even at unbounded
time.

### 6.2 The symmetry quotient, and why it is exact

Let `G = ⟨μ⟩ × S_n` where `μ` is the mirror `(a,b,c) ↦ (−a,−b,−c)` (with cells
reflected) and `S_n` relabels kinds (acting on `g`, `h` and `T` as well). For
`σ ∈ G` the map `S ↦ σ(S)` conjugates the dynamics: `Φ_{σC}(σS) = σ(Φ_C(S))`
for both resolutions, because the guard and the toggle rule are equivariant.

> **Lemma S (soundness of the quotient).** *The seed set — all nonempty codes
> inside 3 cells, normalised so the leftmost cell is occupied — is closed under
> `G`: relabelling permutes kinds within a cell, and the mirror reflects
> `{0,1,2}` to itself and is then re-normalised by a translation. Hence for
> every `σ ∈ G` the multiset of classifications of `σC` over the seed set equals
> that of `C`, and summing over orbit representatives weighted by orbit size is
> exactly the sum over the box.* *[established; battery **C2** checks the
> conclusion directly on 120 random orbits]*

`|G| = 4` here. The enumeration produced **237,006 orbit representatives** whose
orbit sizes sum to exactly **944,784** — the arithmetic check that nothing was
double-counted or dropped.

### 6.3 Stage 1 — the complete class distribution

Weighted runs, 45,349,632 per resolution:

| class | parity | | OR | |
|---|---:|---:|---:|---:|
| EXTINCT | 308,094 | 0.679 % | 325,646 | 0.718 % |
| FIXED | 27,880,408 | 61.479 % | 27,956,342 | 61.646 % |
| BALANCED | 6,122,364 | 13.500 % | 5,786,820 | 12.760 % |
| CYCLE | 7,489,936 | 16.516 % | 7,651,568 | 16.872 % |
| **GLIDER** | **13,300** | **0.029 %** | **14,036** | **0.031 %** |
| GROWING | 3,136,788 | 6.917 % | 3,210,014 | 7.078 % |
| UNRESOLVED | 398,742 | 0.879 % | 405,206 | 0.894 % |

Split by the maximum out-degree of the constitution (parity; OR is the same to
within a percent):

| class | out-degree 0 | out-degree 1 | out-degree 2 |
|---|---:|---:|---:|
| EXTINCT | 0 | 111,384 | 196,710 |
| FIXED | 1,351,584 | 13,702,336 | 12,826,488 |
| BALANCED | 1,482,768 | 3,072,784 | 1,566,812 |
| CYCLE | 0 | 4,426,930 | 3,063,006 |
| **GLIDER** | **0** | **0** | **13,300** |
| GROWING | 0 | 1,108,392 | 2,028,396 |
| UNRESOLVED | 0 | 252,990 | 145,752 |

Split by whether Gridlock survives (Theorem G), parity:

| class | gridlocked (571,536 constitutions) | living bulk (373,248) |
|---|---:|---:|
| EXTINCT | 152,586 | 155,508 |
| FIXED | 18,379,962 | 9,500,446 |
| BALANCED | 3,182,834 | 2,939,530 |
| CYCLE | 3,974,400 | 3,515,536 |
| GLIDER | 6,932 | 6,368 |
| GROWING | 1,698,614 | 1,438,174 |
| UNRESOLVED | **38,400** | **360,342** |

The one strongly non-uniform row is UNRESOLVED, and the right comparison is a
*rate*, since the two columns cover different numbers of constitutions:
38,400 / 27,433,728 = **0.140 %** for gridlocked universes against
360,342 / 17,915,904 = **2.012 %** for living-bulk ones. A living bulk makes a
trajectory **14.4× harder to resolve** at fixed budget — the census-level
signature of the new habitat.

**Cycle periods** (parity, weighted, periods capped at 64):
2 (5,855,368), 4 (1,342,412), 8 (181,468), **3** (52,240), 6 (27,732),
16 (11,152), 32 (5,460), **9** (3,028), **5** (3,004), 12 (1,824), 64 (1,624),
**7** (1,396), 18 (1,188), 10, 14, 24, **42**, 28, **54**, 48, … The distinct
periods realised in the box, over both resolutions and capped at 64 by the
recording, are
`{2,3,4,5,6,7,8,9,10,12,14,16,18,20,24,28,32,34,36,40,42,46,48,54,56,58,60,64}`
— parity contributes 5, 34 and 46; OR contributes 58 and 60.
*[measured, this box]*

**Gliders.** 6,834 glider records over 951 representative constitutions; every
one re-certified from its glider **core** over three full periods by battery
**C3**, which reads `data/gliders1.txt` and re-runs all 6,834. *The word "core"
is load-bearing, and I got it wrong first:* a glider seed often has a
pre-period, so `verify_glider(seed, …)` fails on a perfectly good glider. The
first pass of this analysis reported hundreds of "unverified" gliders before I
noticed the classifier's own `t₀` was being thrown away. Corrected, and the
correct routine is now `cite.certify_glider`. Weighted `(resolution, p, d)`
spectrum:

`(or,1,−1) 6412 · (parity,1,−1) 6156 · (parity,1,+1) 4536 · (or,1,+1) 4536 ·
(or,4,−1) 1400 · (parity,5,−2) 752 · (or,5,−2) 744 · (parity,11,−2) 720 ·
(or,2,+1) 544 · (parity,8,−2) 528 · (parity,2,+1) 464 · (or,14,−7) 320 ·
(or,2,−1) 80 · (parity,10,−2) 72 · (parity,2,−1) 48 · (parity,6,+1) 24`

Speeds realised: `1, 1/2, 2/5, 1/4, 1/5, 2/11, 1/6`. Glider core spans run to
**15**. **[measured, this box — a narrow-glider statement; read no
"impossible" into it.]**

> **A pre-registration refuted.** **P9** predicted that gliders would be *rarer
> per constitution* in the citation sector than in the occupancy corner. They
> are not. Weighted over the box, **0.377 %** of the 11,664 pure-occupancy
> constitutions bear a glider on some span-≤3 seed, against **0.403 %** of the
> 933,120 citing ones. Citation neither helps nor hinders ballistic motion — as
> the guard-free proofs of §3.3 in fact predict. Kept as found.

### 6.4 Stage 2 — the residue, deepened

All 1,790,842 growing-or-unresolved representative runs were re-run with the
budget raised 7.5× in time and 12.5× in span. Counts here are **per orbit
representative** (not weighted by orbit size, unlike §6.3):

| | count | share of residue |
|---|---:|---:|
| GROWING (still) | 748,107 | 41.8 % |
| BALANCED | 566,863 | 31.7 % |
| CYCLE | 245,656 | 13.7 % |
| UNRESOLVED (still) | 222,219 | 12.4 % |
| FIXED | 7,997 | 0.4 % |
| **GLIDER** | **0** | **0 %** |

**Zero new gliders.** In particular the residue contains no wide glider of the
MIRROR type inside `span ≤ 1500`, `p ≤ 1500` — which is the honest form of the
statement, and it is why the deepening was run at all.

**The interesting residue.** The 222,219 still-unresolved runs come from 10,805
distinct constitutions, of which **94.0 % have a living bulk** (Theorem G fails)
against 39.5 % in the box at large — the sharpest single correlate of Gridlock's
death anywhere in this census. They are not runaway growers: on a 150-run sample
at `t = 1500` the median card is **20** and the median span **51**, with a
measured growth exponent `d log card / d log t` of median **0.65** over
`t ∈ [400, 1500]`. In other words the residue is dominated by **slow bounded
machines with creeping reach** — cryptids of exactly the Odometer's type. A
sweep of 1,500 of them to `t = 4000` isolated **802** with card ≤ 24 and span
< 300; the cleanest is **THE LEDGER** (§5.6). *[measured]*

### 6.5 Two hunts inside solid code

Both hunts are **complete over the citation box** (237,006 representatives, all
`(g,h)`, all rules, all target sets), on rings, and both use the light-cone test
`0 < |r| ≤ p·W` so that a hit is transport and not a barber pole.

> **The defect hunt.** For every constitution and every `β`-fixed nonempty phase
> `U`, lay the `U`-plenum on ℤ/11 and ℤ/13, spoil one cell to each other
> kind-set, and ask whether the spoilt cell travels. **7,496,602 ring runs;
> 11,664 travelling defects; 2,712 distinct constitutions.** Rotation spectrum
> `(p, r)`: `(1,−1) 4008 · (1,+1) 2760 · (4,+3) 1464 · (5,+3) 1428 ·
> (4,−3) 900 · (5,−3) 852 · (2,−1) 72 · (2,+1) 48 · (6,−1) 48 · (6,+1) 36 ·
> (16,−16) 36 · (8,−1) 4 · (2,±2) 8` — speeds `1, 3/4, 3/5, 1/2, 1/6, 1/8`.
> **3,200** of the hits sit on a *proper* phase `U ⊊ K`, i.e. on a code that is
> solid but not saturated. *[measured, complete over the box; the minimal
> specimen is LACUNA, §5.2]*
>
> **The boundary hunt.** For every constitution with two distinct `β`-fixed
> phases, lay half of ℤ/12 in each. **2,238,660 runs: 237,202 oscillating
> seams and 444 travelling seams** — conversion fronts inside written code.
> Speeds `1` and `5/6` (a `(p,r) = (36,−30)` family). *[measured, complete over
> the box]*


---

## 7. The statute machine (prediction Y3)

### 7.1 The gate inventory

A citation guard is literally `p ∧ ¬q` on kind-fields at fixed offsets, and
parity resolution XORs the toggles of all authors of a slot. So **one
nomodynamics step applies to every target field an arbitrary XOR of AND-NOT
terms over the neighbourhood.** Gate laws are placed at a cell, cite two data
kinds and write into an output kind; the whole inventory is one step deep:

```
BUFFER  R = P            gate(P, phi)                       00->0 01->0 10->1 11->1
NOT     R = ~P           gate(SELF@0, phi) + gate(P, phi)   00->1 01->1 10->0 11->0
ANDNOT  R = P & ~Q       gate(P, Q)                         00->0 01->0 10->1 11->0
AND     R = P & Q        gate(P, phi) + gate(P, Q)          00->0 01->0 10->0 11->1
XOR     R = P ^ Q        gate(P, phi) + gate(Q, phi)        00->0 01->1 10->1 11->0
OR      R = P | Q        gate(Q, phi) + gate(P, Q)          00->0 01->1 10->1 11->1
FANOUT  R1 = R2 = P      gate(P, phi) -> {R1, R2}           (multi-target)
```

All seven truth tables are machine-checked (battery **M1**). `phi` is the
phantom (Lemma 2); `SELF@0` is self-citation at offset 0, the constant `1`
(Lemma 1). Fan-out is exactly the multi-target device of chapter two, so
**out-degree — which chapter two identified as the price of motion — is also
the price of fan-out.**

### 7.2 Every elementary cellular automaton, exactly

The gates give algebraic degree ≤ 2 per step (a guard reads two cells), so a
degree-3 rule needs one scratch field and two steps. The obstacle is that a gate
has only two clauses, and gating it on a clock phase would consume one of them.
The fix uses the substrate itself:

> **The self-citing clock.** One kind `CK` with `a = 0`, `g = CK`, `h = φ` is
> unconditionally active (Lemma 1). Place it at every cell and let its target
> set be *the entire gate alphabet*. Then every gate kind is toggled on and off
> at every cell at every step: the phase-1 gates are **placed** only on even
> steps and the phase-2 gates only on odd steps. Being present *is* the phase,
> so both guard clauses stay free for data.

Compilation (`circuit.py`): put the CA state in kind `S`, a scratch product in
kind `U`.
*Phase 1:* `U(i) ^= S(i−1)·S(i)`, realised as `x ⊕ (x ∧ ¬y)`.
*Phase 2:* `S(i) ^= f(S(i−1),S(i),S(i+1)) ⊕ S(i)`, with the cubic monomial
supplied by `U(i)·S(i+1)`, and `U` cleared by re-applying the same product
(`S` is unchanged since phase 1, so the same value is XORed back).

> **Theorem M.** *For every one of the 256 elementary cellular automata there is
> a citation constitution with **at most 15 kinds** and **window `W = 1`** such
> that on ℤ/m, for every `m ≥ 3`, two nomodynamics steps restricted to the `S`
> field are exactly one CA step, and the machine kinds are invariant.*
> *[established by construction; battery **M2**: all 256 rules, ℤ/11, 16 CA
> steps, 2 random seeds each, exact; **M3**: Rule 110 for 60 CA steps on ℤ/23
> and 20 more on the independent `xnomos` engine; **M4**: the clock stands at
> every cell and the phases alternate for 80 steps; and a separate check at the
> smallest moduli, `m = 3…8` × 8 rules × 3 seeds × 12 CA steps, 0 failures]*
> Kinds needed: min 8, max 15, mean 12.0.

Rule 110 inside nomodynamics, from a single 1 on ℤ/30 (13 kinds, `W = 1`):

```
    ............................#.
    ...........................##.
    ..........................###.
    .........................##.#.
    ........................#####.
    .......................##...#.
    ......................###..##.
    .....................##.#.###.
    ....................#######.#.
    ...................##.....###.
    ..................###....##.#.
    .................##.#...#####.
```

**Prediction Y3 — CONFIRMED and exceeded.** The charter asked for a gate-level
inventory (≈ 0.7) and gave ≈ 0.35 to a completed universality construction. The
inventory is complete, and the substrate is shown to be **CA-complete
cell-for-cell at the same window** — strictly more than a gate list, strictly
less than Turing universality on ℤ.

### 7.3 The separation, and what is *not* proved

> **Corollary (citation is not a relabelling of chapter two).** Every occupancy
> constitution satisfies Gridlock: its uniform solid regions are interior-frozen
> (`h_k = any` for all `k`, so Theorem G applies). The Pascal clause is a
> citation constitution with a uniform solid region that is not interior-frozen.
> Since "uniform solid regions are interior-frozen" is invariant under the only
> symmetries of the object (mirror and kind relabelling), no occupancy
> constitution is isomorphic to it. *[established]* Chapter three's risk clause
> — "citation is inert, every phenomenon a relabelling on a larger alphabet" —
> is therefore closed, and closed by a theorem rather than by a specimen.

**What is not proved.** Turing universality on ℤ. A code is finite, so the gate
laws can only be laid over a finite region, and a machine needs unbounded tape.
The route is visible and is offered at the **[original proposal]** tier: the
simulated CA's light cone advances at `1/2` cell per nomodynamics step (two
steps per CA step), while a *constructor front* laying gate kinds advances at
1 cell per step, so a front can outrun the computation it feeds and lay tape
(and Rule 110's period-14 background) ahead of it forever. Building that front —
and proving it never disturbs the region behind it — was not attempted here.
Ring simulation gives space-bounded computation only; on a ring every orbit is
eventually periodic, so no undecidability follows from it.

---

## 8. The institutional reading

Chapter three's referent is the most concrete of the three: statutes cite each
other by section number, and a citation is a *name*, not a proximity. Four
things the mathematics actually says, and nothing beyond them.

**1. A complete code is not a frozen code.** Chapter one's Gridlock said that
where the law is dense, nothing can happen: every provision's exception clause
is satisfied by its crowded neighbourhood, so the interior of a written code is
inert and all change happens at the frontier. That is an artefact of anonymity.
The moment a provision says *"unless section 9 is in force"* rather than
*"unless something is in force nearby"*, a fully written code can act
everywhere at once. Theorem G makes the condition exact and, read as law, it is
almost a slogan: **a full code freezes only if every exception clause refers to
nothing in particular, to the provision itself, or to its own precedent. One
reference to a third party anywhere in the code and the interior wakes up.** The
fraction of two-kind constitutions that stay frozen is 60 %; at three kinds it
is 24 %; at six, 0.34 %. *Codification does not produce stasis; anonymity did.*

**2. What "total law" would have to mean.** The plenum theorem survives (Y1):
saturate a region and it freezes. But the saturation that matters is by the
**exception image** — the set of provisions that are *cited as exceptions* —
and a constitution can name, as an exception, a provision that is never enacted.
So the frozen state is no longer something a busy legislature drifts into; it is
a target the drafters would have to hit deliberately, including by enacting
provisions whose only function is to be cited. *Total law is still total stasis.
It has stopped being cheap.*

**3. Self-citation is not cross-citation, and the difference is structural.**
A provision that cites *itself at its own location* is degenerate: as a
precedent it is a tautology (Lemma 1), as an exception it is a contradiction —
the provision either says nothing or repeals its own condition. Cross-citation
is what carries content, and one particular cross-citation — naming a section
that is never enacted — is what makes a provision act **unconditionally**, which
no anonymous guard can do (Lemma 2). Everything in this chapter descends from
that asymmetry. *[established; the reading is interpretation, the two lemmas
are not.]*

**4. Entrenchment becomes architecture.** A kind nobody amends is immortal.
Chapter two noticed that such a provision is a *pump*. Under citation it is
better than that: because a law can now act regardless of its surroundings, an
entrenched provision placed at every cell is a **circuit element**. The
constitutions of §7 split cleanly into an entrenched part that nobody can amend
— the clock and the gates, standing at every cell forever — and an amendable
part that carries the state. The machine is the entrenched law; the data is the
ordinary law. That is not an analogy imposed on the mathematics: it is the
literal in-degree-0 / in-degree-≥1 split of the amendment digraph, and it is
what makes the Rule 110 construction work. *A statute book that entrenches
enough of itself stops being a body of rules and becomes a computer, with the
un-entrenched provisions as its memory.*


---

## 9. Scorecard against the frozen predictions Y1–Y8

**Y1 — the plenum still freezes. CONFIRMED, and hollowed out.** Theorem P; the
sharp criterion is saturation by the *exception image* `E(C)`, not by `K`, and
`E(C)` may name kinds the dynamics never enacts. Structurally the plenum theorem
*is* the statement `β(K) = K` for the bulk map, and Gridlock's exact epitaph
`h_k ∈ {any, k, g_k}` is the promised characterisation in terms of the citation
digraph. *[established]*

**Y2 — the Out-Degree Law survives citation verbatim. CONFIRMED.** By proof
audit (the monovariant never reads the guard), by 51,018,336 complete
classifications at out-degree ≤ 1 with a deepened residue, and by 80,000 deep
random runs: **zero gliders**. The charter's stated *reason* ("guards only thin
the actor set") is **wrong** — citation can make strictly more laws active than
occupancy — and this was flagged in the pre-registration before the audit ran.
The tropical monovariant has no hole; chapter two needs no re-audit on this
axis. *[established]*

**Y3 — citation is the computational substrate. CONFIRMED, and exceeded.**
Charter: ≈ 0.7 for a gate-level inventory with AND, NOT and fan-out; ≈ 0.35 for
a completed universality construction. Delivered: the full inventory (7/7 truth
tables, one step each) **and** an exact simulation of all 256 elementary
cellular automata by ≤ 15-kind, window-1 citation constitutions at two steps per
CA step, including Rule 110. Full Turing universality on ℤ is **not** completed
— a code is finite and the machine must build its own tape; the constructor
front that would do it is sketched in §7.3 at the *original proposal* tier.
*[established for the simulation; original proposal for universality]*

**Y4 — growth stays linear. CONFIRMED, and it is a triviality plus a sharp
constant.** `|S_t| ≤ n(2Wt + span₀ + 1)` in 1-D for any constitution whatsoever
(light cone × `n` laws per cell), and Path-Sum Confinement gives the same
guard-free. The bound is **attained**: a three-kind citation constitution with
`card = 3(2t+1)` exactly, i.e. the maximal rate `2nW = 6` laws per step
(battery **S5'**). *[established]*

**Y5 — a replicator exists. CONFIRMED, in the strongest form available.** Not a
special organism but a property of a constitution: in the Pascal clause **every**
finite code satisfies `S_{2^j} = S₀ ⊔ (S₀ + 2^j)` for every `2^j > span(S₀)`.
Proved (Frobenius over 𝔽₂), machine-checked on 200 random seeds, cross-checked
on the independent engine. The charter gave this ≈ 0.4. *[established]*

**Y6 — the four-law reset is not a coincidence. PREMISE REFUTED; the normal
form CONFIRMED and made exact; the "4 is forced" half REFUTED.**

*The premise.* Re-measuring **THE ODOMETER** (`OEW>B NQR>AB`, seed
`A@(0,0) A@(1,0) B@(0,1)`, parity) with `xnomos` gives card at `t = 2^k`,
`k = 0…13`, of

```
4, 5, 5, 6, 4, 6, 4, 4, 6, 4, 4, 4, 6, 4
```

— **not four at every power of two**. The reason is a compass ambiguity: the
root `verify.py` (lines 353–354) and `note/figs.py` use `N = (0,−1)`, while
`xamend2d/xa2d.py` (lines 29–35) and `xamend2d/RESULTS.md` use `N = (0,+1)`, so
the string `NQR` names two different rules and hence two different machines that
share the name. Under the root compass the card sequence is `6, 4, 4, 4, …`,
and the four-law claim is true. **This was already diagnosed inside the
repository** — `proofs/RESULTS.md` §2.4, "two machines wear the name THE
ODOMETER", certified by `proofs/t2_odometer.py` — by a concurrent expedition;
the finding above is an independent reproduction of it, not a new discovery.
What is still uncorrected at the time of writing is `XFINDINGS.md` §3,
`xamend2d/RESULTS.md` headline 9 and §11.2 (whose own table already shows
card 6 at `t = 2¹²`, two lines above prose claiming four), and the two HTML
demos. *[measured, both engines]*

*The explanation.* Y6 predicted that the Jubilee Code and the Odometer are two
instances of one binary-counter normal form, with the 4 forced by it. **The
first half is confirmed and can now be stated exactly; the second half is
refuted.**

Chapter three supplies a third counter, and its own (§5.6, THE LEDGER: three
laws, two kinds, window 1, on ℤ). Both it and the Odometer have the *same* exact
shape at every power of four — **a fixed head, plus one marker whose distance
doubles**:

| | at `t = 4^j` | card | reach |
|---|---|---:|---|
| **THE ODOMETER** (2-D, root-compass reading) | `{A@(0,0), A@(1,0), B@(0,1)} ⊔ {B@(0, 3·2^{j−1})}` | **4** = 3 + 1 | `3·2^{j−1} + 1 = 1.5√t + 1` |
| **THE LEDGER** (1-D, this chapter) | `{A@0, B@0, B@2} ⊔ {A@(2^j+2), B@(2^j+2)}` | **5** = 3 + 2 | `2^j + 3 = √t + 3` |

*[established by computation: the Odometer form verified exactly for `j = 1…8`,
the Ledger's for `j = 1…11`; battery **F8**, **F10**]*

So there **is** one normal form — *head ⊔ doubling marker*, reach `Θ(√t)`,
constant card at every `t = 4^j`, and a carry avalanche in between — and it now
has a witness in each of the two dimensions. But **the 4 is not forced**: it is
just `|head| + |marker|` for that particular machine, and the Ledger returns to
**five**. What is forced is the *shape*, not the number. The Jubilee Code's
reported reach `≈ 1.5√t` fits the same family; it was not re-examined here.

The replicator reading is also refuted: neither counter's reset state is two
disjoint translates of a common core, so `card(S_{2^j}) = 2·card(S₀)` — the
Fredkin signature that chapter three's additive sector genuinely produces
(§4.2) — is **not** the mechanism. The counters carry a marker; the replicators
carry a copy. *[the normal form is established; the reading of it is
interpretation]*


**Y7 — light-cone-admissible odd-ring rotors exist. CONFIRMED (a check, as the
charter said).** TANDEM-1 satisfies `Φ = rot_{+1}` **exactly** on every ring
`3 ≤ m ≤ 24`, odd and even alike, with `|r| = 1 ≤ p·W = 1` — inside the light
cone, so genuine transport. Chapter three adds two more full-ring rotors of its
own that chapter one could not have: **PROCESSION** and **LACUNA**, both on rings
every cell of which is occupied at every step. *[established; battery **S8**,
**F1**, **F6**]*

**Y8 — the impermanence sector is rich; sunset + citation is the easiest place
to build a machine. FIRST HALF CONFIRMED; SECOND HALF REFUTED — but the
controlled experiment says something better than either.**

Under sunset-by-default with lifetime `τ = 1` (a law lapses unless re-enacted,
so the next state is exactly the toggle set — `cite.step_sunset`), a
40,000-constitution random sample of the citation box gives **9.31 % certified
glider runs**, some 320× the 0.029 % of the permanent sector. Rich, yes.

The controlled experiment: the **complete** occupancy-guard corner (11,664
constitutions) against a size-matched random *citing* sample, same seeds, same
budgets, 1,119,744 runs each, every glider re-certified from its core
(`python3 sunset.py`, results in `data/sunset.json`):

| sunset, `τ = 1` | glider runs | glider-bearing | **speeds realised** |
|---|---:|---:|---|
| occupancy guards (complete corner) | 116,892 = **10.44 %** | 1,692 = 14.51 % | `1/2, 1` |
| citation guards (matched sample) | 104,483 = **9.33 %** | 1,515 = 12.99 % | `1/4, 1/3, 1/2, 2/3, 3/4, 1` |

**Citation does not make the sunset sector glider-*richer* — it makes it
glider-*faster and more varied*.** It thins the count by ~11 % and triples the
speed spectrum, adding `1/4, 1/3, 2/3, 3/4` which the anonymous-guard corner
does not realise at all in a complete enumeration. That is the same lesson as
§6.3: the guard is not a throttle on motion, it is a widener of the reachable
`(p,d)` set. And the second half of Y8 is simply wrong as a piece of advice —
the machine of §7 was built with *permanent* law and no sunset at all.
*[measured; the occupancy figure is consistent with X-D's independently measured
11.4 % at `τ = 1`, a useful cross-check that the two implementations of sunset
agree]*

### 9b. My own pre-registration, scored

| | outcome |
|---|---|
| **P1** citation inert at `n = 1` | **HELD** (Lemma 0, complete over 216 constitutions) |
| **P2** plenum holds but hollows out; sharp form is `E(C)` | **HELD** (Theorem P) |
| **P3** Gridlock ⟺ `h_k ∈ {any, k, g_k}` | **HELD exactly** (Theorem G) |
| **P4** the bulk is a map `β : 2^K → 2^K`, exact on rings, `β(K)=K` | **HELD** (Theorem B) |
| **P5** Y2 survives; the charter's *reason* is wrong | **HELD in both halves** |
| **P6** the unconditional law is the whole mechanism; linear CAs appear | **HELD** (Lemma 2, Theorem L) |
| **P7** Frobenius replication | **HELD** (Theorem R) |
| **P8** gate inventory + full CA simulation; universality on ℤ not completed | **HELD in all three parts** |
| **P9** census shape: gliders *rarer per constitution* under citation | **REFUTED.** 0.377 % (occupancy corner) vs 0.403 % (citing) — indistinguishable, if anything slightly higher. The rest of P9 held: 75 % extinct/fixed/balanced, 0.88 % unresolved at stage 1. |
| **P10** linear growth is trivial and the rate `2Wn` is attained | **HELD** (battery **S5'**) |
| **P11** self-citation at offset 0 is degenerate | **HELD for the stated lemma, REFUTED in its gloss.** I added that "self-citation cannot make a law unconditionally active, cross-citation can". Wrong: `g_k = k, a_k = 0` makes the *precedent* clause unconditionally true, and that is exactly what powers the machine's clock in §7.2. What self-citation cannot do is vacate the *exception* clause in a region carrying its own kind. |

Two of eleven refuted, one of them in a way that turned out to matter (the
self-citing clock is a load-bearing component of the Rule 110 construction).

---

## 10. Verification battery

`python3 verify_citation.py` — **40/40 checks pass**. Two engines with no code
in common are used throughout: `cite.py` (one big integer per kind, bitwise
shifts) and the repository's `xnomos.py` (dict of cell → bitmask).

```
E1  bitfield engine == xnomos, random citation universes    600 universes x 2 resolutions x 8 steps
E2  ring engine == xnomos on Z/m                            300 universes x 2 resolutions x 6 steps
T1  citation is INERT at n = 1                              216 one-kind constitutions, complete
T2  PLENUM: beta(K) = K                                     20,000 random constitutions, n <= 5
T2' PLENUM, sharp form: E(C)-saturation blocks              4,000 constitutions
T3  GRIDLOCK's epitaph: closed form == brute force          30,000 random constitutions, n <= 5
T3' GRIDLOCK fraction = ((3n+1)/(n+1)^2)^n                   complete at n = 1,2,3
T4  BULK MAP exact on homogeneous rings, every modulus      2,000 x 7 moduli x 2 resolutions
T5  bulk period <= 2^n - 2                                  complete n<=3 (2,098,448), sampled n=4,5
T6  SELF-CITATION at offset 0 is trivial                    3,000 random universes
T7  heterogeneous solid: blocked <=> h = any or dead letter 1,782 cases, exhaustive at n = 2,3
S1  SINGLE AUTHOR: in-degree <= 1 => parity == OR           800 universes x 10 steps
S2  DEAD LETTER under OR: fixed <=> no active law           4,000 universes x 6 states
S3  BALANCE: fixed-and-active => even cohorts               4,957 balanced citation codes
S4  ANCHOR (own-kind + citation): trailing law permanent    97,078 states
S5  PATH-SUM / LINEAR GROWTH bound                          3,000 universes x 39 steps
S5' the growth bound is TIGHT: card = n(2t+1)               t <= 29, rate 2nW = 6 laws/step
S6  DILATION survives ("occupancy" -> "cell content")       1,500 universes x 2 x 6 steps
S7  OUT-DEGREE LAW (Y2): deep search                        80,000 deep runs, zero gliders
S8  Y7: TANDEM-1 rotates 1 cell/step on every ring          m = 3..24
S9  SUNSET + citation: every reported glider re-certifies    2,549 sunset gliders, 3 full periods
F1  LACUNA: Phi = rot_(+1), occupancy constant              m in {5,7,8,11,13,16,21,32}
F2  SIX SESSIONS: bulk period 6 = 2^3-2                     m = 2..13, both engines
F3  PASCAL: card = 2^popcount(t)                            t <= 256 / 64
F4  THE COPY: every seed replicates at t = 2^j > span       200 random seeds
F5  THE WRIT: Z'(i) = Z(i-1) exactly                        400 random signal patterns
F6  PROCESSION: Phi = rot_(+1) on a completely full ring    m = 3..19, both engines
F7  CONVERSION FRONT: seam speed exactly 1                  14 steps, occupancy constant
F8  THE LEDGER: card 5, reach 2^j+3 at every t = 4^j        j = 1..8, exact
F9  THE LEDGER is aperiodic                                 400,000 hashed states, card in [3,139]
F10 THE ODOMETER shares the head-plus-marker form           j = 1..7, exact
M1  gate inventory                                          7/7 truth tables
M2  all 256 elementary CA rules simulated exactly           Z/11, 16 CA steps, 2 seeds each
M3  Rule 110 long run + xnomos cross-check                  60 + 20 CA steps, Z/23
M4  the machine is entrenched                               80 steps, clock and phases intact
C1  census slice reproduces                                 400 constitutions, deterministic
C2  census symmetry quotient is sound                       120 orbits, class multiset constant
C3  every census glider record re-certifies from its core   6,834 records, 3 full periods each
X1  xnomos.verify_glider certifies census gliders           60 sampled records, its own routine
X2  xnomos.verify_balanced certifies balanced codes         400 balanced citation codes
```

Counting rule for the census claims: **complete enumerations** are the citation
box of §6.1 (944,784 constitutions × 48 seeds × 2 resolutions = 90,699,264
weighted classifications, plus the 1,790,842-run deepened residue), the bulk
census (1,296 at `n = 2` and 2,097,152 at `n = 3`, each × 2 resolutions × all
`2^n` phases — and *no box caveat*, because `β` is a finite object), the defect
hunt (7,496,602 ring runs) and the boundary hunt (2,238,660 ring runs), and the
sunset occupancy corner (1,119,744 runs). Everything else is a **sample** with
its size stated.

---

## 11. Reproducing

Python 3.11, no dependencies beyond the standard library. From this directory
(the parent must be on `PYTHONPATH`, or run from the repository root):

```sh
python3 cite.py                     # engine self-tests (6/6), incl. cross-check vs xnomos
python3 verify_citation.py          # the 40-check battery                     (~25 min)
python3 specimens.py                # the fauna gallery with certificates      (~1 min)
python3 specimens.py lacuna ledger  # one or more named specimens
python3 circuit.py                  # gate inventory + all 256 elementary CA rules (~3 min)
python3 bulk.py                     # the COMPLETE bulk census, n = 2 and 3    (~4 min)
python3 bulk.py sample              # random search for long bulk orbits, n = 4,5,6
python3 sunset.py                   # prediction Y8: the sunset sector         (~10 min)
python3 census.py stage1 --procs 11 # the complete citation box, stage 1       (~3 min, 11 cores)
python3 census.py stage2 --procs 11 # the deepened residue                     (~35 min)
python3 fauna.py defect  --procs 4  # the complete travelling-defect hunt      (~4 min)
python3 fauna.py boundary --procs 4 # the complete phase-boundary hunt         (~3 min)
```

Data written to `data/`: `census1.json`, `census2.json`, `gliders1.txt`,
`gliders2.txt`, `residue2.txt` (the runs still unresolved after stage 2),
`bulk_census.json`, `bulk_sample.json`, `sunset.json`, `defect_hits.txt`,
`defect_stats.json`, `boundary_hits.txt`, `boundary_stats.json`,
`battery.log` and the run logs — about 4 MB in total.
`residue1.txt` (27 MB) is a stage-1 → stage-2 intermediate and is deleted after
use; `census.py stage1` regenerates it.

Paste-ready specimens (`cite.Cit(rules, targets, guards)`; `None` = *any*):

```python
LACUNA   = Cit([(0,-1,0),(0,0,0)], [(0,),(0,)], [(None,0),(None,0)])
           # seed on Z/m: every cell carries {0,1} except one cell carrying {1}
SIX      = Cit([(-1,1,0)]*3, [(0,1),(1,2),(0,1,2)], [(None,1),(None,2),(None,0)])
           # seed: a solid block (or a full ring) of kind-0 laws
PASCAL   = Cit([(0,0,1),(0,0,0)], [(0,),(1,)], [(0,1),(1,0)])
           # seed: any finite set of kind-0 laws.  Replicates at t = 2^j > span
WRIT     = Cit([(0,0,0),(0,0,1),(0,0,0),(0,0,0)], [(),(0,),(0,),()],
               [(3,3),(0,3),(0,3),(3,3)])
           # seed: kinds 1 and 2 at every cell, kind 0 (the signal) anywhere
CONVERT  = Cit([(-1,-1,-1)]*2, [(0,1),(0,1)], [(None,0),(None,1)])
           # seed: a block of kind-0 laws beside a block of kind-1 laws
LEDGER   = Cit([(-1,-1,0),(0,0,1)], [(1,),(0,1)], [(1,0),(1,0)])
           # seed: [(0,0),(0,1),(2,1)] -- three laws, parity
RULE110  = circuit.ECA(110).C        # 13 kinds, W = 1, 2 steps per CA step
```

---

## 12. Open questions

1. **Is `2^n − 2` the true maximal bulk period for `n ≥ 4`?** It is attained at
   `n = 2, 3` (complete census). Random search finds only 11 of a possible 14 at
   `n = 4`, 14 of 30 at `n = 5`, 16 of 62 at `n = 6` — the gap widens fast, so
   the bound is probably not tight. The bulk map is a finite combinatorial
   object — `A(U)` is determined by two citations per kind and `β` by the target
   masks — so this should be decidable outright rather than sampled.
2. **Turing universality on ℤ.** §7.3 reduces it to a constructor front laying
   gate kinds at speed 1 ahead of a computation whose light cone advances at
   1/2. That is the sharpest open question of this chapter, and it now looks
   like engineering rather than discovery.
3. **What replaces Cryptic Unipotency?** The step map is degree ≤ 3 over 𝔽₂ and
   the "freeze the occupancy and linearise" technique is gone (§3.4). Is there a
   citation analogue — freeze the *cited* fields, linearise in the rest — and
   does it give a period theorem? The census's period spectrum
   (`{2,…,64}` including 3, 5, 7, 9, 42, 54) is currently unexplained.
4. **A wide-glider search in the citation sector.** Every glider number here is
   a narrow-glider statement: seeds of span ≤ 3, cores of span ≤ 15, residue
   deepened only to span 1500. MIRROR's span-616 glider was found by a
   dedicated subshift decider, not by a box; the same tool has never been
   pointed at citation constitutions.
5. **Does citation change the density of balance?** The cohort theorem survives
   verbatim, but 13.5 % of this box classifies as BALANCED and that is a large
   share for a phenomenon chapter one proved impossible. Chapter two's exact
   counting recursion `a(s) = 4a(s−1) − 2a(s−2)` for balanced codes was derived
   with anonymous guards; the citation analogue is not known.
6. **Why `head ⊔ doubling marker`?** Two machines in two dimensions, found by
   different expeditions with different methods, have *literally the same* exact
   form at every power of four (§9, Y6). Is there a theorem forcing it — some
   carry-propagation argument that says a bounded-card, unbounded-reach code on
   a window-1 lattice must look like this? The Ledger, being three laws on ℤ,
   is small enough to be analysed by hand, and that is the obvious next move.
7. **Two dimensions.** Everything here is 1-D. The bulk map is dimension-free
   (Theorem B never uses the offsets), so bulk oscillators and the plenum
   theorem lift immediately; the fauna and the census do not.
