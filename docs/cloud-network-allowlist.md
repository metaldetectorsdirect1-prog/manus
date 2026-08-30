# Opening the network for this session

Two separate blockers stop this session seeing the live store, the videos it
generates, Merchant Center and Search Console. Both are environment
configuration. Neither is a missing repository, and installing a browser-agent
framework would not touch either one.

## Blocker 1 — the egress policy

Measured from the proxy's own status endpoint, not inferred:

```
connect_rejected  studio.youtube.com:443        gateway answered 403 to CONNECT
connect_rejected  www.youtube.com:443           gateway answered 403 to CONNECT
connect_rejected  d8j0ntlcm91z4.cloudfront.net  gateway answered 403 to CONNECT
```

`WebFetch` returns `EGRESS_BLOCKED` for `hivolt-usa.com` as well, so this is
uniform across tools rather than a curl quirk. The environment is on
**Trusted** network access: package registries, GitHub and cloud SDKs only.

The levels are **None**, **Trusted**, **Full**, and **Custom**. Change it by
editing the environment and using the **Network access** selector.

Choose **Custom**, not Full. Full allows any domain, which is a real widening
of what an autonomous session can reach while holding store credentials. A
named list gets the same capability with a boundary someone can audit.

Paste one domain per line. `*.` matches every subdomain. Tick **Also include
default list of common package managers** or package installs break.

```
hivolt-usa.com
*.hivolt-usa.com
f36zps-yd.myshopify.com
admin.shopify.com
accounts.shopify.com
cdn.shopify.com
merchants.google.com
search.google.com
www.google.com
www.youtube.com
studio.youtube.com
*.googlevideo.com
*.cloudfront.net
cdn.higgsfield.ai
www.ebay.com
hivoltstore.com
```

### What each one buys

| domain | what it unblocks |
|---|---|
| `hivolt-usa.com`, `*.hivolt-usa.com` | seeing the live storefront, and the crawl-based SEO skills — every one of them starts by fetching the live URL, which is why they have all been dead |
| `f36zps-yd.myshopify.com`, `cdn.shopify.com` | the myshopify mirror and product imagery |
| `admin.shopify.com`, `accounts.shopify.com` | driving the admin in a browser for the settings the Admin API refuses — customer accounts off `focusfoxes.shop`, sales tax, `settings.logo` |
| `merchants.google.com` | Merchant Center 5838274874: the domain claim, the two-account conflict, per-item disapprovals |
| `search.google.com` | Search Console → Indexing → Pages, the single biggest open question |
| `www.google.com` | checking what actually ranks, rather than inferring it |
| `www.youtube.com`, `studio.youtube.com`, `*.googlevideo.com` | watching video, and reading the channel's own analytics |
| `*.cloudfront.net`, `cdn.higgsfield.ai` | retrieving generated video and thumbnails. Right now they are produced blind — the RDL thumbnail exists and has never been looked at, and AI text rendering garbles often enough that this matters |
| `www.ebay.com` | verifying leaf category ids directly instead of through search results |
| `hivoltstore.com` | settling whether the Chicago Ridge listing is a second storefront splitting the brand |

MCP connector traffic does **not** go through this allowlist. That is why
Shopify, GitHub and Higgsfield all work while `curl` to the same hosts fails,
and it is worth knowing before diagnosing anything else.

## Blocker 2 — the browser's certificate store

Opening the allowlist is not sufficient on its own. Playwright's bundled
Chromium carries its own NSS profile and never reads the CA bundle the rest of
the toolchain uses, so it fails `ERR_CERT_AUTHORITY_INVALID` even on hosts the
policy **allows** — confirmed against `github.com` and `registry.npmjs.org`,
both of which `curl` reaches fine.

`scripts/cloud-env-setup.sh` fixes it. Paste it into the environment's **Setup
script** box. It installs `libnss3-tools` and imports the proxy CA into
`~/.pki/nssdb` with TLS-server-auth trust only.

This is deliberately a setup script rather than something done in-session. The
permission classifier blocks trust-store modification from inside a running
session, which is correct — that decision should be a human's, made once at the
environment level, not something an agent grants itself mid-task.

Nothing here disables verification. No `--ignore-certificate-errors`, no
`NODE_TLS_REJECT_UNAUTHORIZED=0`. Every certificate other than the proxy's own
CA is still validated.

## Telling the two apart afterwards

- `ERR_CERT_AUTHORITY_INVALID` → certificate trust. Setup script did not run.
- `ERR_TUNNEL_CONNECTION_FAILED`, or `403 to CONNECT` in the proxy status →
  the host is not on the allowlist. Add it; do not work around it.

`curl -sS "$HTTPS_PROXY/__agentproxy/status"` prints the recent denials with
the host and reason, which is faster than guessing from a tool's error text.
