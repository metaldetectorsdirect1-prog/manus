#!/usr/bin/env bash
# Stop a ComfyUI started by start-comfyui.sh --background.
# Only ever kills the PID this toolchain wrote - never a broad pkill.

. "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"

PIDFILE="$STATE_DIR/comfyui.pid"
if [ ! -f "$PIDFILE" ]; then
  info "no pid file at $PIDFILE"
  comfy_up && warn "something is still serving $COMFY_URL - it was not started by this script, leaving it alone"
  exit 0
fi

PID="$(cat "$PIDFILE")"
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID" && ok "stopped ComfyUI (pid $PID)"
else
  info "pid $PID is not running"
fi
rm -f "$PIDFILE"
