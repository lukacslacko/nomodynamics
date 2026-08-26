# Expedition Y-D — closing the open conjectures

*Four named targets, all measured-but-unproved when this expedition opened.
Repo: `/Users/lukacs/claude/math/program/phase6`. Engine: `xnomos.py`.*

---

## 0. Pre-registration

**Frozen 2026-08-26, before the first big run of this expedition.** Written
after reading `README.md`, `XFINDINGS.md`, `nomos2d/JUBILEE-LAW.md`, and after
one small orienting run on the Jubilee specimen (16 384 steps, which established
that the Jubilee's kinds 0 and 1 are frozen singletons and that the code lives on
three axis rays — recorded here so the record shows what was already known when
the predictions were made). Nothing else had been run.

| # | prediction | confidence |
|---|---|---|
| **Y1** | The Jubilee reset law `\|S_{2^k}\| = 4` is a **theorem** and will be proved this expedition. The route is the ray reduction plus an inductive/renormalisation argument on the binary expansion of `t`. | 80 % |
| **Y2** | The crest formula `\|S_{2^k−1}\| = 3·2^{⌊(k−1)/2⌋} + 1/2` will also fall, but is harder than the reset law (it needs the *whole* profile at `2^k − 1`, not just its weight). | 55 % |
| **Y3** | The weight grading (min = `w+3` for `w ≤ 9`, max formula) will **not** fall completely; the min half is a finite claim of a different character from the max half, and I expect at best one half plus a sharpened conjecture. | 35 % for a full proof |
| **Y4** | The Jubilee/Odometer "four laws" coincidence is **not** a conjugacy of the two machines. My prediction: both reduce to a one-dimensional carry automaton, and `4` is forced *separately* in each by the same mechanism — a fixed overhead of frozen/boundary laws plus a weight-1 counter word. I.e. it is a **normal form, not an isomorphism**: the shared cause is "binary counter with a constant frame", and the constant happens to be 4 in both. | 60 % that the two machines are NOT conjugate; 50 % that a common renormalisation is nevertheless exhibited |
| **Y5** | The width-free speed cap (Target 3) will **not** be proved outright. I expect the OR half (`\|d\| ≤ 1`) to be provable and the parity half to survive as a sharpened conjecture. The Dilation tension will be resolved (I predict: dilation does **not** preserve the single-field sector, because spreading one cell into `r` cells changes which cells are occupied and hence the guards). | 30 % full cap, 75 % dilation tension resolved |
| **Y6** | Target 4's converse — *every light-cone-admissible ring rotor is a wrapped ℤ glider* — is **true with a vacancy hypothesis and false without it**. I predict a counterexample exists on a ring with no vacant arc (a fully-occupied or nearly-fully-occupied ring code that rotates inside its light cone without lifting to a finite ℤ glider). | 65 % |
| **Y7** | No target will require a new engine: everything will be checkable through `xnomos.Const/step`. | 90 % |

**Risk clause.** If a "measured" claim in the source documents turns out to be
false as stated, the correction is the result and is reported as such, in the
manner of `XFINDINGS.md`'s two self-caught errors.

**Honesty labels used throughout**: *[established]* = proved here or previously,
*[interpretation]* = a reading of established facts, *[original proposal]* = a
conjecture or a fitted formula, not a theorem. A proof sketch is labelled
**sketch** and is never called a proof.

**The width correction applies**: every bounded search below decides a box, and
the box's parameters are stated with the count.

---
