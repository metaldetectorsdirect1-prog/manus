# 03 — Models

Every file, where it goes, where it comes from, and what licence it carries.
The machine-readable source of truth is
[`config/model-profiles.json`](../config/model-profiles.json).

## Directory layout

ComfyUI's model directories, using the exact mapping ComfyUI itself ships in
`blueprints/Text to Image (Flux.1 Dev).json`:

```
$COMFY_HOME/models/
├── diffusion_models/   flux1-schnell.safetensors        ← the FLUX UNet
├── text_encoders/      clip_l.safetensors, t5xxl_*.safetensors
├── vae/                ae.safetensors
├── upscale_models/     RealESRGAN_x4plus.pth
└── background_removal/ birefnet.safetensors             ← ComfyUI 0.30 core
```

> The GGUF profile puts its `.gguf` files in the **same** directories.
> ComfyUI-GGUF aliases `unet_gguf → diffusion_models` and
> `clip_gguf → text_encoders`, so nothing separate is needed.

## Always installed

| File | Dir | Bytes | Size | Source | Licence |
|---|---|---|---|---|---|
| `clip_l.safetensors` | `text_encoders` | 246,144,152 | 0.25 GB | `comfyanonymous/flux_text_encoders` | Apache-2.0 |
| `ae.safetensors` | `vae` | 335,304,388 | 0.34 GB | `black-forest-labs/FLUX.1-schnell` 🔒 | Apache-2.0 |
| `birefnet.safetensors` | `background_removal` | 444,473,596 | 0.44 GB | `Comfy-Org/BiRefNet` | MIT |
| `RealESRGAN_x4plus.pth` | `upscale_models` | 67,040,989 | 0.07 GB | `xinntao/Real-ESRGAN` GitHub release | BSD-3-Clause |

## Per profile

| Profile | File | Dir | Bytes | Size | Source |
|---|---|---|---|---|---|
| `high` | `flux1-schnell.safetensors` | `diffusion_models` | 23,782,506,688 | 23.78 GB | `black-forest-labs/FLUX.1-schnell` 🔒 |
| | `t5xxl_fp16.safetensors` | `text_encoders` | 9,787,841,024 | 9.79 GB | `comfyanonymous/flux_text_encoders` |
| `balanced` `low` `cpu` | `flux1-schnell.safetensors` | `diffusion_models` | 23,782,506,688 | 23.78 GB | same 🔒 |
| | `t5xxl_fp8_e4m3fn.safetensors` | `text_encoders` | 4,893,934,904 | 4.89 GB | same repo |
| `gguf` | `flux1-schnell-Q4_K_S.gguf` | `diffusion_models` | 6,783,943,712 | 6.78 GB | `city96/FLUX.1-schnell-gguf` |
| | `t5-v1_1-xxl-encoder-Q5_K_M.gguf` | `text_encoders` | 3,386,856,640 | 3.39 GB | `city96/t5-v1_1-xxl-encoder-gguf` |

🔒 = gated repo, automatic ungated mirror configured (see below).

**Every file above was verified to exist at that exact path with that exact byte
count**, via the HuggingFace Hub API (and an HTTP HEAD for the GitHub release).
Licences were read from the repo metadata: FLUX.1-schnell `apache-2.0`,
Comfy-Org/flux1-schnell `apache-2.0`, Comfy-Org/BiRefNet `mit`,
city96/FLUX.1-schnell-gguf `apache-2.0`.

## Licensing — why Schnell and not dev

| Model | Licence | Commercial output |
|---|---|---|
| **FLUX.1 Schnell** | **Apache-2.0** | **yes, unrestricted** |
| FLUX.1 dev | FLUX.1-dev Non-Commercial | **no** |
| FLUX.1 pro | closed, API only | n/a |

Only Schnell is installed.

### The BFL repo is gated — and that is handled

`black-forest-labs/FLUX.1-schnell` is a **gated** HuggingFace repo. Its files
return **401/403 without a token**, even though the model is Apache-2.0. You have
two options, and the installer takes the second automatically:

