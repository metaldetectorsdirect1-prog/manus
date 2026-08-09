#!/usr/bin/env bash
# Clone and set up the ten open-source video generators, in one pass.
#
# Written because this container has no GPU and no route to Hugging Face, so
# the install done here stops at source + runtime. Everything below the CLONE
# section is what has to happen on a box that *can* run them. Run it there.
#
#   ./scripts/video-models-setup.sh clone          # source only, ~400 MB
#   ./scripts/video-models-setup.sh comfyui        # + ComfyUI runtime
#   ./scripts/video-models-setup.sh weights        # + the small model weights
#
# VRAM figures are each repo's own README, not a blog roundup. They are the
# floor for the smallest published variant, not for the headline model.
set -euo pipefail

ROOT="${VIDEO_MODELS_DIR:-$HOME/video-models}"
VENV="$ROOT/.venv"

# repo                                  dir             min VRAM   entry point
REPOS=(
  "comfyanonymous/ComfyUI                ComfyUI         cpu-ok     main.py"
  "hpcaitech/Open-Sora                   Open-Sora       52GB       scripts/diffusion/inference.py"
  "lllyasviel/FramePack                  FramePack       6GB        demo_gradio.py"
  "Wan-Video/Wan2.2                      Wan2.2          24GB       generate.py"
  "zai-org/CogVideo                      CogVideo        4.4GB      inference/cli_demo.py"
  "Tencent-Hunyuan/HunyuanVideo          HunyuanVideo    45GB       sample_video.py"
  "Lightricks/LTX-Video                  LTX-Video       8GB        inference.py"
  "deepbeepmeep/Wan2GP                   Wan2GP          6GB        wgp.py"
  "SkyworkAI/SkyReels-V2                 SkyReels-V2     14.7GB     generate_video.py"
  "genmoai/mochi                         mochi           20GB       demos/cli.py"
)

clone() {
  mkdir -p "$ROOT"; cd "$ROOT"
  for line in "${REPOS[@]}"; do
    read -r repo dir _ _ <<<"$line"
    if [ -d "$dir/.git" ]; then
      echo "have  $dir"
    elif git clone --depth 1 "https://github.com/$repo.git" "$dir" >/dev/null 2>&1; then
      echo "ok    $dir"
    else
      echo "FAIL  $dir  ($repo)"
    fi
  done
  du -sh "$ROOT"
}

# ComfyUI is the only one of the ten that runs without a GPU, and it is the
# umbrella the others load through — Wan, LTX, Hunyuan, CogVideoX and Mochi all
# have native ComfyUI support, so this one runtime covers most of the list.
# On a CUDA box, install torch from the cu12x index instead; the plain PyPI
# wheel below drags ~4 GB of nvidia-* packages in either way.
comfyui() {
  [ -d "$ROOT/ComfyUI" ] || { echo "clone first"; exit 1; }
  python3 -m venv "$VENV" 2>/dev/null || true
  "$VENV/bin/pip" install --no-cache-dir -q torch torchvision torchaudio
  "$VENV/bin/pip" install --no-cache-dir -q -r "$ROOT/ComfyUI/requirements.txt"
  echo "launch:  $VENV/bin/python $ROOT/ComfyUI/main.py --cpu --listen 127.0.0.1 --port 8188"
}

# Only the two that fit on a consumer card. The 14B-class weights are 30–60 GB
# each and there is no point pulling them onto a machine that cannot load them.
# Needs huggingface.co reachable — it is NOT reachable from the Claude Code
# container, which is why this is a separate step rather than part of comfyui.
weights() {
  "$VENV/bin/pip" install --no-cache-dir -q "huggingface_hub[cli]"
  "$VENV/bin/hf" download Lightricks/LTX-Video \
      --include "ltxv-2b-0.9.8-distilled.safetensors" \
      --local-dir "$ROOT/ComfyUI/models/checkpoints"
  "$VENV/bin/hf" download zai-org/CogVideoX-2b \
      --local-dir "$ROOT/ComfyUI/models/CogVideo/CogVideoX-2b"
}

case "${1:-clone}" in
  clone)   clone ;;
  comfyui) comfyui ;;
  weights) weights ;;
  all)     clone; comfyui; weights ;;
  *)       echo "usage: $0 {clone|comfyui|weights|all}"; exit 2 ;;
esac
