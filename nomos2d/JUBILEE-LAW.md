# The Jubilee Code: the exact clock law

*2026-08-26, found while cross-validating the general engine (`xnomos.py`)
against the chapter-one specimens. Sharpens the founding note's "quiescent
except at t = 2^k, when the whole code ignites and collapses".*

Specimen (unchanged): three kinds on ℤ², compass E = (1,0), W = (−1,0),
N = (0,−1), S = (0,1); own-kind amendment, parity resolution.

| kind | guard "some law at" | guard "no law at" | enacts its kind at |
|---|---|---|---|
| ESN | E | S | N |
| SNS | S | N | S |
| WNE | W | N | E |

Seed: ESN at (−1,0), SNS at (−1,1), WNE at (0,1). `|S_t|` = laws in force after
`t` steps (`|S_0| = 3`).

## Measured (complete, t < 2^17 = 131 072; `note/figs.py`, `xnomos.py`)

**(1) The reset.** `|S_t| = 4` at **every** power of two, t = 2, 4, 8, …, 2^16 —
sixteen for sixteen, exact. The code does not merely quiet down at a power of
two: it stands at exactly four laws.

**(2) The crest.** The avalanche peaks one tick *earlier*, at t = 2^k − 1 — the
moment the counter is full — and its height doubles every **two** powers of two:

| k | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| \|S_{2^k−1}\| | 7 | 8 | 13 | 14 | 25 | 26 | 49 | 50 | 97 | 98 | 193 | 194 | 385 | 386 | 769 |

i.e. `|S_{2^k−1}| = 3·2^{⌊(k−1)/2⌋} + 1` for odd k and `+ 2` for even k — so the
ignition grows like √t, not like t.

**(3) The grading.** Population is graded by the **binary weight** w(t) of the
time index, not by t itself:

* `min{|S_t| : w(t) = w} = w + 3` for w ≤ 9 (then 14, 19, 30, 53, 100, 195, 386, 769);
* `max{|S_t| : w(t) = w} = 2^{w/2+1} + 1` for even w and `3·2^{(w−1)/2} + 1` for odd w.

The record-holders are the *nearly*-all-ones times; the all-ones time 2^w − 1 is
the maximum in its class for odd w only.

## Reading [interpretation]

The founding note's phrasing is right but coarse. Precisely: **the jubilee falls
due on the last tick before each power of two, and at the power of two itself
the code always stands at exactly four laws.** The Jubilee Code is a binary
counter whose *displayed* quantity is the weight of the counter word — the same
2-adic grading that governs the Pascal-column growers (`|S_t| = 2^popcount(t)`)
of the own-kind sector, here filtered through a bounded, self-resetting machine.

## Status

Measured, complete over t < 2^17, by two independent engines
(`nomos2d/engine2d.py` originally, `xnomos.py` here). The formulas in (2) and
(3) are **original proposals** fitted to complete data over that range, not
theorems; the reset law (1) is exact over the range checked and is the natural
first target for a proof. Aperiodicity through 300 000 steps and the attractor
statistic (791/60 000 random seeds) are as reported in `RESULTS.md`.

Repro: `python3 note/figs.py fig3` (prints the avalanche audit), or the script
block in this directory's `RESULTS.md` §5.
