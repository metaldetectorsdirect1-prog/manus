#!/usr/bin/env bash
# Step 3 - download FLUX.1 Schnell + support models for the detected profile.
#
# Requirement: nothing large is fetched until hardware AND every URL is verified.
# The script therefore runs in two phases:
#   PHASE 1  HEAD-check every URL and re-check free disk. Downloads nothing.
#            Writes a RESOLVED manifest naming the URL that actually answered.
#   PHASE 2  only after phase 1 is clean (and you confirm) does it fetch weights.
#
# Note on gating: black-forest-labs/FLUX.1-schnell is a GATED HuggingFace repo.
# Without HUGGINGFACE_TOKEN its URLs return 401/403, so phase 1 automatically
# falls back to the ungated Comfy-Org mirror, which hosts byte-identical files.

. "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
load_hardware

PY="$(python_bin)"
[ -n "$PY" ] || die "no virtualenv - run scripts/01-install-comfyui.sh first"
[ -d "$COMFY_HOME" ] || die "ComfyUI is not installed at $COMFY_HOME - run scripts/01-install-comfyui.sh first"

CFG="${CFG:-$STUDIO_DIR/config/model-profiles.json}"
[ -f "$CFG" ] || die "missing $CFG"

PROFILE="${PROFILE_OVERRIDE:-$PROFILE}"
step "Step 3/5 - models for profile '$PROFILE'"

# Resolve the profile's file list (common + profile, following inherits_models_from).
MANIFEST="$STATE_DIR/manifest-$PROFILE.tsv"
RESOLVED="$STATE_DIR/resolved-$PROFILE.tsv"
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
printf '  %-44s %-26s %7s\n' FILE DIRECTORY SIZE_GB
while IFS=$'\t' read -r name dir url size lic verified mirror; do
  printf '  %-44s %-26s %7s\n' "$name" "models/$dir" "$size"
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

# HEAD-check a URL and echo only the FINAL status code (curl prints one per
# redirect hop, and HF serves weights off a CDN).
head_code() {
  local c
  c="$(curl -sSL -o /dev/null -w '%{http_code}' --max-time 45 -I \
        ${HUGGINGFACE_TOKEN:+-H "Authorization: Bearer $HUGGINGFACE_TOKEN"} \
        "$1" 2>/dev/null | tail -c 3 || true)"
  echo "${c:-000}"
}

: > "$RESOLVED"
BAD=0
GATED_HINT=0
while IFS=$'\t' read -r name dir url size lic verified mirror; do
  dest="$COMFY_HOME/models/$dir/$name"
  if [ -f "$dest" ]; then
    ok "already present, skipping: $name"
    continue
  fi

  use=""
  code="$(head_code "$url")"
  if [ "$code" = "200" ]; then
    use="$url"
    ok "reachable: $name"
  elif [ -n "$mirror" ]; then
    mcode="$(head_code "$mirror")"
    if [ "$mcode" = "200" ]; then
      use="$mirror"
      if [ "$code" = "401" ] || [ "$code" = "403" ]; then
        warn "$name: upstream is gated (HTTP $code) - using the ungated mirror"
        GATED_HINT=1
      else
        warn "$name: primary returned $code - using the mirror"
      fi
    fi
  fi

  if [ -n "$use" ]; then
    printf '%s\t%s\t%s\t%s\n' "$name" "$dir" "$use" "$size" >> "$RESOLVED"
  else
    err "$name unreachable (HTTP $code) - $url"
    [ "$code" = "401" ] || [ "$code" = "403" ] && GATED_HINT=1
    BAD=$((BAD+1))
  fi
done < "$MANIFEST"

if [ "$BAD" -gt 0 ]; then
  echo
  err "$BAD file(s) could not be verified. NOTHING has been downloaded."
  if [ "$GATED_HINT" = "1" ]; then
    err "At least one 401/403 - that repo is GATED on HuggingFace. Either:"
    err "  1. accept the licence on the model page, create a token at"
    err "     https://huggingface.co/settings/tokens, then re-run with"
    err "     HUGGINGFACE_TOKEN=hf_xxx scripts/03-download-models.sh"
    err "  2. or add an ungated 'mirror' for it in $CFG"
  fi
  err "Model repos also move files; see docs/03-MODELS.md to find the current path."
  exit 1
fi

if [ ! -s "$RESOLVED" ]; then
  ok "every model for profile '$PROFILE' is already installed"
else
  echo
  ok "all URLs verified, disk is sufficient"
  if [ "${SKIP_CONFIRM:-0}" != "1" ]; then
    confirm "Download ${TOTAL_GB} GB of model weights now?" || { info "aborted - nothing downloaded"; exit 0; }
  fi

  # -------------------------------------------------------------- PHASE 2
  step "Phase 2 - downloading"
  while IFS=$'\t' read -r name dir url size; do
    dest="$COMFY_HOME/models/$dir/$name"
    mkdir -p "$(dirname "$dest")"
    info "downloading $name (${size} GB) -> models/$dir/"
    # -C - resumes a partial file; write to .part so an interrupted run never
    # leaves a truncated file that looks complete.
    curl -fL --retry 5 --retry-delay 5 --retry-all-errors -C - \
         ${HUGGINGFACE_TOKEN:+-H "Authorization: Bearer $HUGGINGFACE_TOKEN"} \
         -o "${dest}.part" "$url"
    mv "${dest}.part" "$dest"
    ok "$name"
  done < "$RESOLVED"
fi

# ---------------------------------------------------------------- point workflows at these files
info "aligning workflows with profile '$PROFILE'"
"$PY" "$STUDIO_DIR/scripts/apply-profile.py" --profile "$PROFILE" --config "$CFG" >/dev/null
ok "workflows updated"

step "Installed models"
find "$COMFY_HOME/models" -type f \( -name '*.safetensors' -o -name '*.gguf' -o -name '*.pth' \) \
  -printf '  %-52p %6.2f GB\n' 2>/dev/null \
  | sed "s|$COMFY_HOME/models/||" \
  || du -h "$COMFY_HOME/models" | tail -20

echo
ok "next: scripts/05-install-mcp.sh"
