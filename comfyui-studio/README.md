# ComfyUI Studio — local FLUX.1 Schnell image generation, driven from Claude Code

A completely free, fully local, open-source image-generation stack:

| Piece | What | Licence |
|---|---|---|
| [ComfyUI](https://github.com/Comfy-Org/ComfyUI) `0.30.0` | generation engine + HTTP API | GPL-3.0 |
| [FLUX.1 Schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell) | image model | **Apache-2.0 — commercial use permitted** |
| [comfyui-mcp](https://github.com/artokun/comfyui-mcp) `0.49.8` | MCP bridge so Claude Code drives ComfyUI | MIT |
| BiRefNet | background removal (**ships inside ComfyUI core**) | MIT |
| RealESRGAN x4+ | upscaling | BSD-3-Clause |

No paid APIs, no cloud services, no accounts. Everything runs on your machine.

> **FLUX.1 *dev* is deliberately excluded.** It carries a non-commercial licence.
> Only Apache-2.0 **Schnell** is installed, so generated images are unrestricted
> for commercial use.

---

## Quick start

```bash
# Linux / macOS
git clone <this repo> && cd comfyui-studio
./scripts/install.sh          # hardware check → ComfyUI → PyTorch → models → MCP
./scripts/start-studio.sh     # one-click launch
./scripts/verify.sh           # health check
```

```powershell
# Windows
cd comfyui-studio\scripts\windows
powershell -ExecutionPolicy Bypass -File .\Check-Hardware.ps1
powershell -ExecutionPolicy Bypass -File .\Install-Studio.ps1
powershell -ExecutionPolicy Bypass -File .\Start-Studio.ps1
```

Then restart Claude Code and ask:

> Generate a premium photorealistic e-commerce product advertisement, 1:1 aspect
> ratio, professional studio lighting, clean composition, realistic shadows and
> sufficient negative space for marketing text.

`scripts/install.sh` **will not download a single byte of model weights** until
the hardware check passes *and* every model URL has been HEAD-verified.

---

## The eight workflows

All in `workflows/`, in ComfyUI **API format** — the format `/prompt` and the MCP
consume. Every one of them was validated against a live ComfyUI 0.30.0 server
(see [Verification](#verification)).

| File | Does | Size |
|---|---|---|
| `01-txt2img.json` | text → image | 1024×1024 |
| `02-img2img.json` | image → image, denoise 0.75 | 1024×1024 |
| `03-product-background-replace.json` | cut product out, generate a new background behind it | 1024×1024 |
| `04-upscale.json` | 4× upscale with RealESRGAN | 4× input |
| `05-transparent-product.json` | product on transparent alpha (RGBA PNG) | source res |
| `06-marketplace-1x1.json` | marketplace hero shot | 1024×1024 |
| `07-social-4x5.json` | social advert, headline space on top | 896×1120 |
| `08-youtube-16x9.json` | YouTube thumbnail background | 1344×768 |

**Every workflow uses ComfyUI core nodes only.** No custom node is required for
any of them — that is a deliberate design choice, because each third-party node
is extra breakage on upgrade and extra code running in your Python process.

Two details these graphs get right that hand-written ones usually get wrong:

- `JoinImageWithAlpha` computes `alpha = 1.0 - mask`, so the transparent-product
  workflow **must** put an `InvertMask` after `RemoveBackground`. Without it you
  get a transparent product on an opaque background — exactly backwards.
- `ImageCompositeMasked` shows `source` where `mask == 1`, so the
  background-replacement workflow uses the **same** mask with **no** inversion.

Same mask, opposite polarity, two nodes apart. Both verified against ComfyUI's
own shipped blueprint for BiRefNet.

---

## Hardware profiles

`scripts/00-check-hardware.sh` measures the machine and picks one:

| Profile | VRAM | Weights | Download | Launch flags |
|---|---|---|---|---|
| `high` | ≥ 24 GB | bf16 UNet + fp16 T5 | 34.7 GB | — |
| `balanced` | 16–23 GB | bf16 UNet cast fp8 + fp8 T5 | 29.8 GB | — |
| `low` | 10–15 GB | as balanced | 29.8 GB | `--lowvram` |
| `gguf` | 6–9 GB | Q4_K_S GGUF + GGUF T5 | 11.3 GB | `--lowvram` |
| `cpu` | none | bf16 + fp8 T5 | 29.8 GB | `--cpu` (minutes/image) |

Switching profile later:

```bash
PROFILE_OVERRIDE=gguf ./scripts/03-download-models.sh
python3 scripts/apply-profile.py --profile gguf
```

`apply-profile.py` rewrites the workflows for you — including swapping
`UNETLoader` → `UnetLoaderGGUF` and `DualCLIPLoader` → `DualCLIPLoaderGGUF`
(and dropping the `weight_dtype` / `device` inputs those GGUF loaders don't have).

**Qwen-Image** (optional, typography-heavy work) is gated at ≥ 12 GB VRAM and
≥ 80 GB free disk. It's a 20B model; below that it will not run usefully. See
[docs/03-MODELS.md](docs/03-MODELS.md).

---

## Verification

This pack was built against real upstream source, not from memory. What was
actually executed while authoring it:

| Check | Result |
|---|---|
| ComfyUI 0.30.0 cloned, venv built, PyTorch + 40 deps installed | pass |
| ComfyUI booted; `/system_stats` and `/object_info` served | pass — 825 core nodes |
| All 23 node signatures used by the workflows read from live `/object_info` | pass |
| 8 workflows structurally validated (types, links, slots, required inputs) | **8/8 pass** |
| 8 workflows submitted to ComfyUI's own `/prompt` validator | **8/8 accepted** — only "model not downloaded yet" remained |
| Validator negative-tested against 6 deliberately broken graphs | **6/6 correctly rejected** |
| ComfyUI-GGUF installed; GGUF profile applied and re-validated | **8/8 pass** (831 nodes) |
| Profile round-trip `balanced → gguf → balanced` | pass |
| `00-check-hardware.sh` on a GPU-less box | correctly refused to install |
| `03-download-models.sh` preflight | correctly downloaded **nothing** when URLs unverifiable |
| **`01-install-comfyui.sh` run end-to-end** into a clean prefix | pass — real clone + venv (py3.12) |
| **`04-install-custom-nodes.sh` run end-to-end** | pass — ComfyUI-Manager installed |
| **`05-install-mcp.sh` run end-to-end** | pass — `claude mcp list` → **✓ Connected** |
| **MCP → ComfyUI round trip** (`get_system_stats` through the router) | **pass — returned live ComfyUI 0.30.0 stats** |
| **Every model path + byte count + licence** via the HuggingFace Hub API | **all 9 confirmed** |
| **PowerShell scripts AST-parsed** (pwsh 7.6.4) | **3/3 parse clean** after fixing 1 syntax error |
| `verify.sh` end-to-end | pass |
| `comfyui-mcp` on npm: `0.49.8`, MIT, `node >= 22` | confirmed |

A later self-audit found and fixed seven real defects, including a **PowerShell
syntax error that made `Start-Studio.ps1` unrunnable**, a claim that the FLUX
repo was ungated (**it is gated**), and a `sed \t` construct that breaks on
macOS/BSD. See [docs/08-AUDIT.md](docs/08-AUDIT.md) for the full list.

**Still not verified, and you should treat it as such:**

- **No GPU was present** in the authoring environment, so the CUDA/ROCm/MPS
  branches of `02-install-pytorch.sh` are unexercised. CPU-only PyTorch was.
- **No weights were ever downloaded.** Direct HTTPS to `huggingface.co` was
  blocked, so while every file's path, byte count and licence is confirmed via
  the Hub API, the bulk transfer itself is untested. The preflight re-checks on
  your machine before committing to 30 GB.
- **The PowerShell scripts were parsed, not executed** — no Windows host. Parsing
  catches syntax and reserved-variable errors, not runtime behaviour. They remain
  the least-tested part of this pack; on Windows, WSL2 + the bash scripts is the
  path that was actually run.
- **No image has been generated**, and Claude has not viewed one. That needs
  weights on real hardware.

---

## Layout

```
comfyui-studio/
├── README.md
├── config/
│   ├── model-profiles.json      # profiles, model URLs, sizes, licences
│   └── mcp.example.json         # MCP snippet for ~/.claude/settings.json
├── docs/                        # 01-HARDWARE … 08-AUDIT
├── packs/flux1-schnell/         # comfyui-mcp-compatible install manifest
├── scripts/
│   ├── install.sh               # runs 00→05
│   ├── 00-check-hardware.sh     # gate: no download until this passes
│   ├── 01-install-comfyui.sh    # clone + isolated venv
│   ├── 02-install-pytorch.sh    # auto-detects CUDA / ROCm / MPS / CPU
│   ├── 03-download-models.sh    # preflight, then fetch
│   ├── 04-install-custom-nodes.sh
│   ├── 05-install-mcp.sh        # registers 'comfyui' in Claude Code
│   ├── start-studio.sh          # ONE-CLICK: ComfyUI + MCP status
│   ├── start-comfyui.sh / stop-comfyui.sh
│   ├── verify.sh                # health check
│   ├── validate-workflows.py    # graph validator (used above)
│   ├── apply-profile.py         # retarget workflows at a profile
│   ├── lib/common.sh
│   └── windows/*.ps1
└── workflows/                   # the 8 API-format graphs
```

Installed **outside** the repo:

| Path | What |
|---|---|
| `~/ComfyUI` | ComfyUI checkout (override with `COMFY_HOME`) |
| `~/ComfyUI/.venv` | isolated Python environment |
| `~/ComfyUI/models/**` | weights (see [docs/03-MODELS.md](docs/03-MODELS.md)) |
| `~/ComfyUI/output` | generated images |
| `~/.comfyui-studio/` | `hardware.env`, `comfyui.log`, `comfyui.pid` |
| `~/.claude/settings.json` | MCP registration (backed up before edit) |

Full inventory: [docs/07-FILE-MAP.md](docs/07-FILE-MAP.md).

---

## Safety

Nothing here deletes or silently overwrites your files.

- `01-install-comfyui.sh` refuses to touch `$COMFY_HOME` if it exists and isn't a
  git checkout.
- `05-install-mcp.sh` **backs up `~/.claude/settings.json`** before merging, and
  refuses to touch it if it isn't valid JSON.
- `stop-comfyui.sh` only kills the PID this toolchain wrote — never a broad `pkill`.
- The big download asks for confirmation (skip with `ASSUME_YES=1`).

## Docs

| | |
|---|---|
| [01-HARDWARE.md](docs/01-HARDWARE.md) | what's detected, profile thresholds |
| [02-INSTALL.md](docs/02-INSTALL.md) | step-by-step install, env overrides |
| [03-MODELS.md](docs/03-MODELS.md) | every file, URL, size, licence; Qwen-Image |
| [04-WORKFLOWS.md](docs/04-WORKFLOWS.md) | node-by-node walkthrough, tuning |
| [05-MCP.md](docs/05-MCP.md) | Claude Code wiring, prompts to use |
| [06-TROUBLESHOOTING.md](docs/06-TROUBLESHOOTING.md) | OOM, CUDA mismatch, MCP issues |
| [07-FILE-MAP.md](docs/07-FILE-MAP.md) | complete inventory |
| [08-AUDIT.md](docs/08-AUDIT.md) | self-audit: defects found and fixed |
