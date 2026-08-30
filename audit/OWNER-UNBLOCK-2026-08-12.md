# The three Google blockers: what is reachable from here and what is not

2026-08-12. Asked to implement all three. Two are genuinely outside this
container; one turned out to need far less than previously stated.

## Search Console — the field already exists, no republish needed

The live theme (v33) already ships a **Search engine verification** section in
the theme editor with a `google_site_verification` text setting, and a
`bing_site_verification` beside it. Its own help text says exactly what to
paste. Nothing needs building, and nothing needs publishing — theme settings
are editable in the customiser on the live theme.

What has been blocking it is that the **wrong verification method** was
attempted. `/pages/google-site-verification` contains:

```
google-site-verification: google6945ed5c46bc40d8.html
```

That is the **HTML file** method. It requires that exact file at the domain
root, and Shopify cannot serve one — the store has a redirect from
`/google6945ed5c46bc40d8.html` to a themed page, and Google will not follow a
301 for file verification. It was never going to pass, and no amount of
retrying changes that.

The **HTML tag** method works, and the theme is already wired for it:

1. Search Console → Add property → **URL prefix** → `https://hivolt-usa.com`
2. Choose **HTML tag**. It shows
   `<meta name="google-site-verification" content="XXXXXXXX...">`
3. Copy **only** the `content` value.
4. Shopify admin → Online Store → Themes → Customise → Theme settings →
   Search engine verification → paste → Save.

Only the owner can do steps 1–3; the token comes from a signed-in Google
account and cannot be generated here. Step 4 is a theme-settings write to the
live theme, which is blocked in this container.

## Merchant Center — not reachable, and there are now two accounts

`merchants.google.com` is blocked by the egress proxy, there is no Admin API
surface for Merchant Center, and Windsor has no Google Merchant Center
connector attached to this workspace (only `facebook` / "Hivolt USA" is
connected). Claiming the domain and configuring shipping are UI actions behind
a Google login.

**Worth checking before anything else:** the account id in the link supplied
today is **5838274874**. The one recorded on 08-10 was **5705286743**. Two
Merchant Center accounts for one store is a real hazard — if both end up
holding the same domain and the same offer ids, they compete for the claim and
offers get suppressed for a claim conflict rather than for anything wrong with
the feed. The Google & YouTube channel creates and manages its own account when
it is installed, which is very likely what 5838274874 is. If so, **that** is the
live one, the earlier manual account should be left alone or closed, and the
domain claim only has to happen once, in the channel's account.

## TikTok bio — not reachable

The TikTok tools available here publish videos. There is no profile or bio
endpoint in any connected surface, so `hivolt-usa.com/tiktok` has to be pasted
into the app by hand.

## Also settled today

The `social_instagram` and `social_tiktok` theme settings exist in the same
customiser panel and are still empty. Filling them costs nothing and feeds
`sameAs` in the store's structured data, which is one of the signals that ties
the domain to the social profiles as one entity.

Eight dead URLs that Google still ranks were redirected on 08-12 —
`/pages/contact`, `/pages/ueber-uns`, `/pages/widerrufsbelehrung`,
`/pages/impressum`, `/pages/versand-lieferung`, `/pages/about-focus-foxes`,
`/about`, `/collections/best-sellers`. Those had no redirect and genuinely were
404ing. The nine perfume articles are deliberately still 404ing, for the reason
in `audit/WHY-NO-SALES-SEO-2026-08-12.md`.
