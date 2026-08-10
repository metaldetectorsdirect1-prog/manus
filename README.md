# manus

Working repository for Metal Detectors Direct.

## Branches

Each work stream lives on its own branch and merges here.

| Branch | Contents |
|---|---|
| `claude/instagram-metaldetectorsdirect-b79oy7` | Instagram growth audit, 60-day posting plan and R&D tracker, ComfyUI + Wan2.1 installer |
| `claude/hivolt-store-admin-6e3q23` | Hivolt store admin work |
| `claude/comfyui-local-setup-nmnjs7` | ComfyUI Studio — local FLUX.1 Schnell image generation driven from Claude Code |

## Contents of this line of work

- `instagram-growth-audit.md` — capability audit against the 1M-follower target, organic-only
- `tools/format-rd-tracker.xlsx` — 60-day plan, hook bank, post log, format scorecard, seeding tracker
- `install_comfyui_wan.py` — local ComfyUI + Wan2.1 installer for an NVIDIA machine

## ComfyUI Studio

A completely free, fully local, open-source image-generation stack you drive from
Claude Code — ComfyUI + FLUX.1 Schnell + the `comfyui-mcp` bridge, with eight
ready-made e-commerce workflows.

**→ [`comfyui-studio/`](comfyui-studio/README.md)**

**Linux / macOS**

```bash
cd comfyui-studio
./scripts/install.sh        # hardware check → ComfyUI → PyTorch → models → MCP
./scripts/start-studio.sh   # one-click launch
./scripts/verify.sh         # health check
```

**Windows** (PowerShell — one command per line; `&&` is not valid in PowerShell 5.1)

```powershell
cd comfyui-studio\scripts\windows
powershell -ExecutionPolicy Bypass -File .\Check-Hardware.ps1
powershell -ExecutionPolicy Bypass -File .\Install-Studio.ps1
powershell -ExecutionPolicy Bypass -File .\Start-Studio.ps1
```

No paid APIs, no cloud services, no accounts. Every model is permissively
licensed (Apache-2.0 / MIT / BSD-3-Clause), so generated images are unrestricted
for commercial use.

> Complements the existing `install_comfyui_wan.py` (Wan2.1 **video**, NVIDIA-only)
> rather than replacing it: this pack covers **still images** with FLUX.1 Schnell,
> auto-detects CUDA / ROCm / MPS / CPU, and is driven through Claude Code over MCP.

| | |
|---|---|
| Install guide | [comfyui-studio/docs/02-INSTALL.md](comfyui-studio/docs/02-INSTALL.md) |
| Workflows | [comfyui-studio/docs/04-WORKFLOWS.md](comfyui-studio/docs/04-WORKFLOWS.md) |
| Claude Code wiring | [comfyui-studio/docs/05-MCP.md](comfyui-studio/docs/05-MCP.md) |
| Troubleshooting | [comfyui-studio/docs/06-TROUBLESHOOTING.md](comfyui-studio/docs/06-TROUBLESHOOTING.md) |
| Self-audit | [comfyui-studio/docs/08-AUDIT.md](comfyui-studio/docs/08-AUDIT.md) |
