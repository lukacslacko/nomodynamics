# Expedition Y-C — the replicator hunt

*Chapter three, prediction **Y5**: "some code in the citation or multi-target
sector produces a disjoint copy of itself." Confidence recorded in
`CITATION.md` before the run: ≈ 0.4.*

Honesty tiers used throughout: **[E] established** (proved here or cited from a
proof elsewhere in the repo), **[M] measured** (a bounded search or a numerical
observation — decides a box, never a question), **[P] proposal**
(interpretation, conjecture, framing).

---

## 1. PRE-REGISTRATION

*Written and saved before the first search run. Kept verbatim; the scorecard in
§9 is appended afterwards, and nothing above this line was edited after the
searches began.*

### 1.1 What I will call a replicator

The state space: finite sets of **placed laws** `(i,k) ∈ ℤ^D × K`. A state is
written `S`, the global map `Φ`, translation `σ^d`. `card(S)` counts placed
laws, `supp(S) ⊆ ℤ^D` the occupied cells.

**Interaction radius.** `R(C) = max` sup-norm over all offsets `a_k,b_k,c_k`.

> **Lemma S (separation).** If `dist_∞(supp A, supp B) > 2R` then
> `Φ(A ⊔ B) = Φ(A) ⊔ Φ(B)` and the images are again disjoint, in every mode.

Two copies at sup-distance `> 2R` are therefore *causally independent* for one
step: neither can read, block, or write onto the other. I call such copies
**free**. Copies that merely have disjoint supports I call **embedded**.

### 1.2 The rung ladder (pre-registered, strict)

Let `S` be the seed, `p ≥ 1`, and `d₁ ≠ d₂ ∈ ℤ^D`.

- **Rung 1 — periodic doubling.** `card(S_t) → ∞`, and at some `t` the state
  contains two **embedded** copies `σ^{d₁}S, σ^{d₂}S` with disjoint supports.
  No gap, no debris condition. *Cheap.*
- **Rung 2 — clean replicator.** There are `p, d₁ ≠ d₂` with
  `Φ^p(S) ⊇ σ^{d₁}S ∪ σ^{d₂}S`, the two copies **free** (gap `> 2R`), and the
  debris `D = Φ^p(S) ∖ (σ^{d₁}S ∪ σ^{d₂}S)` either empty (**rung 2-exact**) or
  a state that is itself eventually periodic under `Φ` in isolation
  (**rung 2-debris**). The gap requirement is what stops a solid growing block
  from qualifying — see §1.4.
- **Rung 3 — colony.** The number of pairwise-**free** copies of `S` inside
  `S_t` is unbounded in `t`. (Sub-rung **3-emb**: unbounded *embedded* copies.)
- **Rung 4 — constructor.** A code that builds a *specified* target pattern
  read off a blueprint carried in its own body. I do not expect to reach this;
  if I do not, I will say so plainly.

### 1.3 Certificate standard

Every claimed replication event is re-verified by `replib.pstep`, an engine
written from the definition on **frozensets of placed laws**, sharing no code
with `xnomos.step` (which uses `{cell: bitmask}`). Certificates exhibit `p`,
the offsets, the two copies as explicit cell sets, the gap, and the debris.

### 1.4 Anti-cheat clauses

**(a) The solid block.** The colonizer `(0,1,1)` from a solid block of `n` laws
satisfies `Φ^n(S) = S ⊔ σ^n(S)` **exactly** — a "replicator" by the naive
reading. It is excluded by the gap requirement (the two blocks are adjacent,
gap 1 ≤ 2R = 2). Any specimen I report must survive this test, and I will run
the colonizer through the detector to confirm the filter bites.

**(b) The one-law seed.** If `card(S) = 1` then "a copy of `S`" means only "a
law of the same kind somewhere", and rung 2 degenerates: any constitution that
turns one law into two well-separated laws of that kind qualifies. I therefore
require of a **reported specimen** that `|supp(S)| ≥ 2` — the seed occupies at
least two distinct cells, so that a copy has to reproduce a *spatial relation*,
not just a symbol. One-law results will be reported separately and labelled
**degenerate**.

*(Clause (b) added before the first search run, after writing the detector and
noticing the degeneracy; §1.1–1.3 and §1.5 unchanged.)*

### 1.5 What I expect (recorded before searching)

- **Y-C-1.** Rung 1 is reachable and cheap; the Pascal columns will qualify.
  Confidence 0.85.
- **Y-C-2.** Rung 2 is reachable somewhere in the multi-target / citation
  sector. Confidence 0.5. *(The charter's Y5 said 0.4; I am marginally more
  optimistic because out-degree ≥ 2 already buys motion and a fissioning
  glider is the obvious mechanism.)*
- **Y-C-3.** Rung 3 in the **exponential** sense is impossible. The light cone
  gives `card(S_t) ≤ n·(span₀ + 2Rt + 1)^D`, polynomial in `t`; a colony whose
  copies are all free would double every `p` steps. Confidence 0.95 — I expect
  this to become a theorem, and if so the mission's rung 3 must be **rewritten**
  as "unboundedly many copies, necessarily at polynomial rate".
- **Y-C-4.** Rung 4 is out of reach this cycle. Confidence 0.9.
- **Y-C-5 (linearity).** `Φ` is **not** `𝔽₂`-linear: superposition
  `Φ(A Δ B) = Φ(A) Δ Φ(B)` will fail on overlapping supports for generic
  constitutions, because occupancy guards are an OR over kinds. But it will
  hold *automatically* for separated supports (Lemma S), so **any** replicator
  whose copies are free will look additive at the moment of fission. The honest
  question is therefore not "is the replicator additive?" but "**does the
  fission happen in the sparse regime, where additivity is free, or in
  contact, where it is not?**" I expect the first specimens to be sparse, and I
  will hunt specifically for a contact fission. Confidence in the reframing:
  0.8.

---

*(Everything below this line was written after the searches ran.)*