1. **Use the official BFL source.** Accept the licence on
   [the model page](https://huggingface.co/black-forest-labs/FLUX.1-schnell),
   create a token at <https://huggingface.co/settings/tokens>, then:
   ```bash
   HUGGINGFACE_TOKEN=hf_xxx ./scripts/03-download-models.sh
   ```
2. **Do nothing.** The preflight detects the 401/403 and falls back to the
   **ungated Comfy-Org mirror**, which hosts *byte-identical* files:

   | File | BFL (gated) | Comfy-Org mirror (ungated) |
   |---|---|---|
   | `flux1-schnell.safetensors` | 23,782,506,688 | **23,782,506,688** |
   | `ae.safetensors` | 335,304,388 | **335,304,388** |

   Same bytes, same Apache-2.0 licence, no token. The preflight prints
   `upstream is gated (HTTP 401) - using the ungated mirror` when this happens.

No other model in this pack is gated.

Schnell is guidance- and timestep-distilled, which is why the workflows use
**4 steps at CFG 1.0**. Raising either makes output *worse*, not better — see
[04-WORKFLOWS.md](04-WORKFLOWS.md).

Support models: BiRefNet is MIT, RealESRGAN is BSD-3-Clause, T5-v1.1-XXL and
CLIP-L are Apache-2.0. Everything in this pack is commercially usable.

## The preflight gate

`03-download-models.sh` never starts a large transfer on trust:

```
Phase 1 - preflight (no data transferred)
==> free disk at /home/you/ComfyUI: 512 GB (need ~34 GB)
  ok reachable: clip_l.safetensors
  ok reachable: ae.safetensors
  ...
```

If any URL fails it prints which one and exits **having downloaded nothing**.
A mirror is tried automatically where one is configured (currently `ae.safetensors`
and `flux1-schnell.safetensors`).

### If a URL has moved

Model repos reorganise. To fix:

1. Open the repo page, e.g. `https://huggingface.co/black-forest-labs/FLUX.1-schnell/tree/main`
2. Find the file, copy its **resolve** URL:
   `https://huggingface.co/<repo>/resolve/main/<path>`
3. Update the entry in `config/model-profiles.json`
4. Re-run `./scripts/03-download-models.sh` — files already on disk are skipped

### Honesty note

Direct HTTPS to `huggingface.co` was blocked by egress policy in the authoring
environment, so **no weights were ever downloaded here**. Every path, byte count
and licence above was instead confirmed through the HuggingFace Hub API, which
was reachable. What remains unproven is only the bulk transfer itself — the
preflight re-checks all of it on your machine before committing to 30 GB.

## Verifying what you have

```bash
./scripts/verify.sh                       # includes a per-file presence check
du -h ~/ComfyUI/models/*/*.{safetensors,gguf,pth} 2>/dev/null
```

## Optional: Qwen-Image (typography)

FLUX.1 Schnell renders short text acceptably but is not a typography model.
Qwen-Image 20B is much stronger for text-heavy layouts.

**Gated at ≥ 12 GB VRAM and ≥ 80 GB free disk** — it is a 20B model and will not
run usefully below that. `00-check-hardware.sh` reports `Qwen-Image (opt) yes/no`.

The cleanest install is through the MCP server's own pack system rather than
duplicating a manifest here — `comfyui-mcp` ships a `qwen-image` pack:

> Install the qwen-image pack.

That pulls the Qwen-Image GGUF (Q4_K_S under 12 GB, Q5_K_S for 12–24 GB, Q8_0 for
24 GB+), the Qwen2.5-VL 7B text encoder, the VAE, and the Lightning acceleration
LoRAs, into the correct directories. Upstream:
`https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI`.

Qwen-Image needs its own workflow — the FLUX graphs here will not drive it, and
none of the eight bundled workflows change when you install it.

## Disk budget

| Profile | Weights | + venv/PyTorch | Recommended free |
|---|---|---|---|
| `high` | 34.67 GB | ~8 GB | 50 GB |
| `balanced` / `low` / `cpu` | 29.77 GB | ~8 GB | 45 GB |
| `gguf` | 11.27 GB | ~8 GB | 25 GB |

Generated images land in `$COMFY_HOME/output/` and grow over time — a 1024×1024
PNG is roughly 1–2 MB.
