#!/usr/bin/env bash
# Step 1 - clone ComfyUI from the official repo and create an isolated venv.
# No model weights are downloaded here (that is step 3).

. "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
load_hardware

REPO_URL="${COMFY_REPO_URL:-https://github.com/Comfy-Org/ComfyUI.git}"

step "Step 1/5 - install ComfyUI into $COMFY_HOME"

# ---------------------------------------------------------------- clone
if [ -d "$COMFY_HOME/.git" ]; then
  existing="$(git -C "$COMFY_HOME" remote get-url origin 2>/dev/null || echo '?')"
  info "existing checkout found (origin: $existing)"
  if confirm "Run 'git pull' to update it?"; then
    git -C "$COMFY_HOME" pull --ff-only || warn "pull failed - continuing with the current checkout"
  fi
elif [ -e "$COMFY_HOME" ]; then
  # Never clobber a non-empty directory we did not create.
  die "$COMFY_HOME exists but is not a git checkout. Move it aside or set COMFY_HOME=<other path>."
else
  info "cloning $REPO_URL"
  git clone --depth 1 "$REPO_URL" "$COMFY_HOME"
fi
ok "ComfyUI at $COMFY_HOME ($(cat "$COMFY_HOME/comfyui_version.py" 2>/dev/null | sed -n 's/.*__version__ = "\(.*\)".*/\1/p' || echo 'version unknown'))"

# ---------------------------------------------------------------- venv
if [ -d "$VENV_DIR" ]; then
  ok "virtualenv already present at $VENV_DIR"
else
  info "creating isolated virtualenv at $VENV_DIR"
  "$PY_BIN" -m venv "$VENV_DIR"
  ok "virtualenv created with $PY_BIN ($PY_VER)"
fi

PY="$(python_bin)"
[ -n "$PY" ] || die "virtualenv python not found under $VENV_DIR"

info "upgrading pip inside the venv"
"$PY" -m pip install --quiet --upgrade pip setuptools wheel

# ---------------------------------------------------------------- model dirs
# ComfyUI creates these itself, but making them up-front lets step 3 verify paths.
for d in diffusion_models text_encoders vae upscale_models background_removal loras unet; do
  mkdir -p "$COMFY_HOME/models/$d"
done
ok "model directories ready under $COMFY_HOME/models/"

echo
ok "next: scripts/02-install-pytorch.sh"
