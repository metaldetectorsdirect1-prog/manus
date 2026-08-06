#!/usr/bin/env bash
# Step 5 - wire artokun/comfyui-mcp into Claude Code.
#
# The package is published to npm as `comfyui-mcp` and runs via npx, so there is
# no global install. This script warms the npx cache, then registers the server
# in Claude Code's settings - preferring the official `claude mcp add` CLI and
# falling back to a careful, backed-up JSON edit.

. "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
load_hardware

step "Step 5/5 - comfyui-mcp for Claude Code"

[ "$NODE_VER" != "none" ] || die "Node.js is required"
[ "${NODE_VER%%.*}" -ge 22 ] 2>/dev/null || die "comfyui-mcp needs Node >= 22 (found $NODE_VER)"

info "fetching comfyui-mcp from npm (this caches it for npx)"
npm exec --yes comfyui-mcp -- --version >/dev/null 2>&1 \
  || warn "could not run 'comfyui-mcp --version' - npx will fetch it on first use"
VER="$(npm view comfyui-mcp version 2>/dev/null || echo unknown)"
ok "comfyui-mcp version $VER available via npx"

# ---------------------------------------------------------------- register
CLAUDE_SETTINGS="${CLAUDE_SETTINGS:-$HOME/.claude/settings.json}"

if have claude; then
  info "registering via the Claude Code CLI"
  if claude mcp list 2>/dev/null | grep -q '^comfyui\b'; then
    ok "MCP server 'comfyui' already registered"
  else
    # --scope user makes it available in every project.
    if claude mcp add --scope user comfyui -- npx -y comfyui-mcp; then
      ok "registered MCP server 'comfyui'"
    else
      warn "'claude mcp add' failed - falling back to editing settings.json"
      have claude && CLAUDE_CLI_FAILED=1
    fi
  fi
fi

if ! have claude || [ "${CLAUDE_CLI_FAILED:-0}" = "1" ]; then
  info "writing MCP config into $CLAUDE_SETTINGS"
  mkdir -p "$(dirname "$CLAUDE_SETTINGS")"
  PY="$(python_bin)"; [ -n "$PY" ] || PY="$PY_BIN"

  if [ -f "$CLAUDE_SETTINGS" ]; then
    # This is one of the user's real config files - back it up and merge, never overwrite.
    cp -a "$CLAUDE_SETTINGS" "${CLAUDE_SETTINGS}.bak.$(date +%Y%m%d-%H%M%S)"
    ok "backed up existing settings.json"
  fi

  "$PY" - "$CLAUDE_SETTINGS" <<'PYCODE'
import json, os, sys
path = sys.argv[1]
data = {}
if os.path.exists(path):
    try:
        with open(path) as f:
            data = json.load(f)
    except json.JSONDecodeError:
        print(f"  settings.json is not valid JSON - refusing to touch it: {path}")
        sys.exit(1)
servers = data.setdefault("mcpServers", {})
if "comfyui" in servers:
    print("  'comfyui' entry already present - left unchanged")
else:
    servers["comfyui"] = {"command": "npx", "args": ["-y", "comfyui-mcp"]}
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print(f"  added mcpServers.comfyui to {path}")
PYCODE
fi

step "Config written"
cat <<EOF
  MCP server name : comfyui
  command         : npx -y comfyui-mcp
  ComfyUI URL     : $COMFY_URL (auto-detected by the server; ports 8188 then 8000)

  To point it at a ComfyUI on another machine instead, add:
      --comfyui-url http://<host>:8188
  or set COMFYUI_URL in the server's env block.
EOF

echo
warn "Restart Claude Code (or run /mcp) so it picks up the new server."
ok "then ask Claude:  \"What ComfyUI tools do you have?\"  (expect ~86)"
