# Nomodynamics — index of named results

*One line each, with sector, status and location. Status follows the program's
three tiers: **proved** (a proof exists and is written down), **measured**
(complete or sampled computation, scope stated at the source), **conjecture**
(stated precisely, not settled). Everything marked proved or measured is also
re-derived by `python3 verify.py`, which runs 59 checks on the shared engine
independently of the code that found the results.*

Definitions are in `note/nomodynamics.pdf` §2. Throughout, a **constitution**
gives each kind k offsets (a_k,b_k,c_k), a target set T_k, and citations
(g_k,h_k) ∈ K ∪ {∗}; the founding system is T_k = {k}, g_k = h_k = ∗.

---

## Chapter one — the founding system (own-kind, occupancy guards)

| result | statement | status | where |
|---|---|---|---|
| **Gridlock** | A solid code is frozen: in a fully occupied region every vacancy guard fails. *All dynamics is surface dynamics.* | proved — **fails under citation** | `FINDINGS.md`; epitaph in `citation/` |
| **Single Author** | Only the kind-k law at j−c_k can flip kind k at j; hence parity ≡ OR identically, and per-kind dynamics is occupancy-modulated 𝔽₂-linear. | proved | `rings/RESULTS.md`, `glider-question/RESULTS.md` §2.1 |
| **Dead Letter** | A code is fixed iff every law in it is blocked — no balanced constitutions. | proved — **fails under parity cross-amendment**, survives OR | `rings/RESULTS.md` |
| **Anchor** | Own-kind toggles of kind t land only at offset c_t, so the trailing extremal law is never targeted: *the eldest law cannot be repealed*. No free gliders on ℤ, any window, dimension, guard or resolution. | proved | `glider-question/RESULTS.md` §2.2 |
| **Ray confinement** | 2-D own-kind growth is pinned to axis rays; α ≤ 1, the plane never fills. | proved | `nomos2d/RESULTS.md` |
| **Barber poles** | On ℤ/m, Φ(S) = rot_r(S) is *not* transport when min(r,m−r) > p: the founding ℤ/6 "rotor" changes two cells per step and merely coincides with its own rotation. Own-kind nomodynamics has no transport anywhere. | proved — **retraction of a published claim** | `xrings/RESULTS.md`, `XFINDINGS.md` §6 |
| **Cycle-Length Law** | The frozen-occupancy operator of an L-cycle constitution lives in 𝔽₂[y]/(y^L−1), which is local exactly when L is a power of two — so "all periods are powers of two" was a fact about cycle length **one**. | proved | `xrings/RESULTS.md` |
| **Jubilee clock** | \|S_t\| = 4 at every t = 2^k (16/16 exact, t < 2¹⁷); crest at 2^k−1 doubling every second power; population graded by the binary weight of t. | measured (complete to 2¹⁷) | `nomos2d/JUBILEE-LAW.md` |
| **Sunset Parliament** | Single-kind ring codes reach exact maximal periods 15, 63, 341 at m ≡ 2 (mod 4) — orders of 𝔽₂ polynomials. | measured | `rings/RESULTS.md` |

## Chapter two — cross-amendment (a law may amend another kind)

