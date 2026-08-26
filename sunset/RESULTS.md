# Impermanence — nomodynamics when laws expire

### Coordinator's expedition, 2026-08-26
*Every chapter so far assumed a law stays in force until something repeals it.
The semantic sweep of chapter two found that this assumption, not own-kind
targeting, is what forbids motion on the line. This is the sector where it is
dropped.*

## 1. The object

> **Sunset-by-default.** A law lapses unless it is re-enacted. With lifetime
> τ ≥ 1, a placed law survives a step if some active law enacts it now, or if
> fewer than τ steps have passed since its last enactment. Effects are
> **enactments**, not toggles: an active law of kind k at i enacts every kind of
> T_k at i + c_k. To repeal is simply to stop re-enacting. Guards are as before,
> occupancy or citation.

τ = 1 is the pure form: *only what is enacted now stands next.* Engine and
self-tests: `sunset.py` (`python3 sunset/sunset.py`).

Reading it aloud: **every provision carries a sunset clause, and a statute book
persists only by continually re-enacting itself.**

## 2. The lone-survivor theorem

**Theorem (Lone Survivor).** *Under τ = 1, a single placed law of kind (a,b,c)
survives its first step iff a = 0 and b ≠ 0 — its precedent is itself and its
exception is elsewhere. It then translates by c forever: it **walks** at speed 1
if c ≠ 0, and **renews itself in place** if c = 0. The other 21 of the 27 kinds
vanish in one step.* [established]

*Proof.* With only cell 0 occupied, occ(0+a) = 1 iff a = 0 and occ(0+b) = 0 iff
b ≠ 0, so the law is active exactly then; being active it enacts its kind at c
and nothing else is enacted, so S₁ = {c}, a single law again, and translation
invariance repeats the argument. If it is not active nothing is enacted and
S₁ = ∅. ∎

Verified by complete enumeration of all 27 kinds: 21 extinct, 4 gliders
(a = 0, b = ±1, c = ±1), 2 fixed (a = 0, b = ±1, c = 0).

**The walking clause.** The colonizer (0,1,1) — chapter one's first specimen,
which fills the line and leaves inert code behind it — becomes, under
impermanence, a single law that simply *walks*:

```
permanence           impermanence
 t=0  A.....          t=0  A.....
 t=1  AA....          t=1  .A....
 t=2  AAA...          t=2  ..A...
 t=3  AAAA..          t=3  ...A..
```
Same law, same guard, same target. The Anchor Theorem forbids the right-hand
column in every own-kind variant of chapters one and two; its hypothesis of
**locality** — a slot receiving no toggle is unchanged — is exactly permanence.

## 3. Gridlock's mirror

Under permanence a solid code is **frozen**: every vacancy guard fails, and
*all dynamics is surface dynamics*. Under impermanence a solid code
**evaporates**: nothing in the interior is re-enacted. A block of eight
colonizer laws collapses in a single step to one walking law:

```
 t=0  .AAAAAAAA....
 t=1  .........A...
 t=2  ..........A..
```

> In both worlds only the surface matters. Under permanence it is the only part
> that **moves**; under impermanence it is the only part that **lives**.

## 4. The Longevity Law — speed 2/(τ+1)

The lifetime τ is a dial, and it turns out to set the speed of a packet directly.
One two-kind code — kinds `A = (0,1,−1)` and `B = (0,−1,−1)`, both own-kind,
seeded `A` at 0 and `B` at 2 — travels at speed exactly

> **|d| / p = 2 / (τ + 1)**

with displacement always 2 and only the period changing. Certified over three
full periods at every τ = 1…12 (τ=1 degenerates to p=1, d=−1):

| τ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| speed | 1 | 2/3 | 1/2 | 2/5 | 1/3 | 2/7 | 1/4 | 2/9 | 1/5 | 2/11 | 1/6 | 2/13 |

