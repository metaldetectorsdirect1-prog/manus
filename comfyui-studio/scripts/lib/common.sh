#!/usr/bin/env bash
# Shared helpers for the ComfyUI Studio installer scripts.
# Sourced by every 0X-*.sh script. Not meant to be run directly.

set -euo pipefail

# ---------------------------------------------------------------- paths
# This file lives at <studio>/scripts/lib/common.sh, so go up two levels.
STUDIO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"       # .../comfyui-studio
REPO_DIR="$(cd "$STUDIO_DIR/.." && pwd)"

# Where ComfyUI itself gets installed. Override with COMFY_HOME.
COMFY_HOME="${COMFY_HOME:-$HOME/ComfyUI}"
VENV_DIR="${VENV_DIR:-$COMFY_HOME/.venv}"
COMFY_PORT="${COMFY_PORT:-8188}"
COMFY_HOST="${COMFY_HOST:-127.0.0.1}"
COMFY_URL="http://${COMFY_HOST}:${COMFY_PORT}"

STATE_DIR="${STATE_DIR:-$HOME/.comfyui-studio}"
HW_REPORT="$STATE_DIR/hardware.env"

# ---------------------------------------------------------------- output
if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  C_RED=$'\033[31m'; C_GRN=$'\033[32m'; C_YEL=$'\033[33m'
  C_BLU=$'\033[34m'; C_DIM=$'\033[2m';  C_OFF=$'\033[0m'; C_BLD=$'\033[1m'
else
  C_RED=; C_GRN=; C_YEL=; C_BLU=; C_DIM=; C_OFF=; C_BLD=
fi

info()  { printf '%s==>%s %s\n' "$C_BLU" "$C_OFF" "$*"; }
ok()    { printf '%s  ok%s %s\n' "$C_GRN" "$C_OFF" "$*"; }
warn()  { printf '%swarn%s %s\n' "$C_YEL" "$C_OFF" "$*" >&2; }
err()   { printf '%s fail%s %s\n' "$C_RED" "$C_OFF" "$*" >&2; }
die()   { err "$*"; exit 1; }
step()  { printf '\n%s%s%s\n' "$C_BLD" "$*" "$C_OFF"; }

# Ask a yes/no question. Honours ASSUME_YES=1 for unattended runs.
confirm() {
  local prompt="$1"
  if [ "${ASSUME_YES:-0}" = "1" ]; then
    info "$prompt -> yes (ASSUME_YES)"
    return 0
  fi
  local reply
  printf '%s%s%s [y/N] ' "$C_YEL" "$prompt" "$C_OFF"
  read -r reply </dev/tty || reply=""
  case "$reply" in [yY]|[yY][eE][sS]) return 0 ;; *) return 1 ;; esac
}

have() { command -v "$1" >/dev/null 2>&1; }

# Never delete or overwrite anything the user might care about without asking.
# (Requirement: "Ask permission before deleting or modifying important files".)
guard_overwrite() {
  local path="$1" what="${2:-file}"
  [ -e "$path" ] || return 0
  warn "$what already exists: $path"
  confirm "Overwrite it? A timestamped .bak copy will be kept first." || return 1
  cp -a "$path" "${path}.bak.$(date +%Y%m%d-%H%M%S)"
  ok "backed up $path"
  return 0
}

python_bin() {
  if [ -x "$VENV_DIR/bin/python" ]; then echo "$VENV_DIR/bin/python"
  elif [ -x "$VENV_DIR/Scripts/python.exe" ]; then echo "$VENV_DIR/Scripts/python.exe"
  else echo ""; fi
}

load_hardware() {
  [ -f "$HW_REPORT" ] || die "no hardware report - run scripts/00-check-hardware.sh first"
  # shellcheck disable=SC1090
  . "$HW_REPORT"
}

comfy_up() {
  curl -fsS --noproxy '*' --max-time 5 "$COMFY_URL/system_stats" >/dev/null 2>&1
}
