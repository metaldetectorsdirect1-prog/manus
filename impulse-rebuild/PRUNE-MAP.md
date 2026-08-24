# PRUNE-MAP.md

Blog prune, Track A §3.2. **Steps 1–2 complete. Stopped at step 3 (verify).**

The owner's sequence is: pull 331 redirects → **build map checking for conflicts**
→ **verify** → create redirects → delete in batches → repoint survivors' links.

Steps 1 and 2 are done and committed as data files. Step 3 is a gate, and this
document is what goes through it. **No article has been deleted.**

---

## §1 Status

| Step | State |
|---|---|
| 1. Pull all redirects | ✅ 331 pulled, reconciled — `LEGACY-AUDIT.md` §2.1 |
| 2. Build map, check conflicts | ✅ this document + `prune/` data files |
| 3. **Verify** | ⏸ **gate — needs owner confirmation of the survivor line (§5)** |
| 4. Create redirects | not started (11 of them already done — see §6) |
| 5. Delete in batches | **not started** |
| 6. Repoint survivors' links | not started |

---

## §2 Method, and what it does not cover

| | |
|---|---|
| **Corpus** | 501 handles, full enumeration, 3 paginated reads. `prune/articles-501.txt` is 501 lines, 501 unique, 0 duplicates — matches `blog.articlesCount: 501` exactly |
| **Classifier** | `prune/classify.py` — deterministic, re-runnable, rules written in the file |
| **Classifies by** | **handle keyword only. It does not read article bodies.** |
| **Traffic** | Shopify `sessions GROUP BY landing_page_path`, 90 days, measured |
| **Traffic is a floor** | The analytics API caps at 250 rows. Both the DESC and ASC windows truncated, so an article showing 0 sessions here may have had 1. Nothing in the map turns on the difference between 0 and 1. |

**Self-audit (§1.8).** The first classifier run produced two false positives, caught
by reading its own output: `lint` matched inside "sp**lint**s"
(`shin-splints-prevention…`), and `-dry` matched `rainy-day-athleisure-staying-**dry**…`.
Both rules were tightened and both articles moved to delete. This is why the
classifier is a committed script and not a judgement call — the error was findable.

---

## §3 What the corpus actually is

501 articles, all published inside 13 days (`BLOG-AUDIT.md`). By handle keyword:

| Category | n | Disposition |
|---|--:|---|
| **"Best X for Y" product round-ups** | **142** | delete — they recommend products from a catalog that holds **zero** products |
| Training, exercise, nutrition, gym myths, motivation | ~200 | delete — no relationship to a clothing store |
| Styling and outfit formulas | ~80 | delete — activewear styling, off-brief |
| **Garment care · fabric science · sizing and fit** | **73** | **keep — category-neutral** |
| Traffic outliers outside those 73 | 6 | keep — see §5 |

The 73 are the only part of the corpus that transfers unchanged to a general
women's clothing store: how to wash a knit, what GSM means, how a sports bra
should fit, why leggings bag out. None of it depends on what is in the catalog.

---

## §4 The numbers

| | |
|--:|---|
| **501** | articles |
| **79** | survivors |
| **422** | deletions |
| 84.2% | of the corpus deleted |
| **56.2%** | of measured blog traffic **retained** (127 of 226 sessions/90d) |
| 226 | sessions across live articles in 90 days — the whole blog is a rounding error next to 4,458 site sessions |

Files: `prune/survivors.txt` (79) · `prune/deletions.txt` (422) ·
`prune/prune-map.json` · `prune/articles-501.txt` (501). 79 + 422 = 501.

---

## §5 🟠 The one decision that is the owner's

**Two defensible rules disagree, and they disagree about the biggest page.**

`hot-yoga-outfits-what-survives-105-degrees` is the **single highest-traffic blog
article on the site** — 23 sessions in 90 days, about 10% of all blog traffic.
The category rule **deletes** it: hot yoga outfits is activewear styling, which is
off-brief for a general women's clothing store.

Six articles sit in that gap — measured traffic ≥4 sessions, but off-category:

