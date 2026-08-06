# 07 — Complete file map

Everything this pack creates, installs, or modifies.

## In this repository

```
comfyui-studio/
├── README.md                                   overview + verification record
├── config/
│   ├── model-profiles.json                     profiles, URLs, sizes, licences
│   └── mcp.example.json                        MCP snippet for settings.json
├── docs/
│   ├── 01-HARDWARE.md   02-INSTALL.md   03-MODELS.md   04-WORKFLOWS.md
│   └── 05-MCP.md        06-TROUBLESHOOTING.md   07-FILE-MAP.md
├── packs/flux1-schnell/
│   ├── pack.yaml                               comfyui-mcp pack descriptor
│   └── manifest.yaml                           comfyui-mcp install manifest
├── scripts/
│   ├── lib/common.sh                           shared helpers
│   ├── 00-check-hardware.sh                    gate — no download until it passes
│   ├── 01-install-comfyui.sh                   clone + isolated venv
│   ├── 02-install-pytorch.sh                   CUDA / ROCm / MPS / CPU autodetect
│   ├── 03-download-models.sh                   preflight, confirm, fetch
│   ├── 04-install-custom-nodes.sh              Manager (+ GGUF on low VRAM)
│   ├── 05-install-mcp.sh                       register with Claude Code
│   ├── install.sh                              runs 00→05
│   ├── start-studio.sh                         ONE-CLICK launcher
│   ├── start-comfyui.sh / stop-comfyui.sh
│   ├── verify.sh                               health check
│   ├── validate-workflows.py                   graph validator
│   ├── apply-profile.py                        retarget workflows at a profile
│   └── windows/
│       ├── Check-Hardware.ps1
│       ├── Install-Studio.ps1                  -Step check|comfyui|pytorch|nodes|models|mcp|all
│       └── Start-Studio.ps1
└── workflows/
    ├── 01-txt2img.json                    9 nodes
    ├── 02-img2img.json                   11 nodes
    ├── 03-product-background-replace.json 16 nodes
    ├── 04-upscale.json                    4 nodes
    ├── 05-transparent-product.json        6 nodes
    ├── 06-marketplace-1x1.json            9 nodes
    ├── 07-social-4x5.json                 9 nodes
    └── 08-youtube-16x9.json               9 nodes
```

## Installed on your machine

### `$COMFY_HOME` — default `~/ComfyUI`

```
~/ComfyUI/
├── main.py, nodes.py, comfy/, comfy_extras/     ComfyUI 0.30.0 checkout
├── .venv/                                       isolated Python env (~8 GB)
├── blueprints/                                  ComfyUI's own model manifests
├── custom_nodes/
│   ├── ComfyUI-Manager/                         official node manager
│   └── ComfyUI-GGUF/                            only on the gguf profile
├── models/
│   ├── diffusion_models/   flux1-schnell.safetensors   (or …-Q4_K_S.gguf)
│   ├── text_encoders/      clip_l.safetensors
│   │                       t5xxl_fp16.safetensors | t5xxl_fp8_e4m3fn.safetensors
│   │                       (or t5-v1_1-xxl-encoder-Q5_K_M.gguf)
│   ├── vae/                ae.safetensors
│   ├── upscale_models/     RealESRGAN_x4plus.pth
│   └── background_removal/ birefnet.safetensors
├── input/                                       source images for img2img
└── output/                                      GENERATED IMAGES LAND HERE
```

### `$STATE_DIR` — default `~/.comfyui-studio`

| File | Purpose |
|---|---|
| `hardware.env` | detection result (Windows: `hardware.json`) |
| `manifest-<profile>.tsv` | resolved download list for the active profile |
| `comfyui.log` | server log from `start-comfyui.sh --background` |
| `comfyui.pid` | pid, used by `stop-comfyui.sh` |

### Modified outside the repo

| File | Change | Safety |
|---|---|---|
| `~/.claude/settings.json` | adds `mcpServers.comfyui` | **timestamped backup first**; refuses if not valid JSON; leaves an existing `comfyui` entry alone |

That is the **only** file outside `$COMFY_HOME` and `$STATE_DIR` that is touched.
No system-wide installs, no services, no PATH edits, no registry keys, no sudo.

## Commands

### Install
| Command | Does |
|---|---|
| `./scripts/install.sh` | everything, 00→05 |
| `ASSUME_YES=1 ./scripts/install.sh` | unattended |
| `./scripts/00-check-hardware.sh` | detect only, no install |
| `./scripts/0{1..5}-*.sh` | individual steps |

### Run
| Command | Does |
|---|---|
| `./scripts/start-studio.sh` | **one-click**: ComfyUI background + MCP status |
| `./scripts/start-comfyui.sh` | foreground |
| `./scripts/start-comfyui.sh --background` | detached, logs to `$STATE_DIR` |
| `./scripts/stop-comfyui.sh` | stop (only this toolchain's pid) |

### Check
| Command | Does |
|---|---|
| `./scripts/verify.sh` | full health check |
| `python3 scripts/validate-workflows.py` | validate graphs against a live server |
| `python3 scripts/validate-workflows.py --skip-live` | structural only |

### Reconfigure
| Command | Does |
|---|---|
| `python3 scripts/apply-profile.py --profile gguf` | retarget workflows |
| `python3 scripts/apply-profile.py --profile high --dry-run` | preview |
| `PROFILE_OVERRIDE=gguf ./scripts/03-download-models.sh` | fetch another profile |
| `FORCE_GGUF=1 ./scripts/04-install-custom-nodes.sh` | add GGUF node anyway |

### Environment
`COMFY_HOME` · `VENV_DIR` · `COMFY_PORT` · `COMFY_HOST` · `STATE_DIR` ·
`ASSUME_YES` · `PROFILE_OVERRIDE` · `FORCE_GGUF` · `HUGGINGFACE_TOKEN` ·
`EXTRA_COMFY_ARGS` — see [02-INSTALL.md](02-INSTALL.md).

## Ports

| Port | Service | Bind |
|---|---|---|
| 8188 | ComfyUI HTTP API + web UI | `127.0.0.1` (local only) |

The MCP server speaks stdio to Claude Code and HTTP to ComfyUI; it opens no port
of its own.

## Disk

| Item | Size |
|---|---|
| ComfyUI checkout | ~200 MB |
| `.venv` incl. PyTorch | ~6–8 GB |
| Models (`balanced`) | ~29 GB |
| Models (`gguf`) | ~12 GB |
| **Total (`balanced`)** | **~37 GB** |
| **Total (`gguf`)** | **~20 GB** |