| result | statement | status | where |
|---|---|---|---|
| **Out-Degree Law** | If every law amends at most one of the kinds in play, **no free glider exists** — any offsets, window, dimension, resolution. Contains the Anchor Theorem. | proved | `xamend1d/RESULTS.md` §2.5 |
| **Tropical Speed Law** | For a glider of period p, displacement d: p·min(λ_min,0) ≤ d ≤ p·max(λ_max,0), λ the extreme cycle means of the amendment digraph. | proved | `xamend1d/RESULTS.md` §2.3 |
| **Zero-/Unique-Cycle** | A glider forces every non-empty predecessor-closed kind set to contain a zero-weight cycle or two cycles of opposite sign; at most one cycle ⟹ no glider. | proved | `xamend1d/RESULTS.md` §2.4 |
| **Supersession no-go** | State-dependent supersession targeting admits no free glider in any dimension. | proved | `xamend1d/RESULTS.md` §3 |
| **Balance** | Under parity a code is fixed-but-active iff its active laws split into even **cohorts** co-signing the same amendment; minimum two laws, in one cell. Needs in-degree ≥ 2. Under OR no balanced code exists at any size. | proved | `xtheory/RESULTS.md` |
| **Path-Sum Confinement / Zero-Sum No-Go** | Support is confined to path sums of the cycle offset-sum S_Z; if every reachable cycle has S_Z = 0 the code is bounded forever; a glider's velocity is a positive multiple of S_Z. | proved | `xtheory/RESULTS.md` |
| **Growth dichotomy** | Out-degree 1 ⟹ \|S_t\| ≤ \|S₀\|(t+1), so α ≤ 1 in every dimension; out-degree ≥ 2 attains α = 2 from a single law (LAND GRANT, \|S_t\| = (t+1)²). | proved | `xamend2d/RESULTS.md` |
| **Dilation** | (W,p,d) ↦ (rW,p,rd), which rules out any width-independent speed cap a priori. | proved | `xspeed/RESULTS.md` |
| **Even-Support Law** | For any kind set U with \|T_k ∩ U\| even for all k, the symmetric difference of supports over U is a constant of the motion and vanishes in a glider. Generalises the Twin-Kind Lemma. | proved | `xspeed/RESULTS.md` |
| **Width correction** | A bounded search decides a **box**, not a question: MIRROR carries displacement-2 gliders of span 53, 438, 616, invisible to every census box in this program. All fixed-box "impossible" claims are narrow-glider statements. | methodological — **program-wide** | `xspeed/RESULTS.md`, `XFINDINGS.md` §5 |

## Chapter three — citation (guards that name a kind)

| result | statement | status | where |
|---|---|---|---|
| **Gridlock's epitaph** | A uniform solid region is interior-frozen **iff** h_k ∈ {∗, k, g_k} for every kind; surviving fraction ((3n+1)/(n+1)²)ⁿ — 60.49 % at n = 2, 0.34 % at n = 6. | proved | `citation/RESULTS.md` |
| **Survival audit** | Out-Degree, Tropical Speed, Path-Sum, Anchor, Balance, Dead Letter (OR) all survive verbatim — because the monovariant never reads the guard. The 𝔽₂-linear layer does **not**: the step map is a degree-3 polynomial in the kind fields. | proved | `citation/RESULTS.md` |
| **CA-completeness** | All 256 elementary cellular automata simulate exactly, cell for cell, at ≤ 15 kinds and window 1. | construction | `citation/RESULTS.md` |

## Chapter four — impermanence (a law lapses unless re-enacted)

| result | statement | status | where |
|---|---|---|---|
| **Lone Survivor** | In any dimension a lone law survives iff a = 0 and b ≠ 0, and then translates by exactly c: **its velocity is its target offset**. Complete over all 27 kinds on ℤ and all 729 on ℤ². | proved | `sunset/RESULTS.md` §2, §8 |
| **Gridlock's mirror** | A solid block evaporates in one step, leaving only its front — where under permanence it freezes. In both worlds only the surface matters: in one the only part that moves, in the other the only part that lives. | proved | `sunset/RESULTS.md` §3 |
| **Conservation** | With τ = 1 and out-degree ≤ 1, \|S_{t+1}\| ≤ \|S_t\|: an impermanent code can never grow. So **one threshold governs both worlds** — out-degree ≤ 1 forbids motion under permanence and growth under impermanence. | proved | `sunset/RESULTS.md` §7 |
| **Longevity Law** | One code, one seed: with lifetime τ the packet's speed is exactly **2/(τ+1)** — displacement fixed at 2, only the period changing. The Anchor Theorem is the τ → ∞ limit. | measured (certified τ = 1…12) | `sunset/RESULTS.md` §4 |

