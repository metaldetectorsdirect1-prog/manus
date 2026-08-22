#!/usr/bin/env python3
"""Adjudicate a Shopify theme write target against live theme state.

This script does NOT talk to Shopify, and it is important to be exact about
why. There are no Shopify credentials in this environment, no script in this
repository contains an Admin API call, and egress to the store's admin host is
denied at CONNECT by network policy. Shopify is reachable only through the MCP
connector, which is available to the Claude session and not to a subprocess.

So the work is split. The session fetches; this script judges. Feed it the
themes read-back and it applies the production-state rules from CLAUDE.md
deterministically, which is worth having because the rules are exactly the kind
a tired session talks itself out of:

    role is read from the `role` field and from nothing else
    a name containing "DRAFT" proves nothing
    a name containing "LIVE" proves nothing
    an ID that used to be a draft proves nothing
    MAIN is refused unless production modification was explicitly authorized

On 2026-08-21 theme 158653808872 - named "HIVOLT v7 - DRAFT: PDP data layer
(do not publish)" - became MAIN. Every earlier session in this project would
have treated it as a sandbox. That is the failure this file exists to prevent.

Usage
  python3 site/check-hivolt-theme-target.py --themes state.json \
          --target gid://shopify/OnlineStoreTheme/158653808872 \
          --expect-role UNPUBLISHED
  python3 site/check-hivolt-theme-target.py --themes state.json --report
  python3 site/check-hivolt-theme-target.py --self-test

`state.json` is whatever the connector returned: the full GraphQL envelope, the
`themes` object, or a bare list of theme nodes. All three shapes are accepted
so the read-back can be pasted in without reshaping it.

Exit codes
  0  the target is safe for the requested write
  1  refused - the reason is printed
  2  malformed input
"""
import argparse
import json
import sys

MAIN = "MAIN"


class Refused(Exception):
    """A write that must not proceed. The message is the reason."""


# ---------------------------------------------------------------------------
# Input handling
# ---------------------------------------------------------------------------
def extract_themes(payload):
    """Pull a list of theme dicts out of any of the shapes the connector emits.

    Being liberal here is deliberate: the alternative is a session hand-editing
    a read-back to fit a schema, and hand-editing state before checking it is
    how state gets quietly corrected into the wrong answer.
    """
    node = payload
    if isinstance(node, dict) and "data" in node:
        node = node["data"]
    if isinstance(node, dict) and "themes" in node:
        node = node["themes"]
    if isinstance(node, dict) and "edges" in node:
        node = [e.get("node", e) for e in node["edges"]]
    if not isinstance(node, list):
        raise ValueError("could not find a list of themes in the input")

    out = []
    for t in node:
        if not isinstance(t, dict):
            raise ValueError(f"theme entry is not an object: {t!r}")
        if "id" not in t or "role" not in t:
            raise ValueError(f"theme entry missing id or role: {t!r}")
        out.append({"id": str(t["id"]), "name": t.get("name", ""),
                    "role": str(t["role"]).upper(),
                    "updatedAt": t.get("updatedAt", "")})
    if not out:
        raise ValueError("theme list is empty")
    return out


def find(themes, target):
    """Match on id, accepting a bare numeric id as well as a full GID.

    Matching never falls back to the name. A name lookup is precisely the
    mistake this file exists to make impossible, so it is not offered even as a
    convenience.
    """
    t = str(target)
    for th in themes:
        if th["id"] == t or th["id"].rsplit("/", 1)[-1] == t.rsplit("/", 1)[-1]:
            return th
    return None


def main_theme(themes):
    live = [t for t in themes if t["role"] == MAIN]
    if len(live) != 1:
        raise Refused(
            f"expected exactly one MAIN theme, found {len(live)}: "
            f"{[t['id'] for t in live] or 'none'}. Do not write until this is "
            "resolved - the store's live theme is ambiguous.")
    return live[0]


