# Pre-registration — Expedition X-E (displacement quantisation)

Written 2026-08-26, before the first campaign run. Two facts were already in
hand when this was written and are recorded as such (they took one smoke-test
call each, before any experiment was designed):

* **S0 (dilation, proved on paper before any run).** If a constitution with
  window `W` has a glider of period `p` and displacement `d`, then the
  *dilation* `i ↦ r·i` (offsets `(a,b,c) ↦ (ra,rb,rc)`, targets unchanged) has
  a glider of period `p` and displacement `rd` at window `rW`, for every
  `r ≥ 1`. Proof sketch: the dilated seed occupies only cells `≡ 0 (mod r)`,
  every guard and every emission of the dilated rules reads/writes only such
  cells, so the dilated orbit is the image of the original orbit under `i↦ri`.
  Hence **no `W`-independent cap on `|d|` can be true**: `n=2, W=2` already
  realises `(p,d) = (1,2)`. The question must be asked as *"which coprime
  `(p,d)` at each `(n,W)`"*.
* **S1 (smoke test, 0.02 s).** `n=3, W=2, p=3, d=5` is SAT and certified.
  Since `5 > 2·W = 4`, the multiplicative shape `|d| ≤ g(n)·W` is **also**
  dead before the campaign starts.

## Predictions

**R1 — the cap at `n=3, W=1` is real, not a period artefact.**
`|d| ≥ 3` stays UNSAT at `n = 3, W = 1` up to at least `p ≤ 14`, and at boxes
wider than X-A's `N = 16`. Confidence **0.70**. (If `d = 3` appears at some
larger `p`, the phenomenon is a period bound and the report says so.)

**R2 — the correct invariant is not `|d|` but the extreme cycle mean.**
My best guess after S0/S1: the real law is *Theorem 1 plus integrality*. The
edge weights of `D[C]` are the integers `c_k ∈ {−W..W}`, and a cycle of length
`L ≤ n` has mean `(Σc)/L` — **a rational with denominator at most `n`**. So
`d/p ≤ λ_max ∈ {s/L : L ≤ n, |s| ≤ LW}`, and Theorem 2 further demands a
second, non-positive cycle. I predict the observed "displacement cap" is the
shadow of

> `d/p ≤ max{ λ : λ a cycle mean realisable on ≤ n vertices with c ∈ {−W..W},
>              alongside a non-positive cycle }`,

i.e. a **speed** law with denominator `≤ n`, not a displacement law.
Confidence that a denominator-`≤ n` / cycle-mean statement is the core of the
answer: **0.45**. Confidence that `|d| ≤ 2 at n=3, W=1` is *exactly* explained
by it: **0.20** — because I can already see it does not separate `2/5`
(realisable) from `3/5` (not).

**R3 — `n = 2` is rigid: only the extreme speeds.** I predict `n = 2` realises
exactly the coprime pairs `(1, r)` for `1 ≤ r ≤ W` and nothing else: period 1
only. Confidence **0.55**. I expect to be able to *prove* the `n=2` case
(complete case analysis at the front and the rear plus the Twin-Kind Lemma).
Confidence of a proof: **0.55**.

**R4 — the mechanism.** The front advances only via kinds with `c > 0`; the
rear can be cleared only by kinds with `c ≤ 0` (an author repealing the
rearmost law sits at `α − c_k ≥ α`). A glider therefore needs both channels.
Speed **strictly below** the top of Theorem 1's range requires the front to
*stall*, which requires a guard that is sometimes false at the front, which
costs an extra kind — this is why `n = 2` should be extreme-speed-only.
Confidence in the front/rear channel dichotomy as a *proved lemma*: **0.85**;
in it explaining the `n=3` cap: **0.25**.

**R5 — `n = 3, |d| ≤ 2` will not get a full proof from me.** Probability I
produce a complete theorem for `n = 3`: **0.20**. Probability I produce an
exactly-stated conjecture with a complete certified table and the boundary
sharply located: **0.80**.

**R6 — 2-D.** The magnitude cap survives in the form "`n = 2` realises exactly
`p = 1` and `v` with `‖v‖_∞ ≤ W`". Diagonal displacements have no separate
quantisation beyond `‖v‖_∞`. Confidence **0.50**.

**R7 — where I expect to be wrong.** The strangest datum is that the cap
*vanishes* at `n = 4` instead of growing. `|d| ≤ (n−1)W` is already refuted by
X-A (`n=4` reaches `6/7`). I give **0.35** that the honest final statement is
"`n ≤ 3` is a low-complexity accident with two separate small proofs, and there
is no `f(n)`", and **0.30** that a single clean statement covers all `n`.

**R8 — box dependence.** I predict at least one X-A "UNSAT" flips to SAT when
the box is widened (their `(p,d)` sweeps used `N = 16`, interior 14). If so it
matters most for the `n = 3, |d| = 3` frontier. Confidence a flip happens
somewhere: **0.30**.