```
τ = 2, speed 2/3                τ = 4, speed 2/5   (same code, same seed)
 |.......AABB..|                 |...........AABB..|
 |.......A.B...|                 |...........AABB..|
 |......A.B....|                 |...........AABB..|
 |.....AABB....|                 |...........A.B...|
 |.....A.B.....|                 |..........A.B....|
 |....A.B......|                 |.........AABB....|
 |...AABB......|                 |.........AABB....|
```
The packet dwells while its tail is still standing, then makes the same
two-cell move. **Longevity is friction.** As τ → ∞ the speed tends to 0, and in
the limit of true permanence the packet cannot move at all: *the Anchor Theorem
is the τ → ∞ limit of this family.* [original proposal — the table is complete
and certified through τ = 12; the general formula is fitted, not proved.]

Three speed families appear in the complete two-law box at τ = 6: speed **1**
(τ-independent), **1/τ**, and **2/(τ+1)**, with witnesses in `sunset.py`'s
census. The founding sector's motionlessness is thus not a knife edge but the
endpoint of a continuum.

## 5. Census — the statistics invert

Complete two-law box: both kinds ranging over all 27, seeds `A@0`, `B@span` for
span 0…4, i.e. **3,645 codes per lifetime**, step budget 160, card/span budget
200.

| τ | extinct | fixed | glider | growing | unresolved |
|---|---|---|---|---|---|
| 1 | 2360 | 412 | **814** | 29 | 30 |
| 2 | 2309 | 410 | **850** | 23 | 53 |
| 3 | 2311 | 410 | **838** | 31 | 55 |
| 4 | 2313 | 410 | **836** | 21 | 65 |
| 6 | 2313 | 410 | **836** | 15 | 71 |
| 10 | 2313 | 410 | **836** | 15 | 71 |

Two inversions against the permanent world, where gliders are *impossible* in
the entire own-kind sector and freezing is the generic fate:

* **Extinction is the default** (≈ 64 %), where under permanence it was gridlock.
* **Motion is generic** (≈ 23 % of two-law codes at every lifetime tested),
  where under permanence it was a proved impossibility.

## 6. Why, structurally

Chapter two's no-go runs on a tropical monovariant over the kinds' trailing
edges, and its recursion is

  supp_t(n+1) ⊆ supp_t(n) ∪ (supp_s(n) + c_s).

The first term — *the support persists* — is a **weight-0 self-loop** in the
tropical digraph, and a weight-0 self-loop is exactly what pins the minimum and
forbids the trailing edge from advancing. Impermanence deletes that term. The
digraph loses its zero-loops, the cycle means can be strictly positive, and
motion is permitted.

> **Permanence is the zero-loop.** Chapter two's Out-Degree Law and chapter
> one's Anchor Theorem both trace back to the same term in the same recursion,
> and impermanence removes it. [interpretation, consistent with every
> measurement here]

## 7. Status and scope

Complete enumerations: all 27 single-kind laws; the 3,645-code two-law box at
each of six lifetimes (21,870 classifications). Certificates: every glider
re-verified over three full periods from its settled state by
`verify_glider_sunset`, an independent code path from `classify_sunset`. The
Longevity table is complete and certified through τ = 12.

**A correction made in flight, recorded as the program requires.** The first
version of `classify_sunset` checked translation certificates only at τ = 1,
which reported **zero** gliders at every τ ≥ 2 and a large unresolved bucket — I
briefly had a "sharp transition at τ = 1" that was an artefact of my own
classifier. Normalising the age map along with the state fixed it, and the true
picture (motion generic at every lifetime, with speed set by τ) is the better
result. As with the width correction of chapter two, a box result was
masquerading as a fact about the world.

**Repro.** `python3 sunset/sunset.py` (self-tests); the censuses and the
Longevity table are the scripts quoted in §4–§5 of this document, and the four
headline facts are checks in the field battery, `python3 verify.py`.