# ---------------------------------------------------------------------------
# The rules
# ---------------------------------------------------------------------------
def adjudicate(themes, target, expect_role=None, allow_main=False):
    """Return the target theme, or raise Refused with the reason.

    Order matters. Identity is settled first, then the live role, then the
    prompt's claim about the role - so a prompt can never be the thing that
    establishes what the target is.
    """
    live = main_theme(themes)
    th = find(themes, target)
    if th is None:
        raise Refused(
            f"target {target} is not in the theme list. Either the id is wrong "
            "or the read-back is from a different store. Do not write.")

    role = th["role"]

    # A prompt's claim about the role is checked against Shopify, never
    # trusted over it.
    if expect_role is not None and role != str(expect_role).upper():
        raise Refused(
            f"prompt assumption conflicts with live Shopify state.\n"
            f"  prompt expects : {str(expect_role).upper()}\n"
            f"  Shopify says   : {role}\n"
            f"  theme          : {th['id']}\n"
            f"  name           : {th['name']!r}\n"
            "Live state wins. Stop and report the conflict; do not reinterpret "
            "the authorization and do not redirect the write.")

    if role == MAIN and not allow_main:
        raise Refused(
            f"target is the LIVE theme and production modification was not "
            f"authorized.\n"
            f"  theme : {th['id']}\n"
            f"  name  : {th['name']!r}\n"
            "The name is not evidence of the role. Writing here changes the "
            "storefront. Obtain explicit production authorization, or pick a "
            "genuinely unpublished target - do not publish or unpublish a "
            "theme as a workaround.")

    if role != MAIN and allow_main:
        # Not a refusal, but worth surfacing: production authorization was
        # granted and is not being used, which usually means the target is
        # wrong rather than that the authorization was unnecessary.
        print(f"note: production write authorized but target {th['id']} has "
              f"role {role}; the live theme is {live['id']}", file=sys.stderr)

    return th


def report(themes):
    live = [t for t in themes if t["role"] == MAIN]
    print(f"{'ROLE':<12} {'ID':<44} NAME")
    for t in sorted(themes, key=lambda x: (x["role"] != MAIN, x["id"])):
        flag = "<<< LIVE" if t["role"] == MAIN else ""
        print(f"{t['role']:<12} {t['id']:<44} {t['name'][:46]!r} {flag}")
    print()
    if len(live) == 1:
        print(f"MAIN theme: {live[0]['id']}  (updatedAt {live[0]['updatedAt']})")
    else:
        print(f"WARNING: {len(live)} themes hold role MAIN")
    print("\nRoles above come from Shopify's `role` field. Theme names in this "
          "store are known to contradict it - re-query before every write.")


# ---------------------------------------------------------------------------
# Self-test. These are the Phase 14 scenarios, executable rather than described.
# ---------------------------------------------------------------------------
# The real state as of 2026-08-21: a theme named DRAFT that is MAIN, and a
# theme named LIVE that is not. Both traps present in one fixture.
#
# These names were corrected in Shopify on 2026-08-22 and are kept here on
# purpose. The fixture is not a description of current state - it is the
# adversarial input these tests exist to survive. Updating it to the new neutral
# names would delete the very thing being tested and leave a suite that proves
# nothing. If the fixture ever needs to change, add a case; do not replace this
# one.
REAL = [
    {"id": "gid://shopify/OnlineStoreTheme/158653808872",
     "name": "HIVOLT v7 — DRAFT: PDP data layer (do not publish)",
     "role": "MAIN", "updatedAt": "2026-08-21T04:11:02Z"},
    {"id": "gid://shopify/OnlineStoreTheme/158570021096",
     "name": "HIVOLT v6 — PUBLISH ME: logo in header",
     "role": "UNPUBLISHED", "updatedAt": "2026-08-21T04:10:55Z"},
    {"id": "gid://shopify/OnlineStoreTheme/158482727144",
     "name": "HIVOLT v35 — LIVE (returns copy fixed)",
     "role": "UNPUBLISHED", "updatedAt": "2026-08-16T21:12:59Z"},
]

# The world as every session before 2026-08-21 believed it to be.
REVERSED = [dict(t, role={"MAIN": "UNPUBLISHED", "UNPUBLISHED": "MAIN"}[t["role"]])
            if t["id"].endswith(("158653808872", "158570021096")) else dict(t)
            for t in REAL]

V7 = "gid://shopify/OnlineStoreTheme/158653808872"
V6 = "gid://shopify/OnlineStoreTheme/158570021096"
V35 = "gid://shopify/OnlineStoreTheme/158482727144"

TESTS = []


def test(name):
    def deco(fn):
        TESTS.append((name, fn))
        return fn
    return deco


def refuses(themes, **kw):
    try:
        adjudicate(themes, **kw)
    except Refused as e:
        return str(e)
    raise AssertionError("expected a refusal, the write was allowed")


@test("v7 is refused as a draft target now that it is MAIN")
def t_v7_refused():
    msg = refuses(REAL, target=V7)
    assert "LIVE theme" in msg, msg


@test("a name containing DRAFT does not override role MAIN")
def t_name_draft_ignored():
    th = find(REAL, V7)
    assert "DRAFT" in th["name"] and th["role"] == MAIN
    msg = refuses(REAL, target=V7)
    assert "name is not evidence" in msg, msg


@test("a name containing LIVE does not make an unpublished theme production")
def t_name_live_ignored():
    th = adjudicate(REAL, target=V35)
    assert "LIVE" in th["name"] and th["role"] == "UNPUBLISHED"


