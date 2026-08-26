# PRE-REGISTRATION — Expedition X-B (2-D cross-amendment)
Written 2026-08-26, *before* the first census run. Kept verbatim in RESULTS.md.

Paper work done before writing any survey code (see RESULTS.md §2 for the
proofs that these predictions are based on): I derived a displacement-monoid
confinement lemma and a potential/anchor argument on paper first, so several
of the predictions below are "I believe I can prove this", not blind guesses.
They are recorded as predictions anyway, and the ones that were only hunches
are flagged.

## P1 — growth exponent α
- **P1a** (derived): every **single-target** constitution (out-degree 1 —
  own-kind, cross-amendment relay, supersession) has support contained in a
  finite union of *parallel rays*, so **α ≤ 1**, in every dimension. I expect
  the complete 2-kind census to show **zero** universes with α > 1.05.
- **P1b** (derived + construction sketched): **multi-target** (out-degree ≥ 2)
  should reach **α = 2**. My designed candidate is a "sower": kind A is an
  axis colonizer whose bundled target drops a B-law on every cell it takes,
  and B is a transverse colonizer. Predicted |S_t| ~ t²/2.
- **P1c** (hunch, 60/40): apart from α = 1 and α = 2 there will be a
  **fractal band** of intermediate α (Pascal-like multi-target growers) —
  values strictly between 1 and 2 that are *not* fits-artefacts.

## P2 — gliders
- **P2a** (derived): **no gliders** under single-target, any dimension, any of
  parity / OR / supersession. Complete census should find zero.
- **P2b** (derived): the only stratum where the potential argument fails is
  multi-target whose reachable **cycle-sums do not fit in an open half-plane**
  (e.g. two self-loops with antiparallel effect offsets). Predicted: gliders,
  if they exist at all, live only there.
- **P2c** (hunch): I give a certified free glider in that stratum **~25%**;
  a rake/puffer (moving front + periodic debris) **~50%**; a translating
  grower (α ≥ 1 support whose *shape* translates) **~70%**.

## P3 — period spectrum
- **P3a** (hunch, ~65% yes): own-kind periods are locked to 2^k by
  single-authorship + 𝔽₂-linearity. Multi-target destroys single-authorship,
  so I predict **odd periods (3, 5, 6, 7, …) do appear** in the 2-kind
  multi-target census.
- **P3b**: single-target cross-amendment should stay 2-adic (it is still
  single-author per (cell,kind)); if an odd period turns up there I am wrong
  about the mechanism and will say so.

## P4 — balanced constitutions (fixed but active)
- **P4a**: impossible for single-target under **parity** as well as OR?
  — No: I expect them to be **impossible under single-target** (single
  authorship ⇒ a toggle cannot be cancelled) and to require multi-authorship,
  i.e. two distinct kinds pointing at the same (cell, kind). Minimal 2-D
  witness should have **2 placed laws**.
- **P4b** (hunch): balanced codes should be **common** (≥1% of multi-author
  fixed points) and should exist at **large size with rich active sets**.
- **P4c** (hunch, 50/50): balance is fragile — a single added law should break
  it more often than not.

## P5 — semantics
- parity vs OR must split exactly when two authors hit one (cell,kind); the
  census should show a divergence rate of a few per mille among 2-kind
  single-target universes (teaser measured 20/4000 = 0.5%) and **much higher**
  under multi-target.

## Falsifiers
If the complete single-target census produces any α > 1.05, any glider, or any
balanced constitution, the derived claims P1a/P2a/P4a are refuted and the
proofs in §2 are wrong. That is the sharpest test in this expedition.
