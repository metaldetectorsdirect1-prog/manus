#!/usr/bin/env bash
# One-click ComfyUI launcher.
# Reads the profile chosen by 00-check-hardware.sh and applies its VRAM flags.
#
#   scripts/start-comfyui.sh              # foreground
#   scripts/start-comfyui.sh --background # detach, log to ~/.comfyui-studio/comfyui.log
#   COMFY_PORT=8189 scripts/start-comfyui.sh

. "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
load_hardware

PY="$(python_bin)"
[ -n "$PY" ] || die "no virtualenv at $VENV_DIR - run scripts/01-install-comfyui.sh first"
[ -f "$COMFY_HOME/main.py" ] || die "ComfyUI not found at $COMFY_HOME"

if comfy_up; then
  ok "ComfyUI is already running at $COMFY_URL"
  exit 0
fi

# shellcheck disable=SC2206
FLAGS=($LAUNCH_FLAGS)
[ -n "${EXTRA_COMFY_ARGS:-}" ] && FLAGS+=($EXTRA_COMFY_ARGS)

step "Starting ComfyUI"
info "profile   $PROFILE"
info "flags     ${FLAGS[*]:-<none>}"
info "url       $COMFY_URL"

LOG="$STATE_DIR/comfyui.log"
mkdir -p "$STATE_DIR"

if [ "${1:-}" = "--background" ]; then
  cd "$COMFY_HOME"
  nohup "$PY" main.py --port "$COMFY_PORT" --listen "$COMFY_HOST" "${FLAGS[@]}" >"$LOG" 2>&1 &
  echo $! > "$STATE_DIR/comfyui.pid"
  info "pid $(cat "$STATE_DIR/comfyui.pid"), logging to $LOG"
  # Poll the API instead of sleeping blindly.
  if curl -fsS --noproxy '*' --retry 60 --retry-delay 2 --retry-connrefused --retry-all-errors \
          --max-time 180 "$COMFY_URL/system_stats" >/dev/null 2>&1; then
    ok "ComfyUI API is up at $COMFY_URL"
  else
    err "ComfyUI did not come up in time - last 20 log lines:"
    tail -20 "$LOG" >&2
    exit 1
  fi
else
  cd "$COMFY_HOME"
  exec "$PY" main.py --port "$COMFY_PORT" --listen "$COMFY_HOST" "${FLAGS[@]}"
fi
