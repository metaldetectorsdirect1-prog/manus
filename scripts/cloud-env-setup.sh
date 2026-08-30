#!/usr/bin/env bash
# HIVOLT cloud environment setup script.
#
# Paste this into the environment's "Setup script" box at claude.ai
# (edit the environment -> Setup script). It runs once per session, before
# Claude Code starts, which is why it can do the certificate work that the
# in-session permission classifier blocks — and rightly blocks, since
# modifying a trust store from inside a running agent session is exactly the
# kind of thing that should need a human decision.
#
# ── What this fixes ────────────────────────────────────────────────────────
#
# Playwright's bundled Chromium carries its OWN NSS profile and never reads
# the system trust store the rest of the toolchain uses. The session's egress
# proxy re-terminates TLS, so every HTTPS page load in that browser fails
# ERR_CERT_AUTHORITY_INVALID — including hosts the network policy ALLOWS.
# Measured, not assumed: github.com and registry.npmjs.org both failed that
# way while curl to the same hosts succeeded.
#
# The fix is to add the proxy CA to the NSS database Chromium reads. This is
# an addition to a trust store, not a relaxation of verification: every other
# certificate is still validated normally, and nothing here passes
# --ignore-certificate-errors or sets NODE_TLS_REJECT_UNAUTHORIZED.
#
# ── What this does NOT fix ─────────────────────────────────────────────────
#
# Blocked hosts. Those return "gateway answered 403 to CONNECT" and are an
# organization egress policy, not a certificate problem. The environment's
# README is explicit: do not retry or route around them. They are opened by
# setting the environment's Network access level to Custom and listing the
# domains — see docs/cloud-network-allowlist.md in this repo for the list.
#
# Both halves are needed. The allowlist without the CA gives you curl and
# WebFetch but a browser that cannot load a page; the CA without the
# allowlist gives you a working browser pointed at hosts it may not reach.

set -euo pipefail

CA="/root/.ccr/agent-proxy-ca.crt"
NSSDB="${HOME}/.pki/nssdb"

if [ ! -f "$CA" ]; then
  echo "setup: no agent proxy CA at $CA — nothing to import, skipping."
  exit 0
fi

# certutil ships in libnss3-tools and is not in the base image.
if ! command -v certutil >/dev/null 2>&1; then
  echo "setup: installing libnss3-tools for certutil"
  apt-get update -qq || true          # PPAs 403 behind the proxy; the main
                                      # archive still resolves, so a partial
                                      # update must not abort the script
  apt-get install -y -qq libnss3-tools
fi

mkdir -p "$NSSDB"
if [ ! -f "$NSSDB/cert9.db" ]; then
  certutil -d "sql:$NSSDB" -N --empty-password
fi

# -t "C,," trusts it for TLS server auth only, not for email or code signing.
certutil -d "sql:$NSSDB" -A -t "C,," -n "CCR Agent Proxy CA" -i "$CA"

echo "setup: NSS trust store now contains:"
certutil -d "sql:$NSSDB" -L

cat <<'NOTE'

setup: done. Chromium at /opt/pw-browsers can now complete TLS to any host the
environment's network policy allows. Launch it normally --

    p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                      args=["--no-sandbox"])

-- with no certificate flags. If a page still fails ERR_TUNNEL_CONNECTION_FAILED,
that host is denied by the network policy and needs adding to the Custom
allowlist, not more certificate work.
NOTE
