# Expedition Z-A — the constructor

*Von Neumann's rung 4. Chapter six of nomodynamics.*

Honesty tiers, as in `replication/RESULTS.md`: **[E] established** (proved here
or cited from a proof elsewhere in the repo), **[M] measured** (a bounded search
or a numerical observation — decides a box, never a question), **[P] proposal**
(interpretation, conjecture, framing).

---

## 1. PRE-REGISTRATION

*Written and saved before the first construction run. Kept verbatim; nothing
above the line in §1.6 was edited after the runs began.*

### 1.1 Inherited definitions

From `replication/RESULTS.md` §2, unchanged:

- state `S` = finite set of placed laws `(i,k) ∈ ℤ^D × K`; `Φ` the global map;
  `σ^d` translation; `card` = number of placed laws; `supp` = occupied cells.
- **interaction radius** `R(C) = max_k max(‖a_k‖_∞, ‖b_k‖_∞, ‖c_k‖_∞)`.
- **Lemma S**: `dist_∞(supp A, supp B) > 2R ⟹ Φ(A ⊔ B) = Φ(A) ⊔ Φ(B)`, images
  again disjoint, in every mode and with citation guards.
- **free** = pairwise sup-distance `> 2R`. **causal component** = a maximal
  cluster of the support under the "within `2R`" relation.
- **Theorem A**: `card(S_t) ≤ n(s₀ + 2Rt + 1)^D`. **Corollary A1**: no
  exponential colony, in any dimension. **Corollary A2**: no exact fission at a
  fixed period can iterate forever.

### 1.2 What a rung-4 object must be, stated so it can be checked

A **blueprint-carrying machine** is a pair `(C, S(·))` where `C` is a
constitution **independent of the blueprint** and `S : {0,1}^+ → states` is an
injective seed map, together with a fixed decoder `β(·)` with `β(S(w)) = w`.
The *machinery* is `S(w)` minus the blueprint cells; it must be the same
(up to translation) for every `w`.

Write `p(w)` for a period and `d(w)` for a displacement. I pre-register three
labels, exactly as the mission names them, and one composite.

- **4a — transport + memory.** There are `p, d ≠ 0` with `Φ^p(S(w)) = σ^d S(w)`
  (a glider whose body contains the blueprint), *and* the blueprint is read
  on the orbit: some law whose guard **cites** a blueprint kind fires at least
  once per period, and the ablation of §1.4(c) breaks the object. No second
  copy required.
- **4b — construction without freedom.** At some `t`, `Φ^t(S(w))` contains two
  disjoint translates of `S(w)` — the machinery *and* the blueprint — but they
  are **not** free (sup-distance `≤ 2R`), i.e. they are one causal component.
- **4c — the constructor.** There are `p(w)`, `d₁ ≠ d₂` with
  ```
      Φ^{p}(S(w))  =  σ^{d₁}S(w)  ⊔  σ^{d₂}S(w)  ⊔  D ,
  ```
  the two copies **free** and each a whole causal component of `Φ^p(S(w))`
  (so also free from `D`), `D` empty or inert; **for every** `w`, with one
  blueprint-independent `C`; and the construction is **guard-driven** in the
  sense of §1.4. Because the copies are whole causal components, Lemma S makes
  "the copy then does the same" automatic.
- **4c⁺ — colony.** The number of pairwise-free exact translates of `S(w)`
  inside `Φ^t(S(w))` is unbounded in `t`, for every `w`. (By Corollary A1 this
  can only be polynomial; I am not asking for more.)

I will also record **4c⁻**, the *lineage* weakening: an unbounded sequence of
times at which a free exact translate of `S(w)` exists as a whole causal
component, but with only one such copy alive at a time. A 4c⁻ is a
self-rebuilding traveller, not a replicator, and I will say so if that is all I
get.

### 1.3 Mirror clause

If the child is the mirror image `S̄(w)` of the seed rather than a translate, I
require the **second** generation to be an exact translate, and I state the
certificate at `2p`. A handed machine whose grandchild is exact is honest; a
machine whose "copy" is a different object is not.

### 1.4 Anti-cheat clauses — the anti-Fredkin bar

`replication/RESULTS.md` §6.3 showed that every *additive* replicator in this
program is additive because some guard can never fail; and additive CA replicate
**arbitrary** patterns for free (Fredkin). A blueprint-carrying replicator built
that way would be worthless. So a reported 4a/4b/4c specimen must pass **all
four**:

- **(a) N1 — the guard bites.** `Φ^t(S) ≠ L^t(S)` for some `t ≤ p`, where `L`
  is the unconditional linear map of `replication/RESULTS.md` §2.4.
