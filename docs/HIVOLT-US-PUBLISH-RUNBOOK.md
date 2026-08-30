# HIVOLT-US-PUBLISH-RUNBOOK.md — atomic US launch sequence, 2026-08-28

Nothing in this runbook is executed now. Every stage ends with a read-back;
a failed read-back stops the sequence. Stages 1–11 are preconditions;
12–17 are launch day.

| # | Stage | Actor | Action | Read-back that proves it |
|---|---|---|---|---|
| 1 | Policies verified | Owner | Paste 4 bodies; mirror GMC shipping/returns | `shopPolicies` bodies contain the corrected sentinel phrases ("5 business days", "2–6 business days"); old phrases absent |
| 2 | Identity verified | Owner+session | GMC business info = policies = footer | manual GMC check + policy read |
| 3 | Product facts populated | Owner supplies, session enters | spec.*, gender/age_group, weights, verified composition | metafields read per product; every value CLASS A/B |
| 4 | Fit populated | same | size-chart metaobjects + spec.size_chart links | metaobject query + PDP reference read |
| 5 | Visual assets approved | Owner | approve/replace each of the 31 V3 frames (HIVOLT-V3-IMAGE-REVIEW.md commands) | review index updated: 0 pending |
| 6 | Product QA | Session | titles, media order, options, price, inventory per product | full product read ×4 |
| 7 | Collections cleaned | Owner approves, session executes | unpublish 11 empty; fix 2 live footer links | collections read: no published empty collections; menu read |
| 8 | Navigation activated | Session (workbench) | fashion-main gains Women/Knitwear/New in etc. — only destinations passing a products>0 check | menu read + per-link collection productsCount>0 |
| 9 | Reviews positioned | Owner Decision D, session wires | Judge.me app block gated ≥1 review | template read-back |
| 10 | Analytics verified | Owner installs GA4, session verifies | standard events in DebugView on preview | event log evidence |
| 11 | GMC trust gate | Both | every row in HIVOLT-GMC-TRUST-GATE.md = pass | checklist annotated with evidence |
| 12 | **Product publication** | Session, on explicit owner authorization | 4 products DRAFT→ACTIVE + Online Store publication | status read + `onlineStoreUrl` non-null + collection pages render |
| 13 | Product rows enabled | Session (workbench) | `latest` section `disabled` flag removed | index.json read-back |
| 14 | Commerce CTAs enabled | Session (workbench) | hero/tile/collage links to now-live collections | template read + zero-dead-link scan |
| 15 | Smoke tests | Owner (browser) | PDP → size → ATC → cart → checkout entry; search; filters; 390px pass | owner confirmation + screenshots |
| 16 | Dev theme final review | Owner | full-page 390/1440 screenshots approved | owner approval recorded |
| 17 | **Theme go-live** | **Owner only** | publish decision — never executed by the session | themes read: roles as owner intended |

Feed activation (Simprosys first sync + €5/day PMax trigger per playbook)
is deliberately **after** stage 17, on a store that is fully consistent.
Rollback points: stages 12–14 are each independently reversible
(status→DRAFT, re-disable row, re-blank links) — documented per stage
before execution.
