#!/usr/bin/env bash
# Step 3 - download FLUX.1 Schnell + support models for the detected profile.
#
# Requirement: nothing large is fetched until hardware AND every URL is verified.
# The script therefore runs in two phases:
#   PHASE 1  HEAD-check every URL and re-check free disk. Downloads nothing.
#   PHASE 2  only after phase 1 is clean (and you confirm) does it fetch weights.

. "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
load_hardware

PY="$(python_bin)"
[ -n "$PY" ] || die "no virtualenv - run scripts/01-install-comfyui.sh first"

CFG="$STUDIO_DIR/config/model-profiles.json"
[ -f "$CFG" ] || die "missing $CFG"

PROFILE="${PROFILE_OVERRIDE:-$PROFILE}"
step "Step 3/5 - models for profile '$PROFILE'"

# Resolve the profile's file list (common + profile, following inherits_models_from).
MANIFEST="$STATE_DIR/manifest-$PROFILE.tsv"
"$PY" - "$CFG" "$PROFILE" > "$MANIFEST" <<'PYCODE'
import json, sys
cfg = json.load(open(sys.argv[1])); prof = sys.argv[2]
p = cfg["profiles"][prof]
models = list(cfg["common_models"])
src = p.get("inherits_models_from")
models += cfg["profiles"][src]["models"] if src else p.get("models", [])
for m in models:
    print("\t".join([m["name"], m["dir"], m["url"], str(m.get("size_gb", 0)),
                     m.get("license", "?"), "yes" if m.get("verified") else "no",
                     m.get("mirror", "")]))
PYCODE

TOTAL_GB="$(awk -F'\t' '{s+=$4} END{printf "%.1f", s}' "$MANIFEST")"

echo
printf '  %-42s %-20s %7s  %s\n' FILE DIRECTORY SIZE_GB "URL VERIFIED UPSTREAM"
while IFS=$'\t' read -r name dir url size lic verified mirror; do
  printf '  %-42s %-20s %7s  %s\n' "$name" "models/$dir" "$size" "$verified"
done < "$MANIFEST"
printf '\n  total download: %s GB\n' "$TOTAL_GB"
printf '  licences:\n'
cut -f5 "$MANIFEST" | sort -u | sed 's/^/    - /'

# ---------------------------------------------------------------- PHASE 1
step "Phase 1 - preflight (no data transferred)"

NEED_GB="$(awk -v t="$TOTAL_GB" 'BEGIN{printf "%d", t+5}')"
AVAIL_GB="$(df -Pk "$COMFY_HOME" | awk 'NR==2{print int($4/1024/1024)}')"
info "free disk at $COMFY_HOME: ${AVAIL_GB} GB (need ~${NEED_GB} GB)"
[ "$AVAIL_GB" -ge "$NEED_GB" ] || die "not enough free disk - nothing was downloaded"

BAD=0
while IFS=$'\t' read -r name dir url size lic verified mirror; do
  dest="$COMFY_HOME/models/$dir/$name"
  if [ -f "$dest" ]; then
    ok "already present, skipping: $name"
    continue
  fi
  # -L follows redirects (HF serves weights off a CDN); tail -c3 keeps only the
  # FINAL status code, since curl prints one per hop.
  code="$(curl -sSL -o /dev/null -w '%{http_code}' --max-time 45 -I "$url" 2>/dev/null | tail -c 3 || true)"
  code="${code:-000}"
  if [ "$code" = "200" ]; then
    ok "reachable: $name"
  elif [ -n "$mirror" ]; then
    mcode="$(curl -sSL -o /dev/null -w '%{http_code}' --max-time 45 -I "$mirror" 2>/dev/null | tail -c 3 || true)"
    mcode="${mcode:-000}"
    if [ "$mcode" = "200" ]; then
      warn "primary URL for $name returned $code - will use the mirror"
      sed -i.bak "s|^$name\t$dir\t[^\t]*|$name\t$dir\t$mirror|" "$MANIFEST" 2>/dev/null || true
    else
      err "$name unreachable (primary $code, mirror $mcode)"; BAD=$((BAD+1))
    fi
  else
    err "$name unreachable (HTTP $code) - $url"; BAD=$((BAD+1))
  fi
done < "$MANIFEST"

if [ "$BAD" -gt 0 ]; then
  echo
  err "$BAD file(s) could not be verified. NOTHING has been downloaded."
  err "Model repos occasionally move files. Fix the URLs in:"
  err "  $CFG"
  err "then re-run this script. See docs/03-MODELS.md for how to find the current path."
  exit 1
fi

echo
ok "all URLs verified, disk is sufficient"
if [ "${SKIP_CONFIRM:-0}" != "1" ]; then
  confirm "Download ${TOTAL_GB} GB of model weights now?" || { info "aborted - nothing downloaded"; exit 0; }
fi

# ---------------------------------------------------------------- PHASE 2
step "Phase 2 - downloading"

HF_HDR=()
[ -n "${HUGGINGFACE_TOKEN:-}" ] && HF_HDR=(-H "Authorization: Bearer $HUGGINGFACE_TOKEN")

while IFS=$'\t' read -r name dir url size lic verified mirror; do
  dest="$COMFY_HOME/models/$dir/$name"
  [ -f "$dest" ] && { ok "skip $name"; continue; }
  mkdir -p "$(dirname "$dest")"
  info "downloading $name (${size} GB) -> models/$dir/"
  # -C - resumes a partial file; write to .part so an interrupted run never
  # leaves a truncated file that looks complete.
  curl -fL --retry 5 --retry-delay 5 --retry-all-errors -C - \
       "${HF_HDR[@]}" -o "${dest}.part" "$url"
  mv "${dest}.part" "$dest"
  ok "$name"
done < "$MANIFEST"

# ---------------------------------------------------------------- point workflows at these files
info "aligning workflows with profile '$PROFILE'"
"$PY" "$STUDIO_DIR/scripts/apply-profile.py" --profile "$PROFILE" >/dev/null
ok "workflows updated"

step "Installed models"
find "$COMFY_HOME/models" -type f \( -name '*.safetensors' -o -name '*.gguf' -o -name '*.pth' \) \
  -printf '  %-46p %6.2f GB\n' 2>/dev/null \
  | sed "s|$COMFY_HOME/models/||" \
  || du -h "$COMFY_HOME/models" | tail -20

echo
ok "next: scripts/04-install-custom-nodes.sh"