- **(b) N2 — the splitting test.** Some splitting `S = A ⊔ B` has
  `Φ^p(S) ≠ Φ^p(A) Δ Φ^p(B)`.
- **(c) The citation ablation.** Replacing every citation guard that names a
  **blueprint** kind by the anonymous occupancy guard `(any, any)` destroys the
  property — the same one-line control that `citation/RESULTS.md` §5.6 runs on
  THE LEDGER. This is the clause that says the blueprint is *read*, not carried.
- **(d) The blueprint discrimination test.** Two blueprints `w ≠ w'` of the same
  length must give `Φ^p(S(w)) ≠ Φ^p(S(w'))` translated — i.e. the child differs
  exactly as the parent does, symbol for symbol, and the decoder recovers `w`
  from the child. A machine that copies a *fixed* pattern and merely carries
  junk alongside fails this.

### 1.5 Certificate standard

Every claim is machine-checked on **two engines**: `xnomos.step` (dict of
bitmasks) and `replib.pstep` (frozenset of placed laws), which share no code.
Copies are exhibited as explicit cell sets with their sup-distance, and the
debris is exhibited in full. Colony counts are computed by an independent
component-splitter, not by pattern matching alone.

### 1.6 What I expect (recorded before the first construction run)

- **Z-A-1.** 4a is reachable. Confidence 0.85. THE SCRIBE's clerk is already a
  moving reader; what it lacks is a *moving tape*.
- **Z-A-2.** 4b is reachable. Confidence 0.8 — THE SCRIBE is one erasure away.
- **Z-A-3.** 4c is reachable. Confidence 0.55. The obstruction named by
  Expedition Y-C (Observation C: a write of range `R` can never open a gap of
  `2R+1`) is real but I believe it is beaten by *erasure*, not by travel: if the
  parent's tape is consumed as it is read, and the child is built at range `3R`
  through a self-clearing relay, the intervening rows are empty at the moment
  the child completes. That is the design I will try first.
- **Z-A-4.** 4c⁺ is reachable **if** 4c is, and only in the OR resolution:
  under parity the coincident writes of two neighbouring copies cancel, exactly
  as `replication/RESULTS.md` §3.1a records for THE SPLIT DECISION.
  Confidence 0.5.
- **Z-A-5.** Full von Neumann universality — the blueprint describing the
  *machinery* as well, so that the constitution is a universal constructor —
  is **out of reach this cycle**. Confidence 0.85. I expect to reach the
  Langton level (arbitrary heritable genome, hard-wired machinery) and I will
  label it as that, not as von Neumann's `U`.
- **Z-A-6.** The kind count will be large: 60–120. Nothing in this program has
  needed more than 31, and I expect no elegance here. Confidence 0.7.
- **Z-A-7.** The population will grow **linearly**, not exponentially
  (Corollary A1 forbids exponential; the OR-merge of coincident children is the
  mechanism, as in THE SPLIT DECISION). Confidence 0.7.

*(Everything below this line was written after the runs.)*

---

## 2. THE SUCCESSION — the specimen

*2-D · **73 kinds** · window 1 (`R = 1`) · citation guards · **OR** resolution ·
seed = a charter of `n+2` cells plus a 16-law clerk bundle in one of them.*

Constructed, not found. `artificer.py` builds it; `verify_constructor.py`
re-checks every line of this section on two engines.

### 2.1 What it is, in one paragraph

A **charter** is one row of `ℤ²` reading `L s₁…s_n Z`, the `s_i` drawn from two
inert kinds `X` (blueprint `0`) and `Y` (blueprint `1`), with `L` and `Z` the
end markers — four **dead letters**, whose guard cites a phantom kind and is
therefore never satisfied. A **clerk** is a bundle of sixteen placed laws
occupying a single cell of that row. The clerk walks the charter, and at each
cell does four things in the one step:

| law | reading it aloud | effect |
|---|---|---|
| `A_h` | *while I stand here, repeal my whole bundle here* | erases itself |
| `B_h` | *while I stand here and my own end marker does **not**, enact my whole bundle one cell along* | moves one cell |
| `T_s^{u,d}` | *while section `s` stands here, commence a relay one row up (down)* | reads the symbol **by name** |
| `E_s` | *while section `s` stands here, repeal it* | consumes the charter |

The relay (`riser`) is four kinds per payload per direction. At each stage a
`C`-law clears the stage's own pair from its cell and a `W`-law writes the next
stage one row further out; after **two** stages the payload lands **three rows
away**, and both intermediate rows are empty again on the next step. When the
clerk reaches its own end marker, `B` is blocked (a citation in a *vacancy*
clause) and a further pair of relays `S_h^{u,d}` fires, whose payload is a whole
clerk bundle **of the opposite handedness**. It lands on the child's far end at
exactly the step the child's last symbol does.

