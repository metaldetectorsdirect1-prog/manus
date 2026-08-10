#!/usr/bin/env bash
# One-command installer: runs steps 0-5 in order and stops at the first failure.
#
#   scripts/install.sh                 # interactive (asks before the big download)
#   ASSUME_YES=1 scripts/install.sh    # unattended
#
# Step 0 is a hard gate: if the hardware check reports blockers, nothing is
# downloaded or installed.

. "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"

step "ComfyUI Studio - full install"
cat <<EOF
  ComfyUI       -> $COMFY_HOME
  virtualenv    -> $VENV_DIR
  state/logs    -> $STATE_DIR
  workflows     -> $STUDIO_DIR/workflows

  Override the install location with:  COMFY_HOME=/path scripts/install.sh
EOF

if [ "${ASSUME_YES:-0}" != "1" ]; then
  confirm "Proceed?" || { info "aborted"; exit 0; }
fi

run() {
  local script="$1"
  step "Running $(basename "$script")"
  bash "$script" || die "$(basename "$script") failed - fix the problem above and re-run scripts/install.sh"
}

run "$STUDIO_DIR/scripts/00-check-hardware.sh"
run "$STUDIO_DIR/scripts/01-install-comfyui.sh"
run "$STUDIO_DIR/scripts/02-install-pytorch.sh"
run "$STUDIO_DIR/scripts/04-install-custom-nodes.sh"   # before models: gguf profile needs the node
run "$STUDIO_DIR/scripts/03-download-models.sh"
run "$STUDIO_DIR/scripts/05-install-mcp.sh"

step "Install complete"
ok "start everything with: scripts/start-studio.sh"
ok "then verify with:      scripts/verify.sh"