## Chapter five — computation

| result | statement | status | where |
|---|---|---|---|
| **Self-clearing kind** | A law that repeals itself every step satisfies x(t+1) = f(t): *a provision that expires every step is a register.* | proved | `computation/RESULTS.md` §1 |
| **Statute–Circuit** | A normal-form constitution **is** a synchronous AND-NOT network with free XOR fan-in, free fan-out and unit delay. A law nobody amends is a gate; a law that repeals itself is a wire. | proved | `computation/RESULTS.md` §1 |
| **Rule 110** | Runs inside a 24-kind window-1 constitution, three amendment steps per CA step. Certificate is a **complete enumeration of the local map's inputs** (all 2⁷ configurations of ℤ/7), which decides ℤ. | construction, complete certificate | `computation/RESULTS.md` §3 |
| **Finite-code universality** | Every Turing machine compiles into a **finite code** of the founding occupancy-guard sector, tape supplied by a self-extending front. Nomodynamics is computation-universal; halting for finite codes is undecidable. | proved | `computation/RESULTS.md` §5 |
| **P-completeness** | PREDICT is P-complete under log-space reductions at dimension 1, window 0, one cell. | proved | `computation/RESULTS.md` §6 |
| **The linear sector is tame** | The single-author sector is 𝔽₂-linear with Φᵗ = Lᵗ; PREDICT there is in NC, so it is not P-complete unless NC = P. *Chapter one's solvable sector is provably the wrong place to look for computation.* | proved (NC membership quoted) | `computation/RESULTS.md` §6 |
| **Computation without transport** | Every gate law and power law stands exactly where it started, certified over 60 steps at out-degree 1. *A statute book can compute while every one of its provisions stands still.* | measured | `computation/RESULTS.md` §4.1 |

## Chapter six — replication

| result | statement | status | where |
|---|---|---|---|
| **Rung 3 reached** | THE SPLIT DECISION is true binary fission — Φ²(S) = σ^(0,−2)(S) ⊔ σ^(0,+2)(S) exactly, parent gone, no debris, t/2+1 free copies at every even t. THE ENGROSSMENT replicates in the **founding** semantics. | construction, certified | `replication/RESULTS.md` |
| **Not additive** | Replication here is *not* the Fredkin phenomenon: the replicators fail the splitting test. And 2^popcount(t) is **not** a signature of additivity. | measured | `replication/RESULTS.md` §6 |
| **Light-cone bound** | card(S_t) ≤ n(s₀+2Rt+1)^D, so **exponential replication is impossible in every dimension**, and no fixed-period doubling survives — every free fission must eventually self-collide. | proved | `replication/RESULTS.md` |
| **Lemma S** | Separation implies independence, so long-range superposition is free and proves nothing about additivity. | proved | `replication/RESULTS.md` |

---

## Open, stated precisely

1. **The constructor.** A rung-4 object is a blueprint-carrying packet that *moves*: travel needs out-degree ≥ 2, reading needs citation, nothing forbids the combination, nobody has built it.
2. **Does the strict own-kind sector compute?** Every universality construction so far uses cross-amendment even at out-degree 1. Bracketed by an NC result below and Sierpinski (own-kind + citation) above.
3. **The width-free speed cap.** In the single-field sector \|d\| ≤ 2 under parity and ≤ 1 under OR at any width and any number of channels; the resource that buys \|d\| ≥ 3 is another 𝔽₂ field, not another kind. Prove it, and explain why it fails to scale with the window.
4. **Turing universality on ℤ in the citation sector** — reportedly now engineering rather than discovery: a constructor front laying gate kinds at speed 1 ahead of a light cone advancing at 1/2.
5. **Light-cone-admissible odd-ring rotors**, and whether every such rotor is a wrapped ℤ glider.
6. **The Jubilee clock law**, proved rather than measured.