| Sessions | Handle |
|--:|---|
| 23 | `hot-yoga-outfits-what-survives-105-degrees` |
| 9 | `bulgarian-split-squats-why-they-hurt-and-why-they-work` |
| 7 | `best-gym-clothes-that-hide-sweat` |
| 4 | `best-color-block-activewear-bold-without-clashing` |
| 4 | `breathing-while-running-rhythms-that-prevent-side-stitches` |
| 4 | `what-time-is-the-gym-least-busy-data-backed-windows` |

**The map recommends keeping all six** — the union of both rules. Keeping an
article is reversible; deleting one is not, and these six carry 44 of the 226
measured sessions. That is the recommendation, not a decision taken.

**Three options, and the owner picks one:**

| | Survivors | Deletions | Traffic retained |
|---|--:|--:|--:|
| **A — recommended: category ∪ traffic** | 79 | 422 | 56.2% |
| B — category rule only | 73 | 428 | 33.6% |
| C — `BLOG-AUDIT.md`'s original plan | ~13 | ~488 | ~25% |

**Option C is no longer supportable.** It was designed from a 26-article sample
that `BLOG-AUDIT.md` itself flagged as too thin. Measured traffic is now available
for the whole corpus, and it shows 112 live articles earning sessions, not 13.

---

## §6 Conflict check — clean

**Redirect ↔ article collisions: zero.**

The only redirects in the `/blogs/news/*` namespace are 15, and **every one of
them points at a handle that is not in the 501-article corpus** — they are the
already-deleted perfume articles. No live article has a dormant redirect waiting
to fire at its own path.

Checked by exact-path query with a working control (a known redirect returned,
three checked paths returned empty). The `path:*wildcard*` filter form does **not**
work on this API and silently returns 0 — it was not used for any conclusion here.

### The `/de/` arm needs no work

170 `/de/blogs/news/*` → `/blogs/news/*` redirects already exist
(`LEGACY-AUDIT.md` §2.2). After an English article is deleted:

```
/de/blogs/news/X  →  /blogs/news/X  →  /blogs/news
```

Two hops, resolves, no orphan. **No second locale arm has to be built.** This was
the single largest unknown in the prune's cost and it is answered.

### Already done: 11 redirects created 2026-08-24

Eleven perfume-article URLs were taking measured traffic — 23 sessions in 90 days
— to **hard 404s**: no article, no redirect. They now redirect to `/blogs/news`,
matching the handling of the four that already had redirects.

Verified independently: redirect count 331 → **342** (+11 exactly), and four spot-
checked paths read back with the correct target. `userErrors: []` was not treated
as proof.

---

## §7 Execution plan, once the gate clears

Aliased batch mutations are **proven to work on this connector** — 11
`urlRedirectCreate` calls executed in a single request on 2026-08-24. That makes
the prune far cheaper than `BLOG-AUDIT.md` assumed.

| Batch | Calls | Note |
|---|--:|---|
| Create 422 redirects, 50/call | 9 | Order matters: **redirects first.** A redirect is dormant while the article exists and activates the moment it is deleted, so there is never a window with a live 404. |
| Verify | 1 | `urlRedirectsCount` must read **764** (342 + 422) |
| Delete 422 articles, 50/call | 9 | re-read `articlesCount` after each batch |
| Verify | 1 | `articlesCount` must read **79** |

**~20 calls total.** `BLOG-AUDIT.md` deferred the prune on the belief this was a
batch job too large for one session. With aliased mutations it is not.

**Abort rule:** if any batch returns a mismatch between expected and actual count,
stop and reconcile before continuing. A partial delete with complete redirects is
recoverable; a partial delete with partial redirects is the failure mode the
owner's safety rule names.

---

## §8 Why this stopped here and not further

Not budget — budget is ample, and §7 shows the work is about twenty calls.

It stopped because **step 3 of the owner's own sequence is "verify"**, and the
thing needing verification is the survivor line in §5. Deleting an article is
irreversible. The previous survivor set was built from a 26-article sample; this
one is built from the full corpus and measured traffic, and it disagrees with the
old one about the site's most-visited blog page.

Everything reversible has been done: the map is built and committed, the conflict
check is clean, the `/de/` question is closed, and the 11 live 404s are fixed.
The only thing left is the irreversible part, and it is one confirmation away.
