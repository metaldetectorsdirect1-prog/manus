#!/usr/bin/env bash
# One-click "everything up" script: starts ComfyUI in the background, waits for
# its API, and confirms the MCP server can be launched by Claude Code.
#
# This is the script to double-click / alias. Run it, then talk to Claude.

. "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"

step "ComfyUI Studio"

"$STUDIO_DIR/scripts/start-comfyui.sh" --background

load_hardware

# ---------------------------------------------------------------- MCP check
step "MCP bridge"
if have node && [ "${NODE_VER%%.*}" -ge 22 ] 2>/dev/null; then
  ok "Node $NODE_VER (>= 22 required)"
else
  err "Node >= 22 not available - Claude Code cannot start comfyui-mcp"
fi

REGISTERED="no"
if have claude && claude mcp list 2>/dev/null | grep -q '^comfyui\b'; then
  REGISTERED="yes (claude mcp list)"
elif [ -f "$HOME/.claude/settings.json" ] && grep -q '"comfyui"' "$HOME/.claude/settings.json" 2>/dev/null; then
  REGISTERED="yes (~/.claude/settings.json)"
fi
if [ "$REGISTERED" = "no" ]; then
  warn "MCP server 'comfyui' is not registered - run scripts/05-install-mcp.sh"
else
  ok "MCP server registered: $REGISTERED"
fi

# ---------------------------------------------------------------- summary
step "Ready"
cat <<EOF
  ComfyUI web UI    $COMFY_URL
  ComfyUI API       $COMFY_URL/prompt
  Profile           $PROFILE  (${LAUNCH_FLAGS:-no special flags})
  Workflows         $STUDIO_DIR/workflows/
  Logs              $STATE_DIR/comfyui.log
  Stop with         scripts/stop-comfyui.sh

  Now ask Claude Code, for example:

    Generate a premium photorealistic e-commerce product advertisement,
    1:1 aspect ratio, professional studio lighting, clean composition,
    realistic shadows and sufficient negative space for marketing text.
EOF
