# 01 — Hardware

`scripts/00-check-hardware.sh` (or `windows/Check-Hardware.ps1`) is the gate.
It downloads and installs nothing; it only measures and decides.

## What it inspects

| Item | Linux / macOS source | Windows source |
|---|---|---|
| OS + version | `/etc/os-release`, `sw_vers` | `Win32_OperatingSystem` |
| Architecture | `uname -m` | `PROCESSOR_ARCHITECTURE` |
| CPU cores | `nproc` / `sysctl hw.ncpu` | `Win32_ComputerSystem` |
| RAM | `/proc/meminfo` / `hw.memsize` | `Win32_ComputerSystem` |
| Free disk | `df` on `$HOME` | `Get-PSDrive` |
| GPU model | `nvidia-smi`, `rocminfo`, Apple Silicon detect | `nvidia-smi`, `Win32_VideoController` |
| **GPU VRAM** | `nvidia-smi --query-gpu=memory.total` | same |
| CUDA runtime | `nvidia-smi` header | same |
| Driver version | `nvidia-smi` | same |
| Python | first `python3.{12,11,10}` ≥ 3.10 | `python`/`py` ≥ 3.10 |
| Git / Node / npm | `--version` | `--version` |
| `nvcc` | optional, reported only | — |

`nvcc` is **not** required. PyTorch's CUDA wheels bundle their own CUDA runtime;
only a recent NVIDIA **driver** matters.

Results are written to `~/.comfyui-studio/hardware.env`
(Windows: `hardware.json`) and read by every later script.

## Profile thresholds

| Profile | VRAM | UNet | T5 text encoder | Download | Flags |
|---|---|---|---|---|---|
| `high` | ≥ 24 GB | `flux1-schnell.safetensors` bf16 | `t5xxl_fp16` | 34.7 GB | — |
| `balanced` | 16–23 GB | same, `weight_dtype=fp8_e4m3fn` | `t5xxl_fp8_e4m3fn` | 29.8 GB | — |
| `low` | 10–15 GB | same as balanced | `t5xxl_fp8_e4m3fn` | 29.8 GB | `--lowvram` |
| `gguf` | 6–9 GB | `flux1-schnell-Q4_K_S.gguf` | `t5-v1_1-xxl-encoder-Q5_K_M.gguf` | 11.3 GB | `--lowvram` |
| `cpu` | none | bf16 | `t5xxl_fp8_e4m3fn` | 29.8 GB | `--cpu` |

`balanced` downloads the same 23.8 GB bf16 file as `high` and casts it to fp8
**at load time** — that saves VRAM, not disk. The `gguf` profile is the only one
that meaningfully reduces download size, because the weights themselves are
quantised on disk.

## Blockers vs warnings

**Blockers** stop the install (exit 1, nothing downloaded):

- Python < 3.10 or missing
- Git missing
- Node.js < 22 or missing (the MCP server requires it)
- Free disk < profile download + 15 GB

**Warnings** let it continue:

- RAM < 16 GB — FLUX needs roughly 16 GB of *system* RAM to load comfortably,
  independently of VRAM
- No GPU — works, but expect minutes per image instead of seconds

## Platform notes

**NVIDIA** is the well-supported path. The CUDA wheel line is chosen from the
runtime `nvidia-smi` reports: ≥ 13.0 → cu130, ≥ 12.8 → cu128, 12.x → cu124.

**Apple Silicon** uses the MPS backend and default PyPI wheels; unified memory
means VRAM is reported as system RAM, so an 8 GB Mac is genuinely tight.

**AMD** gets ROCm wheels **on Linux only**. There is no ROCm PyTorch build for
Windows — on Windows an AMD card falls back to CPU, and the Windows script says
so. Use WSL2 with the bash scripts for AMD acceleration.

## Re-running

Safe and idempotent. Re-run it after a driver update, a GPU swap, or freeing
disk; every later script picks up the new profile. To force a different profile
without re-detecting:

```bash
PROFILE_OVERRIDE=gguf ./scripts/03-download-models.sh
python3 scripts/apply-profile.py --profile gguf
```

## Reference: this pack's authoring environment

For calibration — the machine these scripts were *built and tested* on was
deliberately hostile: **no GPU at all**.

```
OS         Ubuntu 24.04.4 LTS (x86_64)     CPU        4 cores
RAM        15 GB                            Free disk  24 GB
GPU        none  (no nvidia-smi, no /dev/dri, no VGA device)
Python     3.11.15 / 3.12                   Git 2.43.0    Node 22.22.2
CUDA       none
→ profile  cpu   → blocked: needs ~45 GB free, found 24 GB
```

That is the check working correctly: it refused to install. See the
Verification table in the main [README](../README.md).
