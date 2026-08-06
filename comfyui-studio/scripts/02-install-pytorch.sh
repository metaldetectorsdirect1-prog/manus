#!/usr/bin/env bash
# Step 2 - install the PyTorch build that matches the detected hardware,
# then the rest of ComfyUI's Python requirements.

. "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"
load_hardware

PY="$(python_bin)"
[ -n "$PY" ] || die "no virtualenv at $VENV_DIR - run scripts/01-install-comfyui.sh first"

step "Step 2/5 - PyTorch for $GPU_VENDOR (${VRAM_GB:-0} GB VRAM)"

# Pick the wheel index. The PyTorch CUDA wheels bundle their own CUDA runtime,
# so a system CUDA toolkit / nvcc is NOT required - only a recent driver.
TORCH_INDEX=""
case "$GPU_VENDOR" in
  nvidia)
    # Driver -> CUDA wheel. Newer drivers are backward compatible, so we pick the
    # newest wheel line the driver supports.
    major="${CUDA_VER%%.*}"; minor="$(echo "$CUDA_VER" | cut -d. -f2)"
    if   [ "${major:-0}" -ge 13 ] 2>/dev/null; then TORCH_INDEX="https://download.pytorch.org/whl/cu130"
    elif [ "${major:-0}" -eq 12 ] && [ "${minor:-0}" -ge 8 ] 2>/dev/null; then TORCH_INDEX="https://download.pytorch.org/whl/cu128"
    elif [ "${major:-0}" -eq 12 ] 2>/dev/null; then TORCH_INDEX="https://download.pytorch.org/whl/cu124"
    else
      warn "CUDA runtime reported as '${CUDA_VER}' - falling back to cu124."
      warn "If torch.cuda.is_available() is False afterwards, update your NVIDIA driver."
      TORCH_INDEX="https://download.pytorch.org/whl/cu124"
    fi
    info "NVIDIA detected -> $TORCH_INDEX"
    ;;
  amd)
    TORCH_INDEX="https://download.pytorch.org/whl/rocm6.2"
    info "AMD/ROCm detected -> $TORCH_INDEX"
    warn "ROCm support is Linux-only and card-dependent; verify after install."
    ;;
  apple)
    info "Apple Silicon detected -> default PyPI wheels (MPS backend, no index override)"
    ;;
  none)
    TORCH_INDEX="https://download.pytorch.org/whl/cpu"
    warn "No GPU -> CPU-only PyTorch. Generation will take minutes per image."
    ;;
esac

info "installing torch / torchvision / torchaudio (this is a large download)"
if [ -n "$TORCH_INDEX" ]; then
  "$PY" -m pip install --upgrade torch torchvision torchaudio --index-url "$TORCH_INDEX"
else
  "$PY" -m pip install --upgrade torch torchvision torchaudio
fi

info "installing ComfyUI requirements"
"$PY" -m pip install -r "$COMFY_HOME/requirements.txt"

step "Verifying the PyTorch install"
"$PY" - <<'PYCODE'
import sys, torch
print(f"  torch          {torch.__version__}")
cuda = torch.cuda.is_available()
mps = getattr(torch.backends, "mps", None)
mps = bool(mps and mps.is_available())
if cuda:
    print(f"  CUDA device    {torch.cuda.get_device_name(0)}")
    print(f"  VRAM           {torch.cuda.get_device_properties(0).total_memory/1024**3:.1f} GB")
elif mps:
    print("  MPS backend    available (Apple Silicon)")
else:
    print("  accelerator    NONE - running on CPU")
PYCODE

ACCEL="$("$PY" -c 'import torch;print("cuda" if torch.cuda.is_available() else ("mps" if getattr(torch.backends,"mps",None) and torch.backends.mps.is_available() else "cpu"))')"
if [ "$GPU_VENDOR" != "none" ] && [ "$ACCEL" = "cpu" ]; then
  warn "A $GPU_VENDOR GPU was detected but PyTorch cannot use it."
  warn "Most common cause: the GPU driver is older than the CUDA wheel line."
  warn "See docs/06-TROUBLESHOOTING.md."
fi

echo
ok "next: scripts/03-download-models.sh"
