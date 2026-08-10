#!/usr/bin/env bash
# Step 0 - inspect the machine and decide which FLUX.1 Schnell profile it can run.
# Writes ~/.comfyui-studio/hardware.env, which every later step reads.
# NOTHING is downloaded or installed by this script.

. "$(dirname "${BASH_SOURCE[0]}")/lib/common.sh"

mkdir -p "$STATE_DIR"

step "ComfyUI Studio - hardware inspection"

# ---------------------------------------------------------------- OS
OS_KIND="$(uname -s)"
case "$OS_KIND" in
  Linux)  OS_NAME="$(. /etc/os-release 2>/dev/null && echo "${PRETTY_NAME:-Linux}")" ;;
  Darwin) OS_NAME="macOS $(sw_vers -productVersion 2>/dev/null || echo '?')" ;;
  *)      OS_NAME="$OS_KIND" ;;
esac
ARCH="$(uname -m)"
info "OS:        $OS_NAME ($ARCH)"

# ---------------------------------------------------------------- CPU / RAM
CPU_CORES="$( (nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null) || echo '?')"
if [ "$OS_KIND" = "Darwin" ]; then
  RAM_BYTES="$(sysctl -n hw.memsize 2>/dev/null || echo 0)"
  RAM_GB=$(( RAM_BYTES / 1024 / 1024 / 1024 ))
else
  RAM_KB="$(awk '/MemTotal/{print $2}' /proc/meminfo 2>/dev/null || echo 0)"
  RAM_GB=$(( RAM_KB / 1024 / 1024 ))
fi
info "CPU cores: $CPU_CORES"
info "RAM:       ${RAM_GB} GB"

# ---------------------------------------------------------------- disk
DISK_AVAIL_GB="$(df -Pk "$HOME" 2>/dev/null | awk 'NR==2{print int($4/1024/1024)}')"
DISK_AVAIL_GB="${DISK_AVAIL_GB:-0}"
info "Free disk: ${DISK_AVAIL_GB} GB (on $HOME)"

# ---------------------------------------------------------------- GPU
GPU_VENDOR="none"; GPU_NAME="none"; VRAM_GB=0; CUDA_VER="none"; DRIVER_VER="none"

if have nvidia-smi && nvidia-smi -L >/dev/null 2>&1; then
  GPU_VENDOR="nvidia"
  GPU_NAME="$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -1)"
  VRAM_MB="$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)"
  VRAM_GB=$(( ${VRAM_MB:-0} / 1024 ))
  DRIVER_VER="$(nvidia-smi --query-gpu=driver_version --format=csv,noheader 2>/dev/null | head -1)"
  CUDA_VER="$(nvidia-smi 2>/dev/null | sed -n 's/.*CUDA Version: *\([0-9.]*\).*/\1/p' | head -1)"
elif [ "$OS_KIND" = "Darwin" ] && [ "$ARCH" = "arm64" ]; then
  GPU_VENDOR="apple"
  GPU_NAME="$(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo 'Apple Silicon')"
  VRAM_GB="$RAM_GB"          # unified memory
elif have rocminfo && rocminfo >/dev/null 2>&1; then
  GPU_VENDOR="amd"
  GPU_NAME="$(rocminfo 2>/dev/null | sed -n 's/.*Marketing Name: *//p' | grep -v CPU | head -1)"
  VRAM_MB="$( (rocm-smi --showmeminfo vram 2>/dev/null | sed -n 's/.*Total.*: *\([0-9]*\).*/\1/p' | head -1) || echo 0)"
  VRAM_GB=$(( ${VRAM_MB:-0} / 1024 / 1024 ))
fi

if [ "$GPU_VENDOR" = "none" ]; then
  warn "GPU:       none detected - CPU-only mode (very slow: minutes per image)"
else
  info "GPU:       $GPU_NAME ($GPU_VENDOR)"
  info "VRAM:      ${VRAM_GB} GB"
  [ "$CUDA_VER" != "none" ] && info "CUDA:      $CUDA_VER (driver $DRIVER_VER)"
fi

# ---------------------------------------------------------------- toolchain
PY_BIN=""
for c in python3.12 python3.11 python3.10 python3 python; do
  if have "$c"; then
    v="$("$c" -c 'import sys;print("%d.%d"%sys.version_info[:2])' 2>/dev/null || echo 0.0)"
    major="${v%%.*}"; minor="${v##*.}"
    if [ "$major" = "3" ] && [ "$minor" -ge 10 ] 2>/dev/null; then PY_BIN="$c"; PY_VER="$v"; break; fi
  fi
done
if [ -n "$PY_BIN" ]; then info "Python:    $PY_VER ($PY_BIN)"; else warn "Python:    no >=3.10 found"; fi

GIT_VER="$(git --version 2>/dev/null | awk '{print $3}' || echo none)"
NODE_VER="$(node --version 2>/dev/null | tr -d v || echo none)"
NPM_VER="$(npm --version 2>/dev/null || echo none)"
NVCC_VER="$(nvcc --version 2>/dev/null | sed -n 's/.*release \([0-9.]*\).*/\1/p' || echo none)"
info "Git:       $GIT_VER"
info "Node:      $NODE_VER (npm $NPM_VER)"
info "nvcc:      ${NVCC_VER:-none} (optional - the PyTorch wheel bundles its own CUDA)"

