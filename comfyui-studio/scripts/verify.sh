#!/usr/bin/env bash
# End-to-end health check. Safe to run any time; changes nothing.
#
# Checks: venv, torch+accelerator, ComfyUI API, model files on disk,
# custom nodes, workflow validity, and MCP registration.

. "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
load_hardware

# A health check must report every problem, not abort on the first one.
set +e
set +o pipefail

FAILED=0
check() { # check <label> <ok?> [detail]
  if [ "$2" = "0" ]; then ok "$1${3:+ - $3}"; else err "$1${3:+ - $3}"; FAILED=$((FAILED+1)); fi
}

step "1. Python environment"
PY="$(python_bin)"
[ -n "$PY" ]; check "virtualenv at $VENV_DIR" "$?"
if [ -n "$PY" ]; then
  TORCH="$("$PY" -c 'import torch;print(torch.__version__)' 2>/dev/null || echo missing)"
  [ "$TORCH" != "missing" ]; check "torch installed" "$?" "$TORCH"
  ACCEL="$("$PY" -c 'import torch;print("cuda" if torch.cuda.is_available() else ("mps" if getattr(torch.backends,"mps",None) and torch.backends.mps.is_available() else "cpu"))' 2>/dev/null || echo unknown)"
  if [ "$ACCEL" = "cpu" ] && [ "$GPU_VENDOR" != "none" ]; then
    check "GPU acceleration" 1 "a $GPU_VENDOR GPU exists but torch reports CPU"
  else
    check "accelerator" 0 "$ACCEL"
  fi
fi

step "2. ComfyUI server"
if comfy_up; then
  VER="$(curl -fsS --noproxy '*' "$COMFY_URL/system_stats" | sed -n 's/.*"comfyui_version": "\([^"]*\)".*/\1/p')"
  check "API reachable at $COMFY_URL" 0 "ComfyUI $VER"
  NODES="$(curl -fsS --noproxy '*' "$COMFY_URL/object_info" | "$PY" -c 'import json,sys;print(len(json.load(sys.stdin)))' 2>/dev/null || echo 0)"
  check "node types loaded" "$([ "${NODES:-0}" -gt 100 ] && echo 0 || echo 1)" "$NODES nodes"
else
  check "API reachable at $COMFY_URL" 1 "start it with scripts/start-comfyui.sh"
fi

step "3. Models on disk"
CFG="$STUDIO_DIR/config/model-profiles.json"
MISSING=0
while IFS= read -r line; do
  name="${line%%|*}"; dir="${line##*|}"
  if [ -f "$COMFY_HOME/models/$dir/$name" ]; then
    sz="$(du -h "$COMFY_HOME/models/$dir/$name" | cut -f1)"
    ok "models/$dir/$name ($sz)"
  else
    err "models/$dir/$name MISSING"; MISSING=$((MISSING+1))
  fi
done < <("$PY" - "$CFG" "$PROFILE" <<'PYCODE'
import json, sys
cfg = json.load(open(sys.argv[1])); p = cfg["profiles"][sys.argv[2]]
models = list(cfg["common_models"])
src = p.get("inherits_models_from")
models += cfg["profiles"][src]["models"] if src else p.get("models", [])
for m in models:
    print(f"{m['name']}|{m['dir']}")
PYCODE
)
[ "$MISSING" -eq 0 ]; check "all profile '$PROFILE' models present" "$?" "$MISSING missing"

step "4. Custom nodes"
for d in "$COMFY_HOME"/custom_nodes/*/; do
  [ -d "$d/.git" ] || continue
  ok "$(basename "$d") ($(git -C "$d" log -1 --format=%cd --date=short 2>/dev/null))"
done

step "5. Workflows"
if comfy_up; then
  WF_OUT="$("$PY" "$STUDIO_DIR/scripts/validate-workflows.py" --url "$COMFY_URL" 2>&1)"
  WF_RC=$?
  echo "$WF_OUT" | tail -12
  check "workflow validation" "$WF_RC"
else
  warn "skipped - ComfyUI is not running"
fi

step "6. Claude Code MCP"
if have claude && claude mcp list 2>/dev/null | grep -q '^comfyui\b'; then
  check "MCP server registered" 0 "claude mcp list"
elif grep -q '"comfyui"' "$HOME/.claude/settings.json" 2>/dev/null; then
  check "MCP server registered" 0 "~/.claude/settings.json"
else
  check "MCP server registered" 1 "run scripts/05-install-mcp.sh"
fi
NODE_OK=1; [ "${NODE_VER%%.*}" -ge 22 ] 2>/dev/null && NODE_OK=0
check "Node >= 22" "$NODE_OK" "$NODE_VER"

echo
if [ "$FAILED" -eq 0 ]; then
  ok "everything checks out"
else
  err "$FAILED check(s) failed - see docs/06-TROUBLESHOOTING.md"
  exit 1
fi
