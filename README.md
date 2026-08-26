# Nomodynamics

**The mathematics of self-amending law.** A minimal, parameter-free dynamical
system whose only substance is laws acting on laws — and the first census,
theorems, and fauna of the resulting universe.

📄 **[The founding note (PDF)](note/nomodynamics.pdf)** · 🖥 **[Live demo](https://lukacslacko.github.io/nomodynamics/)** · MIT licensed

*Two chapters so far: an exactly solvable own-kind sector where **the eldest law
cannot be repealed**, and a second where laws amend each other and it turns out
that **motion is bought with out-degree** — one target buys oscillation, two buy
travel.*

---

## Why this object did not exist

Game theory formalized games with **fixed rules**. Conway deleted the
*players* and got cellular automata and the Game of Life. The orthogonal
deletion — removing the **fixity of the rules** — was never taken, even though
rules that amend rules are humanity's oldest formal practice.

Three independent observations point at the same empty cell:

1. **The deletion grid.** 2-player fixed-rule games (von Neumann–Morgenstern),
   1-player (puzzles), 0-player (cellular automata). Along the *rule-fixity*
   axis: nothing elementary.
2. **The reduction shadow.** Computability's founding move — "without loss of
   generality the program is fixed" — is valid for *what can be computed*
   (universality lets a fixed machine simulate a self-modifying one) but it
   silently discards the *behavioural* question: what do small self-amending
   systems actually **do**? Nobody looked, because the reduction said one need
   not.
3. **The practiced verb.** Constitutions and statutes are self-amending by
   essence and are the oldest running formal systems, yet "amend" was never
   objectified the way Church and Turing objectified "compute." The existing
   fragments — von Neumann's rule-carrying constructor cells, Suber's game
   *Nomic* (1982), self-modifying Petri nets (1978), algorithmic chemistry —
   never produced a minimal canonical object, a census, or a theorem.

## The object, in one definition

> A **law** is a triple `(a, b, c) ∈ {−1,0,1}³` placed at a position `i ∈ ℤ`.
> A **code** is a finite set of placed laws.
> A placed law `(i, (a,b,c))` is **active** iff some law stands at `i+a` and no
> law stands at `i+b`.
> Time is synchronous: every active law flips the presence of **its own kind**
> at `i+c`; simultaneous flips resolve by parity.

There is no board and no external rule table — the law is the only substance.
No parameters. **Nomic rings** are the same system on `ℤ/m`; the
`d`-dimensional and window-`w` versions replace `{−1,0,1}` by offset sets in
`ℤᵈ`.

Reading the guard aloud: *"while my precedent stands and my exception is
vacant, enact/repeal my kind at my target."*

## What is proved

| | |
|---|---|
| **Gridlock** | In a fully occupied region every law's vacancy guard fails: solid code is frozen. All dynamics is surface dynamics. |
| **Single Author** | The only law that can flip kind `k=(a,b,c)` at cell `j` is the kind-`k` law at `j−c`. Hence parity ≡ OR resolution *identically*, in every dimension, and per-kind dynamics is occupancy-modulated linear algebra over `𝔽₂`. |
| **Dead Letter** | A code is a fixed point **iff** every law in it is blocked. *Balanced constitutions* — codes in perpetual self-cancelling activity — do not exist: stability is always gridlock. |
| **Anchor** | On `ℤ` (any window, any dimension, any guard predicate, either resolution) own-kind toggles of kind `t` land only at `t`'s own offset `c_t`; the extremal law on the trailing side of a finite code is therefore never targeted. **The eldest law cannot be repealed** — so free gliders are impossible. |
| **Ring rotors** (corollary) | On `ℤ/m` there is no eldest law and the obstruction genuinely vanishes: three laws of the single kind `(0,1,−1)` at cells `{1,2,5}` of `ℤ/6` hop `m/2` cells per step. *Entrenchment is a theorem of linear order: linear statute books are anchored by their oldest provision; circular codes can revolve.* |

```
t=0  |.XX..X|      X = law (0,1,-1)  ("while I stand and my right is vacant,
t=1  |..X.XX|                          repeal my left")
t=2  |.XX..X|      each step the bloc hops m/2 = 3 cells: Φ(S) = rot₃(S)
```

## Fauna of the solvable sector

* **Colonizers** `(0,1,1)` / `(0,−1,−1)` — the only two single-law growers of
  the 27 kinds; march at speed 1, leaving inert solid code behind.
* **The sunset clause** `(0,−1,1)` — enacts a subordinate whose presence then
  blocks it; period-2 blinker.
* **Sunset codes** `(−1,1,0)` — blocks that dissolve from their newest end.
* **Welds** — colliding fronts fuse into frozen code with a double-law seam.
* **Refraction ≈ 2** — a colonizer meets a sunset wall of length `L` and clears
  it at time exactly `max(2L, x₀+L)`: the wall erodes from its far end on its
  own while the front stands blocked, and the front then fills the vacated
  ground. *The front never converts the wall — it waits for the old code to
  expire and takes the vacancy.*
* **Conversion waves** — speed 2/3, one-way, anchored at a point defect.
* **The Sunset Parliament** — single-kind ring codes with exact maximal periods
  15, 63, **341** at resonant circumferences `m ≡ 2 (mod 4)`: orders of
  `𝔽₂` polynomials governing constitutional cycles.
* **Pinwheel rotors** — 239 certified 2D half-turn rotors.
* **Pascal columns** — growers with `|S_t| = 2^popcount(t)`.
* **The Jubilee Code** — a ~26-law 2D machine, aperiodic through 300,000
  fully-hashed steps, quiescent except on the last tick before each power of
  two, when the whole code ignites — and at `t = 2^k` itself **exactly four laws
  stand**, every time (16/16 exact, complete through `t < 2^17`; crest height
  doubles every second power of two). A binary counter native to law-space, and
  an attractor: 791 of 60,000 random seeds fall into its family.
  Details: `nomos2d/JUBILEE-LAW.md`.

2D own-kind growth obeys a **ray-confinement theorem**: each kind is pinned to
one axis ray, so the plane never fills (measured growth exponent α ≤ 0.99).

## Chapter two: what motion costs

Everything above holds because laws amend only their **own** kind — the tame
simplification. Real law amends *other* law. Generalize minimally: a
**constitution** is a finite kind set `K`, each kind `k` carrying a rule
`(a_k,b_k,c_k)` and a **target set** `T_k ⊆ K`; an active law of kind `k` at `i`
toggles every kind of `T_k` at `i+c_k`. Own-kind is `T_k = {k}`. Nothing
external is added — out-degree 1 makes the amendment digraph a functional graph,
so a kind is a pointed finite graph with a triple at each node (*"I am (a,b,c),
and I amend the law that is (a′,b′,c′) and amends…"*), and own-kind laws are
exactly its self-loops.

The expected escape was cross-kind targeting. It isn't.

| | |
|---|---|
| **Out-Degree Law** | If, restricted to the kinds a pattern uses, every law amends **at most one** kind, no free glider exists — any offsets, any window, any dimension, parity or OR. This *contains* the Anchor Theorem (self-loops), reciprocal amendment, and every permutation constitution of every cycle length. |
| **Supersession no-go** | State-dependent supersession targeting — *enact your own kind on empty ground, clear the whole cell if occupied* — admits no free glider in any dimension: creation is still own-kind, so every kind must push forward, and then nothing can clear the rearmost cell. |
| **Tropical Speed Law** | For a glider of period `p`, displacement `d`: `p·min(λ_min,0) ≤ d ≤ p·max(λ_max,0)`, with `λ` the extreme cycle means of the amendment digraph. Every cycle of weight zero, or an acyclic digraph ⟹ nothing moves. |
| **Balance** | Under parity, two active laws whose enactments cancel leave a code **fixed forever while still alive** — a *balanced constitution*, minimum two placed laws. Under OR none exists at any size: Dead Letter survives that convention verbatim. |

The proofs run on a tropical (min-plus) monovariant `Ψ = min_t(α_t + w_t)` over
the kinds' trailing edges, refined by a tight-cycle argument.

**The threshold is exact — out-degree 2 suffices, and the travellers are tiny:**

| name | what it is | p | d |
|---|---|---|---|
| **SOLO** | *one placed law*, travelling forever; no law in the constitution amends its own kind | 2 | +1 |
| **TANDEM-1** | two laws in a **single cell** at speed 1 — the maximum. Lifts to `ℤ²` at *any* velocity, knight moves included, and revolves on **every** ring `m ≥ 3` | 1 | +1 |
| **TRIPTYCH** | travels under parity; under OR it does not move at all but detonates into a lattice growing 3 laws/step | 1 | +1 |

The cleanest evidence for the law is a controlled experiment: three semantics
sharing guards, offsets and destruction rule exactly, differing only in the
out-degree of the *creation* channel — **0** gliders in 1,119,744 complete
classifications at out-degree 1, **3,424** certified gliders in 279,936 at
out-degree 2.

> **Cross-amendment was never the obstruction; narrowness was.** A law that
> amends a single provision — even somebody else's — can never move. Motion in a
> statute book requires laws that amend several provisions at once. Entrenchment,
> in chapter one a consequence of linear order, is equally a consequence of
> legislative narrowness.

**A warning that came out of chasing that threshold.** Bounded searches decide a
*box*. Every census here used boxes of ≤ ~26 interior cells, and the two-kind
universe `MIRROR` (`W=1`, rules `(0,1,−1)` and `(0,−1,1)`, each amending both
kinds) carries displacement-2 gliders of minimal period 4, 5, 6, 7, 12 with
spans **53, 20, 616, 438, 39** — invisible to every one of those boxes, and all
certified. Sweeps over *coprime* `(p,d)` compound it: they cannot see
`Φ⁴ = σ²` when `Φ² = σ¹` fails. **Read every "decided impossible" in a fixed box
as "no narrow glider".** The theorems above are unaffected — they are proofs,
not box statements — but the speed *spectra* are all narrow-glider statements.

Open: prove the width-free cap that does survive (`|d| ≤ 2` under parity,
`|d| ≤ 1` under OR, in the single-field sector, at any number of channels), and
explain why it does not scale with the window. Is any small cross-amendment
universe computation-universal?

## Repository map

| path | contents |
|---|---|
| `NOMOS.md` | founding document: derivation, definition, and the pre-registered predictions N1–N6, frozen **before** the first simulation |
| `FINDINGS.md` | consolidated findings, corrections, and the pre-registration scorecard |
| `XNOMOS.md` | charter of chapter two (cross-amendment): the general object, the escape lattice, predictions X1–X8, risk clause |
| `xnomos.py` | the shared engine: constitutions with amendment targets, 1D/2D/rings, parity / OR / supersession / multi-target, certificates |
| `verify.py` | the verification battery — re-checks every named claim |
| `nomos2.py` | reference 1D engine (bitmask, 27 kinds) |
| `glider-question/` | the free-glider expedition: `RESULTS.md` (Anchor Theorem, full proofs, hypothesis audit), sweep code, ~15.3M certified classifications in `data/` |
| `xamend1d/` | chapter two on ℤ: the Out-Degree Law and the first gliders — 1,930 SAT decisions, ~24.7bn certified classifications, `demo.py` re-certifies every specimen |
| `XFINDINGS.md` | chapter-two findings and the scorecard against the frozen predictions |
| `rings/` | nomic rings: Single-Author Lemma, Dead Letter Theorem, Sunset Parliament resonances, exact fixed-point counts, Garden-of-Eden algebra |
| `nomos2d/` | two dimensions: ray-confinement theorem, pinwheel rotors, Pascal columns, the Jubilee Code, interaction chart, cross-amendment teaser |
| `note/` | the founding note (LaTeX source, figures, compiled PDF) |
| `demo/` | interactive web demo (single self-contained HTML file) |
| `docs/` | the same demo, published via GitHub Pages |

## Reproducing

Python 3.11 + numpy. No other dependencies.

```sh
python3 verify.py          # re-checks every named claim in this README (~2 s)
python3 verify.py -v       # ...printing each specimen's spacetime diagram
python3 xnomos.py          # engine self-tests
python3 note/figs.py       # regenerate every figure of the note
```

`verify.py` is the point of entry: it re-derives the fauna, the four theorems,
the ring rotors, the Jubilee clock law and the chapter-two specimens from the
shared engine, independently of the expedition code that originally found them.
It runs in CI on every push. Two published descriptions have already been
corrected by it — see the *Corrections* section of `FINDINGS.md`.

Per-expedition code: `python3 nomos2.py` (1D own-kind), `nomos2d/engine2d.py`
(2D), `rings/ring.py`, `glider-question/tests.py`. Each expedition directory has
a `RESULTS.md` whose last section lists the exact commands that regenerate its
data files.

## Method

Definitions and predictions were frozen before the first run (`NOMOS.md` §3),
and every census carries machine-checked certificates: recurrence,
translation-recurrence, and rotation-recurrence witnesses, complete
enumerations where stated (1- and 2-law seeds at `W=1`; ≤4-law/5-cell patterns,
8.1M; ring sweeps `m ≤ 12`), and lockstep parity-vs-OR duels. The Anchor and
Dead Letter theorems have short combinatorial proofs, checked against 15.3M
runs with zero violations. Pre-registration N3 (a glider among small seeds) was
**refuted by a theorem** — the record is kept as found.

## Provenance

Nomodynamics was derived and founded in the **Treeline Program**, a research
program on how mathematics selects its objects — specifically on the mismatch
between where mathematical practice stopped and where the proven dividing lines
actually run. This repository is its Phase 6.

## License

MIT — see [LICENSE](LICENSE).
