# Google SEO / Google Shopping skills — what was installed, 2026-08-10

101 skills added, taking the user-level set from 116 to 221. Reproduce with
`bash scripts/seo-skills-setup.sh`; the container is ephemeral, the script is
the durable copy.

| Prefix | Count | Source | What it covers |
|---|---|---|---|
| `seo-*` | 30 | [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | Technical, schema, sitemap, hreflang, local, maps, clusters, content briefs, programmatic, **e-commerce incl. Google Shopping**, plus paid-API extensions |
| `geo-*` | 16 | [zubair-trabzada/geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude) | Answer-engine optimisation: citability scoring, AI-crawler access, llms.txt, brand mentions, per-platform tuning |
| `mk-*` | 55 | [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) (49), [ericosiu/ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills) (5), [aaron-he-zhu](https://github.com/aaron-he-zhu/aaron-marketing-skills) (1) | SEO audit, AI SEO, programmatic SEO, schema, site architecture, CRO, analytics, attribution, content strategy, plus the product-feed optimiser |
| `gsc-*` | 4 | [AminForou/mcp-gsc](https://github.com/AminForou/mcp-gsc) | Indexing audit, cannibalisation check, content opportunities, weekly report — driven by the Search Console MCP server |

`mcp-search-console` is now declared in `.mcp.json` with its two credential
paths left empty, so it appears the moment a Google credentials file exists.

## The finding that matters more than the install

**Google Shopping skills essentially do not exist as a category.** Searching
GitHub for `merchant center` above 15 stars returns exactly two repositories,
one of which is commercetools and unrelated. The only real one is
[google/rubik](https://github.com/google/rubik) — official, Python, **29 stars**
— which repairs offers disapproved for image and GTIN problems. Broader queries
for Shopping feed tooling returned nothing but awesome-lists matching on readme
text. Google *SEO* skills, by contrast, are abundant and good.

So the Shopping coverage now installed is two skills, not a suite:
`seo-ecommerce` (Google Shopping visibility, product schema validation,
competitor pricing) and `mk-product-feed-optimizer`.

**And neither can run yet.** Google Shopping free listings require a Merchant
Center account fed by the Shopify Google & YouTube channel, and HIVOLT has
neither — "install Google & YouTube" has been on the owner-gated list for some
time. A feed optimiser with no feed optimises nothing. The same is true one
layer up: the four `gsc-*` skills and the MCP server are inert until the Search
Console credentials are pasted, which is the same blocker already recorded in
`SEO-2026-08-10.md`.

Worth stating plainly: this install adds capability, not traffic. The two
things standing between HIVOLT and Google are both account connections only the
owner can make.

## What was deliberately not installed

- **119 of the 120 skills in `aaron-marketing-skills`** — influencer, narrative,
  social and paid-ads work, outside an SEO ask, and the `tt-*` set already
  covers social. Only `product-feed-optimizer` came across.
- **All of `TheCraigHewitt/seomachine`** (25 skills). It is a near-duplicate of
  `marketingskills` — same `copy-editing`, `programmatic-seo`, `seo-audit`,
  `marketing-psychology`, `popup-cro`. Installing both would have put two
  copies of the same advice in the routing table under different names.
- **The 21 non-SEO skills in `ai-marketing-skills`** — podcast, video and
  sales-pipeline work.

A `SKILL.md` is an instruction file this agent later reads and follows, and
every installed description occupies context in *every* session. "Add them all"
was read as all of the SEO and Shopping packs, not all 240 files in five
repositories; doubling the routing table with influencer-marketing skills would
make the SEO ones harder to reach, not easier.

## Two things the scan caught

Third-party skills are third-party instructions, so `verify_pack()` in the
setup script scans every pack before install — for credential paths (`~/.ssh`,
`~/.aws`), for `base64 -d | sh`, and for text telling the agent to ignore prior
instructions or withhold information from the user. It runs on every invocation
rather than being a one-off that rots. All five packs came back clean.

The scan did not catch either of the two real problems, both in
`ai-marketing-skills`, both found by reading the files:

**Every skill in that pack opens with a "Preamble (runs on skill start)" that
shells out to `telemetry/version_check.py` and `telemetry/telemetry_init.py`** —
19 skills carry it. In practice it would have failed silently, because
`telemetry/` sits at the pack root and is not copied with the skill, but an
instruction to phone home on every invocation would still have been sitting in
the installed file. Stripped on the way in. For the record, the upstream
telemetry endpoint is the placeholder `https://example.com/api/telemetry` and
`version_check` only hits the GitHub releases API — nothing was being
exfiltrated, and the pack documents the collection as opt-in.

**Three of the five have no YAML frontmatter at all.** Claude Code still
registers a skill by its directory name, but with no `description` the model has
nothing to route on — `mk-seo-ops` was listing as the bare string "AI SEO Ops".
Descriptions were written from each skill's own "When to Use" section. Worth
knowing generally: a skill can install cleanly, appear in the list, and still be
unreachable in practice.

## A note on the star counts

`marketingskills` shows 43.7k stars on a repository created 2026-01-15;
`claude-seo` 13.8k since February. Those numbers are steep for repositories that
young, and they were not treated as evidence of quality. The packs were taken on
what the files actually contain — which, on inspection, is substantive: real
rubrics, working Python, and in `claude-seo`'s case correct handling of the
Google Shopping surface.