Every guard in the constitution reads **only its own cell** (`a = b = (0,0)`
throughout). The machine has no sensors; all coupling is through writes.

### 2.2 The certificate — rung 4c, exact, debris-free

`R = 1`, so *free* means sup-distance `> 2R = 2`. Let `S(w)` be the charter for
blueprint `w ∈ {0,1}^n` with a right-handed clerk on its `L` cell, and `S̄(w)`
the same charter with a left-handed clerk on its `Z` cell (the mirror form of
§1.3). Then, **exactly, for every `w` tested**:

```
    p = n + 4

    Φ^p ( S(w) )   =   σ^(0,+3) S̄(w)   ⊔   σ^(0,−3) S̄(w)          debris ∅
    Φ^2p( S(w) )   =   σ^(0,−6) S(w)  ⊔  S(w)  ⊔  σ^(0,+6) S(w)     debris ∅
```

The two children of the first line are whole causal components: their supports
are two full rows six apart, so **gap = 6 > 2R = 2**, and rows `−2 … +2` are
*completely empty* at `t = p` — the parent charter has been eaten, the relays
have cleared themselves. The second line is the mirror clause discharged: the
grandchildren are exact translates, and the middle one is the seed itself, in
place.

| `w` | `n` | `p` | `card S(w)` | `card Φ^p` | `Φ^p` exact | `card Φ^2p` | `Φ^2p` exact |
|---|---|---|---|---|---|---|---|
| `0` | 1 | 5 | 19 | 38 | ✓ | 57 | ✓ |
| `1` | 1 | 5 | 19 | 38 | ✓ | 57 | ✓ |
| `011` | 3 | 7 | 21 | 42 | ✓ | 63 | ✓ |
| `1001` | 4 | 8 | 22 | 44 | ✓ | 66 | ✓ |
| `01101001` | 8 | 12 | 26 | 52 | ✓ | 78 | ✓ |

### 2.3 The frames

Blueprint `011`, `n = 3`, `p = 7`. `[`/`]` are the end markers, `0`/`1` the
blueprint symbols, `#` a clerk standing on a symbol, `:` a relay in flight.
Rows `+5` (top) to `−5` (bottom).

```
 t= 0 card 21   t= 3 card 28   t= 6 card 16   t= 7 card 42   t=14 card 63
 ........       ........       ........       ........       .[011>..   +6
 ........       ........       ........       ........       ........
 ........       .[......       .[011...       .[011#..       ........
 ........       ..:.....       .....:..       ........       ........
 ........       ...:....       ........       ........       ........
 .#011]..       ....#]..       ........       ........       .#011]..    0
 ........       ...:....       ........       ........       ........
 ........       ..:.....       ........       ........       ........
 ........       .[......       .[011...       .[011#..       ........
 ........       ........       .....:..       ........       ........
 ........       ........       ........       ........       .[011>..   −6
```

At `t = 6` the two children are **incomplete** — the last symbol and the clerk
are still in flight — and at `t = 7` they are complete, free, and nothing else
exists. `card` dips to **16** at `t = 6`, below the seed's 21: the parent is
already gone. This is a true fission, not a budding.

### 2.4 The colony — rung 4c⁺

Because the two children are whole causal components, Lemma S makes the next
generation automatic; because coincident writes **merge** under OR instead of
cancelling, the middle children of neighbouring parents fuse. The population is
therefore linear, not exponential — which is the only thing Corollary A1 allows.
Measured, both engines, `w = 011` and `w = 1001`:

| generation `g` | 0 | 1 | 2 | 3 | 4 | 6 | 8 | 10 | 12 |
|---|---|---|---|---|---|---|---|---|---|
| `t = g·p` (`w=011`) | 0 | 7 | 14 | 21 | 28 | 42 | 56 | 70 | 84 |
| **free exact charters** | 1 | 2 | 3 | 4 | 5 | 7 | 9 | 11 | **13** |
| rows occupied | `0` | `±3` | `0,±6` | `±3,±9` | `0,±6,±12` | … | … | … | `0,±6,…,±36` |
| `card` | 21 | 42 | 63 | 84 | 105 | 147 | 189 | 231 | **273** |

At generation `g` the state is **exactly** `g+1` charters on rows
`−3g, −3g+6, …, +3g`, spaced 6 apart, every one of them carrying the blueprint
`w` intact and re-readable, every one of them carrying a clerk, and **nothing
else**: `card = (g+1)·card(S(w))` on the nose at every generation. Handedness
alternates with the parity of `g`; even generations are exact translates of the
seed.

