#!/usr/bin/env bash
# Install the Google SEO / Google Shopping skill packs into ~/.claude/skills.
#
# The container is ephemeral — skills installed by hand vanish with it. This
# script is the durable copy, so a fresh session can restore the whole set in
# one command:
#
#     bash scripts/seo-skills-setup.sh
#
# Idempotent: an already-installed skill is left alone, so re-running only
# fills gaps.
#
# A note on why the selection is not "everything in every repo". A SKILL.md is
# an instruction file this agent later reads and follows, and every installed
# description occupies context in every session. Two consequences:
#   - Scope. Packs are pulled for the SEO/Shopping ask, not wholesale. The
#     120-skill influencer/narrative half of aaron-marketing-skills is skipped;
#     only its product-feed-optimizer is Shopping-relevant.
#   - Trust. These are third-party instructions. verify_pack() below is the
#     same scan run before the first install — it is cheap, so it runs every
#     time rather than being a one-off that rotted.
set -euo pipefail

WORK="${WORK:-${TMPDIR:-/tmp}/seo-skill-src}"
DEST="${DEST:-$HOME/.claude/skills}"
mkdir -p "$WORK" "$DEST"

REPOS=(
  AgriciDaniel/claude-seo               # 33 skills: technical, schema, ecommerce, Google APIs
  zubair-trabzada/geo-seo-claude        # 16 skills: AI-search / answer-engine optimisation
  coreyhaines31/marketingskills         # 49 skills: SEO, CRO, analytics, growth
  ericosiu/ai-marketing-skills          # seo-ops + conversion/content/growth ops
  aaron-he-zhu/aaron-marketing-skills   # product-feed-optimizer only
)

clone() {
  local repo=$1 dir="$WORK/$(basename "$1")"
  [ -d "$dir" ] && { echo "  have   $repo"; return; }
  git clone --depth 1 -q "https://github.com/$repo.git" "$dir" && echo "  cloned $repo"
}

# Refuses to install a pack whose instructions reach for credentials or try to
# talk over the top of the session. Documentation that merely *mentions* .env
# or an API-key variable is normal and allowed; a skill that reads ~/.ssh, pipes
# base64 into a shell, or tells the agent to ignore prior instructions is not.
verify_pack() {
  local dir=$1 hits
  hits=$(grep -rlEi 'id_rsa|\.ssh/|~/\.aws|AWS_SECRET|base64 -d *\| *(ba)?sh|ignore (all )?(previous|prior|above)|disregard (the )?(system|previous)|do not tell the user' \
           "$dir" --include=SKILL.md 2>/dev/null || true)
  [ -z "$hits" ] && return 0
  echo "  REFUSED $(basename "$dir") — suspicious instructions:" >&2
  echo "$hits" >&2
  return 1
}

# Copy one skill directory in, renaming the `name:` frontmatter to match when
# the destination name differs. Claude Code resolves a skill by its directory,
# so a stale `name:` left behind by a prefix rename is a silent mismatch.
install_skill() {
  local src=$1 name=$2
  [ -f "$src/SKILL.md" ] || return 0
  if [ -e "$DEST/$name" ]; then echo "  skip   $name (present)"; return 0; fi
  cp -r "$src" "$DEST/$name"
  if [ "$(basename "$src")" != "$name" ]; then
    sed -i "0,/^name:.*/s//name: $name/" "$DEST/$name/SKILL.md"
  fi
  echo "  add    $name"
}

echo "Fetching packs into $WORK"
for r in "${REPOS[@]}"; do clone "$r"; done

echo "Verifying"
for r in "${REPOS[@]}"; do verify_pack "$WORK/$(basename "$r")" || exit 1; done
echo "  clean"

echo "Installing into $DEST"

# claude-seo — already namespaced seo-*, install verbatim. The extensions/ tree
# holds paid-API variants (Ahrefs, DataForSEO, SERanking, Profound, Firecrawl,
# Bing Webmaster); they are installed too so they are ready the day a key
# exists, and install_skill's present-check keeps the two copies of
# seo-image-gen / seo-dataforseo from fighting.
for d in "$WORK"/claude-seo/skills/*/ "$WORK"/claude-seo/extensions/*/skills/*/; do
  [ -d "$d" ] && install_skill "${d%/}" "$(basename "$d")"
done

# geo-seo-claude — namespaced geo-*, plus the umbrella skill at geo/.
for d in "$WORK"/geo-seo-claude/skills/*/ "$WORK"/geo-seo-claude/geo/; do
  [ -d "$d" ] && install_skill "${d%/}" "$(basename "$d")"
done

