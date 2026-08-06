#!/usr/bin/env bash
# Step 4 - install custom nodes.
#
# Deliberately minimal. All eight bundled workflows run on ComfyUI CORE nodes
# only, so nothing here is required for them to work. We install just two
# widely-used, actively-maintained packages:
#
#   ComfyUI-Manager  (Comfy-Org, the official node manager)     - convenience
#   ComfyUI-GGUF     (city96, quantised model loaders)          - low-VRAM only
#
# Anything beyond this is opt-in; every extra custom node is extra attack
# surface and extra breakage on ComfyUI upgrades.

. "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
load_hardware

PY="$(python_bin)"
[ -n "$PY" ] || die "no virtualenv - run scripts/01-install-comfyui.sh first"
NODE_DIR="$COMFY_HOME/custom_nodes"
mkdir -p "$NODE_DIR"

step "Step 4/5 - custom nodes"

install_node() {
  local name="$1" url="$2" why="$3"
  local dest="$NODE_DIR/$name"
  if [ -d "$dest/.git" ]; then
    ok "$name already installed"
  else
    info "installing $name  ($why)"
    git clone --depth 1 "$url" "$dest"
  fi
  if [ -f "$dest/requirements.txt" ]; then
    "$PY" -m pip install --quiet -r "$dest/requirements.txt" && ok "$name deps installed"
  fi
}

install_node "ComfyUI-Manager" "https://github.com/Comfy-Org/ComfyUI-Manager.git" \
             "official node/model manager"

if [ "$PROFILE" = "gguf" ] || [ "${FORCE_GGUF:-0}" = "1" ]; then
  install_node "ComfyUI-GGUF" "https://github.com/city96/ComfyUI-GGUF.git" \
               "quantised loaders for the ${VRAM_GB}GB-VRAM profile"
  "$PY" -m pip install --quiet gguf && ok "gguf python package installed"
else
  info "profile '$PROFILE' does not need ComfyUI-GGUF - skipping"
  info "(install later with: FORCE_GGUF=1 scripts/04-install-custom-nodes.sh)"
fi

step "Installed custom nodes"
for d in "$NODE_DIR"/*/; do
  [ -d "$d/.git" ] || continue
  printf '  %-24s %s\n' "$(basename "$d")" "$(git -C "$d" log -1 --format=%cd --date=short 2>/dev/null)"
done

echo
ok "next: scripts/05-install-mcp.sh"