@test("a stale prompt claiming v7 is UNPUBLISHED is refused, not obeyed")
def t_stale_prompt_refused():
    msg = refuses(REAL, target=V7, expect_role="UNPUBLISHED")
    assert "conflicts with live Shopify state" in msg, msg
    assert "Live state wins" in msg, msg


@test("v6 is a valid draft target now")
def t_v6_ok():
    th = adjudicate(REAL, target=V6, expect_role="UNPUBLISHED")
    assert th["role"] == "UNPUBLISHED"


@test("role detection follows the data, not the id")
def t_reversed_roles():
    assert main_theme(REAL)["id"].endswith("158653808872")
    assert main_theme(REVERSED)["id"].endswith("158570021096")
    # Under the old world v7 was a legitimate draft target...
    adjudicate(REVERSED, target=V7, expect_role="UNPUBLISHED")
    # ...and v6 was the one that had to be refused.
    assert "LIVE theme" in refuses(REVERSED, target=V6)


@test("explicit production authorization allows a MAIN write")
def t_allow_main():
    th = adjudicate(REAL, target=V7, allow_main=True)
    assert th["role"] == MAIN


@test("authorization does not paper over a role conflict")
def t_allow_main_still_checks_expectation():
    msg = refuses(REAL, target=V7, expect_role="UNPUBLISHED", allow_main=True)
    assert "conflicts with live Shopify state" in msg, msg


@test("an unknown target is refused rather than guessed at")
def t_unknown_target():
    assert "not in the theme list" in refuses(REAL, target="gid://x/999")


@test("two MAIN themes stop the write instead of picking one")
def t_two_main():
    two = [dict(t, role=MAIN) for t in REAL[:2]] + [REAL[2]]
    assert "exactly one MAIN" in refuses(two, target=V6)


@test("no MAIN theme stops the write")
def t_no_main():
    none = [dict(t, role="UNPUBLISHED") for t in REAL]
    assert "exactly one MAIN" in refuses(none, target=V6)


@test("every connector payload shape parses to the same theme list")
def t_shapes():
    nodes = REAL
    shapes = [
        nodes,
        {"edges": [{"node": t} for t in nodes]},
        {"themes": {"edges": [{"node": t} for t in nodes]}},
        {"data": {"themes": {"edges": [{"node": t} for t in nodes]}}},
    ]
    got = [extract_themes(s) for s in shapes]
    assert all(g == got[0] for g in got), "shapes disagreed"
    assert len(got[0]) == 3


@test("a theme entry with no role is rejected, not defaulted")
def t_missing_role():
    try:
        extract_themes([{"id": "gid://shopify/OnlineStoreTheme/1", "name": "x"}])
    except ValueError as e:
        assert "missing id or role" in str(e)
    else:
        raise AssertionError("a role-less theme was accepted")


def self_test():
    failed = []
    for name, fn in TESTS:
        try:
            fn()
            print(f"  ok    {name}")
        except AssertionError as e:
            failed.append(name)
            print(f"  FAIL  {name}\n        {e}")
        except Exception as e:                              # noqa: BLE001
            failed.append(name)
            print(f"  ERROR {name}\n        {type(e).__name__}: {e}")
    total = len(TESTS)
    print(f"\nTHEME TARGET GUARD: {total - len(failed)}/{total} "
          f"{'PASS' if not failed else 'FAIL'}")
    return 1 if failed else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--themes", help="file holding the themes read-back, or - for stdin")
    ap.add_argument("--target", help="theme id or GID the write would go to")
    ap.add_argument("--expect-role", help="the role the task prompt claims the target has")
    ap.add_argument("--allow-main", action="store_true",
                    help="explicit authorization to modify the live theme")
    ap.add_argument("--report", action="store_true", help="print the role table and exit")
    ap.add_argument("--self-test", action="store_true", help="run the guard's own tests")
    a = ap.parse_args(argv)

    if a.self_test:
        return self_test()
    if not a.themes:
        ap.error("--themes is required (or use --self-test)")

    raw = sys.stdin.read() if a.themes == "-" else open(a.themes).read()
    try:
        themes = extract_themes(json.loads(raw))
    except (ValueError, json.JSONDecodeError) as e:
        print(f"MALFORMED INPUT: {e}", file=sys.stderr)
        return 2

    if a.report or not a.target:
        report(themes)
        return 0

    try:
        th = adjudicate(themes, target=a.target, expect_role=a.expect_role,
                        allow_main=a.allow_main)
    except Refused as e:
        print(f"REFUSED\n\n{e}", file=sys.stderr)
        return 1

    kind = "LIVE (production write authorized)" if th["role"] == MAIN else th["role"]
    print(f"OK - target is safe for this write\n"
          f"  theme : {th['id']}\n"
          f"  name  : {th['name']!r}\n"
          f"  role  : {kind}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
