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

## 7. Conservation — and the same threshold, dual consequence

**Theorem (Conservation under impermanence).** *With τ = 1 and every law
amending at most one kind, |S_{t+1}| ≤ |active(S_t)| ≤ |S_t|: the population
never increases.* [established]

*Proof.* Under τ = 1 the next state is exactly the set of slots enacted this
step. Each active law enacts one slot (out-degree 1), distinct laws may enact
the same slot, and nothing else survives. ∎

Verified over 160,000 steps of random out-degree-1 codes: no increase, ever.
With out-degree 2 growth appears at once — 289 of 2,000 random two-target codes
grew. So:

| | permanence | impermanence |
|---|---|---|
| **out-degree ≤ 1** | no motion (Out-Degree Law) | no growth (Conservation) |
| **out-degree ≥ 2** | gliders exist | growth exists |

*The same threshold governs both worlds, with dual consequences.* A law that
amends a single provision cannot move a permanent code and cannot enlarge an
impermanent one. [interpretation]

**The frontier without the territory.** `LAND GRANT` — the one-law code whose
population is exactly (t+1)², the specimen that showed the plane can be filled —
becomes, under impermanence, exactly **two edges of that square**: the top row
and the right column, |S_t| = 2t+1.

```
 t = 8, permanence: the solid square      t = 8, impermanence: its two edges
        ########                                 ########
        ########                                 .......#
        ########                                 .......#
        ########                                 .......#
        ########                                 .......#
```
The settled interior is precisely what impermanence erases; what survives is the
frontier where enactment is still happening.

## 8. Any dimension, and genuine ring transport

**Theorem (Lone Survivor, general form).** *In any dimension, under τ = 1, a
lone law of kind (a,b,c) survives iff a = 0 and b ≠ 0, and it then translates by
exactly **c** per step: its velocity **is** its target offset.* [established]

Complete verification over all 729 single-kind laws on ℤ²: 657 die immediately,
**64 walk with velocity exactly c**, 8 renew themselves in place (c = 0), zero
violations. The 64 include every diagonal — and own-kind permanence forbids
diagonal motion outright, since ray confinement pins all growth to axis rays and
the Anchor Theorem forbids translation altogether.

**Rings.** A single colonizer law circulates a ring, one cell per step, on every
ℤ/m for m = 2…15, odd and even alike. Since min(r, m−r) = 1 ≤ p = 1, this is
**inside the light cone**: genuine transport, not the barber pole of chapter one
(where Φ(S) = rot_{m/2}(S) held while only two cells changed and nothing
travelled). So there are exactly two known routes to real transport on a ring:

* wrap a cross-amendment glider (out-degree ≥ 2), or
* make the laws impermanent — where a *single* own-kind provision goes round.

## 9. Status and scope

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