# ---------------------------------------------------------------- profile
# Profiles decide which weights get downloaded and how ComfyUI is launched.
# Download sizes are the verified byte counts from config/model-profiles.json,
# rounded up: common files total 1.10 GB, plus the profile's UNet + T5.
#   high     >=24GB VRAM  bf16 UNet + t5xxl_fp16          34.67 -> 35 GB
#   balanced 16-23GB      bf16 UNet cast fp8 + t5 fp8     29.77 -> 30 GB
#   low      10-15GB      same as balanced + --lowvram    29.77 -> 30 GB
#   gguf      6-9GB       Q4_K_S GGUF + t5 GGUF           11.27 -> 12 GB (needs ComfyUI-GGUF)
#   cpu      no GPU       bf16 + t5 fp8, --cpu            29.77 -> 30 GB, minutes/image
PROFILE="cpu"; LAUNCH_FLAGS="--cpu"; EST_DOWNLOAD_GB=30
if [ "$GPU_VENDOR" = "nvidia" ] || [ "$GPU_VENDOR" = "amd" ] || [ "$GPU_VENDOR" = "apple" ]; then
  if   [ "$VRAM_GB" -ge 24 ]; then PROFILE="high";     LAUNCH_FLAGS="";           EST_DOWNLOAD_GB=35
  elif [ "$VRAM_GB" -ge 16 ]; then PROFILE="balanced"; LAUNCH_FLAGS="";           EST_DOWNLOAD_GB=30
  elif [ "$VRAM_GB" -ge 10 ]; then PROFILE="low";      LAUNCH_FLAGS="--lowvram";  EST_DOWNLOAD_GB=30
  elif [ "$VRAM_GB" -ge 6  ]; then PROFILE="gguf";     LAUNCH_FLAGS="--lowvram";  EST_DOWNLOAD_GB=12
  else                             PROFILE="cpu";      LAUNCH_FLAGS="--cpu";      EST_DOWNLOAD_GB=30
  fi
fi
# Apple Silicon uses MPS, not CUDA, and never wants --cpu.
if [ "$GPU_VENDOR" = "apple" ]; then LAUNCH_FLAGS=""; [ "$RAM_GB" -lt 16 ] && LAUNCH_FLAGS="--lowvram"; fi

# Qwen-Image is a 20B model - only offer it on genuinely capable hardware.
QWEN_OK="no"
[ "$VRAM_GB" -ge 12 ] && [ "$DISK_AVAIL_GB" -ge 80 ] && QWEN_OK="yes"

step "Verdict"
printf '  profile           %s%s%s\n' "$C_BLD" "$PROFILE" "$C_OFF"
printf '  launch flags      %s\n' "${LAUNCH_FLAGS:-<none>}"
printf '  model download    ~%s GB\n' "$EST_DOWNLOAD_GB"
printf '  Qwen-Image (opt)  %s\n' "$QWEN_OK"

BLOCKERS=0
if [ -z "$PY_BIN" ]; then err "Python >= 3.10 is required"; BLOCKERS=$((BLOCKERS+1)); fi
if [ "$GIT_VER" = "none" ]; then err "Git is required"; BLOCKERS=$((BLOCKERS+1)); fi
if [ "$NODE_VER" = "none" ]; then
  err "Node.js >= 22 is required for the MCP server"; BLOCKERS=$((BLOCKERS+1))
elif [ "${NODE_VER%%.*}" -lt 22 ] 2>/dev/null; then
  err "Node.js is $NODE_VER - the MCP server needs >= 22"; BLOCKERS=$((BLOCKERS+1))
fi

NEED_GB=$(( EST_DOWNLOAD_GB + 15 ))     # weights + venv + PyTorch + headroom
if [ "$DISK_AVAIL_GB" -lt "$NEED_GB" ]; then
  err "Need ~${NEED_GB} GB free, found ${DISK_AVAIL_GB} GB"; BLOCKERS=$((BLOCKERS+1))
fi
if [ "$RAM_GB" -lt 16 ]; then
  warn "RAM is ${RAM_GB} GB. FLUX needs ~16 GB system RAM to load comfortably."
fi
if [ "$PROFILE" = "cpu" ]; then
  warn "No usable GPU: generation will take MINUTES per image, not seconds."
fi

cat > "$HW_REPORT" <<EOF
# Generated by 00-check-hardware.sh on $(date -u +%Y-%m-%dT%H:%M:%SZ)
OS_KIND="$OS_KIND"
OS_NAME="$OS_NAME"
ARCH="$ARCH"
CPU_CORES="$CPU_CORES"
RAM_GB="$RAM_GB"
DISK_AVAIL_GB="$DISK_AVAIL_GB"
GPU_VENDOR="$GPU_VENDOR"
GPU_NAME="$GPU_NAME"
VRAM_GB="$VRAM_GB"
CUDA_VER="$CUDA_VER"
DRIVER_VER="$DRIVER_VER"
PY_BIN="$PY_BIN"
PY_VER="${PY_VER:-none}"
GIT_VER="$GIT_VER"
NODE_VER="$NODE_VER"
PROFILE="$PROFILE"
LAUNCH_FLAGS="$LAUNCH_FLAGS"
EST_DOWNLOAD_GB="$EST_DOWNLOAD_GB"
QWEN_OK="$QWEN_OK"
BLOCKERS="$BLOCKERS"
EOF

echo
if [ "$BLOCKERS" -gt 0 ]; then
  die "$BLOCKERS blocker(s) above must be fixed before installing. Nothing was downloaded."
fi
ok "hardware verified - report written to $HW_REPORT"
ok "next: scripts/01-install-comfyui.sh"
