# Nomodynamics

**The mathematics of self-amending law.** A minimal, parameter-free dynamical
system whose only substance is laws acting on laws — and the first census,
theorems, and fauna of the resulting universe.

📄 **[The founding note (PDF)](note/nomodynamics.pdf)** · 🖥 **[Live demo](https://lukacslacko.github.io/nomodynamics/)** · MIT licensed

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
* **Refraction ≈ 2** — a colonizer assimilates a sunset wall at half speed.
* **Conversion waves** — speed 2/3, one-way, anchored at a point defect.
* **The Sunset Parliament** — single-kind ring codes with exact maximal periods
  15, 63, **341** at resonant circumferences `m ≡ 2 (mod 4)`: orders of
  `𝔽₂` polynomials governing constitutional cycles.
* **Pinwheel rotors** — 239 certified 2D half-turn rotors.
* **Pascal columns** — growers with `|S_t| = 2^popcount(t)`.
* **The Jubilee Code** — a ~26-law 2D machine, aperiodic through 300,000
  fully-hashed steps, quiescent except at `t = 2^k` when the whole code ignites
  (~770 laws) and collapses back to a handful. A binary counter native to
  law-space — and an attractor: 791 of 60,000 random seeds fall into its family.

2D own-kind growth obeys a **ray-confinement theorem**: each kind is pinned to
one axis ray, so the plane never fills (measured growth exponent α ≤ 0.99).

## The frontier, located by theorem

Everything above holds because laws amend only their **own** kind — the tame
simplification. Real law amends *other* law, and by the Single-Author Lemma
**cross-amendment** is precisely the escape from the solvable sector.
Charted escape lattice: state-dependent targeting (*supersession*),
permutation targeting with a fixed-point-free cycle (*reciprocal amendment*),
multi-target laws, and leaving `ℤ` (rings — where rotors already exist).
First probes confirm the door is real: parity and OR genuinely diverge there,
odd periods appear, and diagonal motion — impossible under ray confinement —
unlocks in 2D.

Open: does cross-amendment admit a free glider on `ℤ`, or does a deeper no-go
extend? Is any small cross-amendment universe computation-universal?

## Repository map

| path | contents |
|---|---|
| `NOMOS.md` | founding document: derivation, definition, and the pre-registered predictions N1–N6, frozen **before** the first simulation |
| `FINDINGS.md` | consolidated findings and pre-registration scorecard |
| `nomos2.py` | reference 1D engine (bitmask, 27 kinds) |
| `glider-question/` | the free-glider expedition: `RESULTS.md` (Anchor Theorem, full proofs, hypothesis audit), sweep code, ~15.3M certified classifications in `data/` |
| `rings/` | nomic rings: Single-Author Lemma, Dead Letter Theorem, Sunset Parliament resonances, exact fixed-point counts, Garden-of-Eden algebra |
| `nomos2d/` | two dimensions: ray-confinement theorem, pinwheel rotors, Pascal columns, the Jubilee Code, interaction chart, cross-amendment teaser |
| `note/` | the founding note (LaTeX source, figures, compiled PDF) |
| `demo/` | interactive web demo (single self-contained HTML file) |
| `docs/` | the same demo, published via GitHub Pages |

## Reproducing

Python 3.11 + numpy. No other dependencies.

```sh
python3 nomos2.py                  # 1D engine, first-contact specimens
python3 nomos2d/engine2d.py        # 2D engine self-tests
python3 rings/ring.py              # ring engine
python3 glider-question/tests.py   # Anchor-Theorem test battery
```

Each expedition directory has a `RESULTS.md` whose last section lists the exact
commands that regenerate its data files.

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
