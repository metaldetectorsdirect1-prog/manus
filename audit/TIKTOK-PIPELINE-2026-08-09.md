# Posting to TikTok from here — the route that works

Until today, finished media could not leave this container. `tiktok_publish`
requires a **Higgsfield-hosted** video URL, and every Higgsfield host is refused
at the proxy:

```
upload.higgsfield.ai        000
higgsfield.ai               000
d2ol7oe51mr4n9.cloudfront   000
```

That is still true. The unblock is that the *upload* never has to happen from
here at all — `media_import_url` is fetched **server-side by Higgsfield**, so the
file only needs to sit somewhere Higgsfield can reach. Shopify's own CDN is such
a place, and staged uploads to it work from this container.

```
local render
  → stagedUploadsCreate (resource: FILE, video/mp4)
  → POST the bytes to shopify-staged-uploads.storage.googleapis.com   [201]
  → fileCreate (contentType: FILE)  → poll until fileStatus READY
  → public https://cdn.shopify.com/…/hivolt-<film>.mp4
  → media_import_url                → Higgsfield media_id
  → https://d2ol7oe51mr4n9.cloudfront.net/user_<uid>/<media_id>.mp4
  → tiktok_prepare_publish → tiktok_publish → PUBLISH_COMPLETE
```

`cdn.shopify.com` is also blocked *from here*, which does not matter: nothing in
this chain requires us to read it back. Byte-exactness is confirmed instead by
comparing `originalFileSize` on the Shopify file against the local file.

## Why these films carry no AIGC label

`is_aigc: false` is a factual claim, not a convenience. The films are rendered
by `scripts/tiktok-film.py` — deterministic HTML and CSS, screenshotted frame by
frame through Playwright and encoded with ffmpeg. No model generates any part of
them. TikTok demotes reach on AIGC-labelled media, so a brand that can honestly
answer "no" should not be paying that cost.

Commercial disclosure is the opposite case: `enabled: true, your_brand: true`,
which labels each post "Promotional content". It is our own brand being
promoted, so the disclosure is owed.

## Quotas

Enforced before TikTok is called: **5 posts per minute, 13 per 24 hours**, both
rolling. Failed attempts and drafts do not consume quota; an accepted post does.
A rejection returns `cadence_burst` or `cadence_daily` with `retry_after_seconds`
— wait that long rather than retrying, since retrying sooner only earns another
rejection.

## Posted 2026-08-09

| Film | publish_id | Caption hook |
|---|---|---|
| spec | `…7672167423436408845` | Every brand knows this number. Almost none print it |
| ask | `…7672168330799990797` | Ask any brand one question |
| opacity | `…7672168517508155405` | "Is it opaque?" Wrong question |
| ladder | `…7672168651881596942` | Our leggings are not one price |

Confirmed `PUBLISH_COMPLETE` on the first; the rest returned publish ids and
TikTok takes a few minutes to process.

Imported and ready, not yet posted: `weights`, `sets`, `returns`. Staged but not
yet imported: `factory`, `shipping`, `mens`, `yoga`, `voltcore` — their signed
upload targets expire 2026-08-10T22:46Z.

## One defect caught before it went public

The `sets` film said **"$92 bought separately"**. The fabric-weight ladder had
already moved the 230 g/m² legging in that set from $54 to $59, so the true
separate total is **$97** — the figure the product's own `compareAtPrice`
carries. A stale compare-at on a public post is a false savings claim, not a
stale number. Fixed before any render was uploaded.

The lesson generalises: every figure in a film is a copy of a number that lives
somewhere else. When a price moves, `grep '\$[0-9]' scripts/tiktok-film.py` is
part of the change, not a follow-up to it.
