# Expedition Y-B — the computation question

*Gate inventory and universality for nomodynamics.  Chapter-three (citation)
sector plus the chapter-two ballistic sector.*

---

## 0. Pre-registration (frozen before the first big run)

Written after reading `README.md`, `XFINDINGS.md`, `CITATION.md` and `xnomos.py`,
after exactly three scratch probes (an AND-NOT guard, an XOR-merge with a
constant, and a one-cell-per-step signal track), and **before** any census,
compiler, circuit, Rule-110 attempt or collision sweep was written.  Kept as
found.

- **B1 — the citation sector is a circuit substrate, and the gates are cheap.**
  The guard `g at i+a ∧ ¬(h at i+b)` is a two-input AND-NOT read at fixed
  offsets, and a target cell that is toggled accumulates by XOR.  I expect
  AND-NOT, XOR, NOT, fan-out and a unit-delay wire all to exist as *one-law*
  gadgets at window 1.  Confidence: high (the three probes already show
  AND-NOT and XOR-merge).
- **B2 — the expensive primitive is not a gate but ASSIGNMENT.**  Toggling
  accumulates; a wire must be cleared before it is rewritten.  Prediction: the
  clean fix is a *self-clearing kind* (rule `(0,0,0)`, target itself, guard
  always true), which converts `x ⊕= f` into `x ← f`.  Confidence ≈ 0.8.
- **B3 — a full synchronous Boolean circuit compiles, at window 1, with a
  fixed finite constitution.**  Prediction: there is a single citation
  constitution on ℤ, with a fixed number of kinds and offsets in `{−1,0,1}`,
  into which an *arbitrary* fan-in-2 Boolean circuit can be laid out as a
  placement of immortal laws.  Confidence ≈ 0.6.
- **B4 — Rule 110 falls.**  Given B3, a Rule-110 cell is a five-gate circuit
  (`q ⊕ r ⊕ qr ⊕ pqr`) and should simulate with a small constant time dilation.
  Confidence ≈ 0.5.  Universality then holds for the class of codes Rule 110's
  own universality proof needs (ultimately periodic backgrounds), **not**
  automatically for finite codes.
- **B5 — the finite-code gap is the real difficulty, and I may not close it.**
  Nomodynamics codes are *finite*.  Simulating a machine with an unbounded tape
  needs hardware that builds itself ahead of the head.  Confidence that a
  self-extending hardware front is built and certified this cycle: ≈ 0.35.
- **B6 — P-completeness falls out cheaply and is the safe floor.**  A circuit
  simulation with log-space-computable layout reduces the Circuit Value Problem
  to nomodynamic prediction.  Confidence ≈ 0.75.  I expect this to be the
  result that survives even if B4/B5 fail.
- **B7 — ballistic gates are *harder*, not easier.**  Against the Life
  intuition: I predict the glider-collision sector yields **absorption and
  reflection readily but fan-out badly**, because chapter two's collision
  parity rule (even gap ⇒ mutual transparency) means colliding writs mostly
  *ignore* each other, and transparency is the enemy of interaction.
  Prediction: ≥ 1 certified reflector, ≥ 1 certified absorber (deleter),
  and **no** certified ballistic fan-out (duplicator) from a bounded sweep.
  Confidence ≈ 0.55.  *(Recorded as a box statement, per the width correction.)*
- **B8 — the single-author sector is NOT provably poly-time predictable, and I
  expect I will fail to prove it.**  Given occupancy, per-kind dynamics is
  𝔽₂-linear — but occupancy is itself the nonlinear part, and occupancy is a
  function of the kind fields.  Prediction: linearity gives a *conditional*
  poly-time algorithm only, and no unconditional non-universality theorem.
  Confidence ≈ 0.7 that the obstruction does not close.
- **B9 — what I do not expect.**  I do not expect a replicator (Y5), I do not
  expect the ballistic sector to reach universality, and I do not expect to
  find any *new* glider.  This expedition is about gates, not fauna.

**The honesty bar I am holding myself to:** a universality claim requires an
explicit constitution, an explicit encoding, an explicit composition argument,
and a machine check of the simulation against an independent reference
implementation.  Anything less is reported as "ingredients present".

---

*(Sections 1 onward are written after the runs.)*
