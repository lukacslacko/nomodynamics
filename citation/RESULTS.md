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
the same dynamics. *[established; battery **T1**, complete over all 216 one-kind
constitutions × all guard choices]* The smallest sector where citation can do
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
a universal dead letter. Theorem G is the uniform statement, which is the one
that matches the bulk map and the motivating example.)*

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
> census for `n ≤ 3`; battery **T5**]* At `n = 4, 5, 6` a random search over
> 400 k / 200 k / 200 k bulk data found maxima **11, 12, 21** against the bounds
> 14, 30, 62 — **[measured, sampled]**; whether `2^n − 2` is attained for
> `n ≥ 4` is open.

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

* **Complete**, over the whole census box (§5): all 531,441 constitutions with
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
the right every one of the ten interior laws fires at once and the block turns
into a Pascal triangle. `h_1 = 1 ∉ {any, 0, g_0}`, so Theorem G says Gridlock is
dead for this constitution — and it is.

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
*[established; battery **F7**: 15 steps, seam speed exactly 1, occupancy
constant]*

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

The one strongly non-uniform row is UNRESOLVED: a living bulk makes trajectories
**9.4×** harder to resolve at fixed budget, which is the census-level signature
of the new habitat.

**Cycle periods** (parity, weighted, periods capped at 64):
2 (5,855,368), 4 (1,342,412), 8 (181,468), **3** (52,240), 6 (27,732),
16 (11,152), 32 (5,460), **9** (3,028), **5** (3,004), 12 (1,824), 64 (1,624),
**7** (1,396), 18 (1,188), 10, 14, 24, **42**, 28, **54**, 48, … The distinct
periods realised in the box are
`{2,3,4,5,6,7,8,9,10,12,14,16,18,20,24,28,32,34,36,40,42,46,48,54,56,64}`.
*[measured, this box]*

**Gliders.** 6,834 glider records over 951 representative constitutions; every
one re-certified from its glider core by `cite.verify_glider` over three full
periods (the seed itself often has a pre-period, so the naive check on the seed
fails — a trap worth recording). Weighted `(resolution, p, d)` spectrum:

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
budget raised 7.5× in time and 12.5× in span:

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