# marketingskills — names like `schema`, `analytics`, `cro`, `ads` are far too
# generic to sit unqualified next to 116 existing skills, so the whole pack
# takes an mk- prefix.
for d in "$WORK"/marketingskills/skills/*/; do
  install_skill "${d%/}" "mk-$(basename "${d%/}")"
done

# ai-marketing-skills — the ops-shaped subset. The rest of the pack is podcast,
# video and sales-pipeline work that the ask did not cover.
#
# These five need repair on the way in, which is why they get their own pass:
#
#   1. They ship with NO YAML frontmatter. Claude Code will still register a
#      skill by its directory name, but with no `description` the model has
#      nothing to route on — "AI SEO Ops" as a bare H1 is not a trigger. The
#      descriptions below are written here, from each skill's own "When to Use".
#   2. Every one opens with a "Preamble (runs on skill start)" that shells out
#      to telemetry/version_check.py and telemetry/telemetry_init.py. That
#      directory lives at the pack root and is not part of the skill, so the
#      commands would fail silently — but the instruction to phone home on
#      every invocation would still be sitting in the file. Stripped.
#      (For the record: version_check hits the GitHub releases API, and the
#      telemetry endpoint in the upstream source is the placeholder
#      https://example.com/api/telemetry — nothing was being exfiltrated.)
for n in seo-ops conversion-ops content-ops growth-engine autoresearch; do
  install_skill "$WORK/ai-marketing-skills/$n" "mk-$n"
done

python3 - "$DEST" <<'PY'
import pathlib, re, sys
dest = pathlib.Path(sys.argv[1])
desc = {
 "mk-seo-ops": "Keyword intelligence and Google Search Console operations: quick-win keywords from GSC, competitor gap analysis, decaying-content detection, and trend scouting. Ships Python tooling (gsc_client.py, content_attack_brief.py, trend_scout.py); the full brief needs GSC auth and an Ahrefs token.",
 "mk-conversion-ops": "Conversion-rate audit of a landing or product page, plus survey and lead-magnet generation. Ships cro_audit.py and survey_lead_magnet.py.",
 "mk-content-ops": "Quality gate for any written asset: assembles a panel of domain experts, scores the draft against rubrics, and iterates until every score clears 90 (max three rounds). Use for copy, sequences, landing pages, strategy docs, or as a gate on another skill's output.",
 "mk-growth-engine": "Weekly growth scorecard, experiment engine, and budget-pacing alerts. Use for running an ongoing experiment program rather than a one-off test.",
 "mk-autoresearch": "Generates 50+ variants of a piece of copy, scores each with a simulated five-expert panel, and evolves the winners over several rounds. Use for landing pages, subject lines, ad copy, headlines, or CTA text.",
}
for name, d in desc.items():
    p = dest / name / "SKILL.md"
    if not p.exists():
        continue
    text = p.read_text()
    # Drop the telemetry preamble: its heading through the fenced block after it.
    text = re.sub(r"##\s*Preamble \(runs on skill start\).*?```\s*\n(?:.*?```\s*\n)?",
                  "", text, count=1, flags=re.S)
    if not text.startswith("---"):
        text = f"---\nname: {name}\ndescription: {d}\n---\n\n" + text.lstrip()
        p.write_text(text)
        print(f"  fixed  {name} (frontmatter + preamble)")
    else:
        p.write_text(text)
PY

# The one genuine Google Shopping skill found anywhere on GitHub.
install_skill "$WORK/aaron-marketing-skills/ad/research/product-feed-optimizer" \
              "mk-product-feed-optimizer"

# mcp-gsc ships four skills that drive the Search Console MCP server configured
# in .mcp.json. They are the only ones here that read live Google data rather
# than reasoning about a page, so they stay inert until credentials exist.
clone AminForou/mcp-gsc
for d in "$WORK"/mcp-gsc/skills/*/; do
  install_skill "${d%/}" "gsc-$(basename "${d%/}")"
done

# Agent-Reach — an internet-reading CLI plus skill (Twitter, Reddit, YouTube,
# GitHub, Bilibili, XiaoHongShu, Facebook, Instagram, LinkedIn, V2EX, RSS, and
# any web page via Jina Reader).
#
# Installed on request, and worth being blunt about: **every data channel it
# reads is blocked by this container's proxy.** Measured 2026-08-11 —
# r.jina.ai, youtube.com, the V2EX API, two unrelated RSS feeds and
# mcp.exa.ai all return 000 at the tunnel. `agent-reach doctor` reports RSS and
# "any web page" as available because it checks that curl exists, not that the
# host resolves. The only reachable host in the whole set is registry.npmjs.org,
# which just installs more tooling that then cannot reach anything.
#
# It is not wasted: the same skill runs fully on a normal machine, and the
# cookie-based platforms need a real Chrome session that a sandbox never has
# anyway. Install it here for parity; use it from the desktop.
#
# Note for HIVOLT specifically: the platform list has **no TikTok**.
if [ "${WITH_AGENT_REACH:-0}" = "1" ]; then
  clone Panniantong/Agent-Reach
  pip install -q -e "$WORK/Agent-Reach" && agent-reach skill --install
  mkdir -p "$HOME/.config/yt-dlp"
  grep -qxF -- '--js-runtimes node' "$HOME/.config/yt-dlp/config" 2>/dev/null \
    || printf '%s\n' '--js-runtimes node' >> "$HOME/.config/yt-dlp/config"
fi

# Repos that are tools rather than skills — cloned for reference, not installed.
# None of them run unattended; each needs a credential or a target URL.
#   google/rubik                  Merchant Center offer repair (Google Shopping
#                                 disapprovals: image, GTIN). Needs a Merchant
#                                 Center account, which HIVOLT does not have yet.
#   every-app/open-seo            Self-hosted Semrush/Ahrefs alternative.
#   sethblack/python-seo-analyzer Crawls a site and reports technical SEO issues.
if [ "${WITH_TOOLS:-0}" = "1" ]; then
  for r in google/rubik every-app/open-seo sethblack/python-seo-analyzer; do clone "$r"; done
fi

echo
echo "Installed skill count: $(find "$DEST" -maxdepth 2 -name SKILL.md | wc -l)"
