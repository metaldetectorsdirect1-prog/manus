# Leggings price ladder — 2026-08-09

Twelve leggings and yoga pants all sat at $54 while their published fabric
weights ranged from 200 to 270 g/m². A shopper had no way to choose between
them, and the store's entire proposition — that the number is the thing worth
knowing — did no commercial work at all. If the number does not change the
price, it is decoration.

Price is now a function of fabric weight.

| g/m² | Price | Products |
|---|---|---|
| 200 | $49 | `women-s-faux-denim-zip-fly-leggings` |
| 220 | $54 | topstitching, high-rise yoga pants, high-rise flared, high-waisted ankle, high-waisted flare, solid high-rise |
| 230 | $59 | `womens-high-rise-ankle-length-leggings` |
| 240 | $59 | `womens-flared-drawstring-yoga-pants` |
| 250 | $64 | `womens-color-block-yoga-leggings` |
| 270 | $69 | `womens-high-rise-ankle-length-yoga-leggings` |

Five products moved (25 variants), one down and four up. Seven were already on
their rung and were left alone.

| Handle | Was | Now | Cost | Margin |
|---|---|---|---|---|
| `women-s-faux-denim-zip-fly-leggings` | $54 | **$49** | 16.98 | 65.3% |
| `womens-high-rise-ankle-length-leggings` | $54 | **$59** | 11.97 | 79.7% |
| `womens-flared-drawstring-yoga-pants` | $54 | **$59** | 16.98 | 71.2% |
| `womens-color-block-yoga-leggings` | $54 | **$64** | 18.97 | 70.4% |
| `womens-high-rise-ankle-length-yoga-leggings` | $54 | **$69** | 16.98 | 75.4% |

Every one clears the 60% margin floor recorded in `pricing.py`. The single
reduction is deliberate: 200 g/m² is genuinely the lightest thing in the range
and now has an entry price to match, which gives the ladder a bottom rung.

## The one product that breaks the ladder

`womens-high-rise-flared-yoga-pants` is 220 g/m² but stays at **$59** rather
than dropping to $54, because its unit cost is $21.97 against $14.98–16.98 for
every other 220 in the range. At $54 it would return 59.3%, under the floor.

That is a sourcing problem wearing a pricing problem's clothes. It was already
on the list of badly-costed products flagged in `STORE-AUDIT-2026-08-08.md`;
this is what that costs in practice — one visible inconsistency in an otherwise
legible ladder. The fix is cheaper supply, not a cheaper price.

## Knock-on corrections

Raising the 230 g/m² leggings to $59 made three existing claims false. All
three were corrected in the same session:

- `womens-training-set-bra-ankle-leggings` advertised **$92** bought
  separately. The set contains that legging, so the true separate total is now
  **$97**. `compareAtPrice` updated across all four variants — an uncorrected
  compare-at is a false savings claim, not a stale number.
- `scripts/tiktok-film.py`, film `spec` — stated "$54 · free US shipping" for
  that exact product. Now $59.
- `scripts/tiktok-carousel.py` — slide 3 stated Price $54. Now $59.

The `weights` film opened on "Three pairs. All $54.", which the ladder made
untrue outright. Rather than patch the number it was rebuilt around the ladder
itself — "Three pairs. Three prices." with each weight carrying its price, and
closing on "The number sets the price." The film is stronger for it: it now
demonstrates the proposition instead of asserting it.

## Reversal

Every previous price was $54 except `womens-high-rise-flared-yoga-pants`
($59, unchanged). To revert, set the five products above back to $54 and
restore the set's `compareAtPrice` to $92.
