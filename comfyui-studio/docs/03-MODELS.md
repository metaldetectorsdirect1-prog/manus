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

| File | Dir | Size | Source | Licence |
|---|---|---|---|---|
| `clip_l.safetensors` | `text_encoders` | 0.25 GB | `comfyanonymous/flux_text_encoders` ✅ | Apache-2.0 |
| `ae.safetensors` | `vae` | 0.34 GB | `black-forest-labs/FLUX.1-schnell` | Apache-2.0 |
| `birefnet.safetensors` | `background_removal` | 0.9 GB | `Comfy-Org/BiRefNet` ✅ | MIT |
| `RealESRGAN_x4plus.pth` | `upscale_models` | 0.07 GB | `xinntao/Real-ESRGAN` GitHub release | BSD-3-Clause |

## Per profile

| Profile | File | Dir | Size | Source |
|---|---|---|---|---|
| `high` | `flux1-schnell.safetensors` | `diffusion_models` | 23.8 GB | `black-forest-labs/FLUX.1-schnell` |
| | `t5xxl_fp16.safetensors` | `text_encoders` | 9.79 GB | `comfyanonymous/flux_text_encoders` ✅ |
| `balanced` `low` `cpu` | `flux1-schnell.safetensors` | `diffusion_models` | 23.8 GB | same |
| | `t5xxl_fp8_e4m3fn.safetensors` | `text_encoders` | 4.89 GB | same repo |
| `gguf` | `flux1-schnell-Q4_K_S.gguf` | `diffusion_models` | 6.8 GB | `city96/FLUX.1-schnell-gguf` |
| | `t5-v1_1-xxl-encoder-Q5_K_M.gguf` | `text_encoders` | 3.9 GB | `city96/t5-v1_1-xxl-encoder-gguf` |

✅ = URL taken **verbatim from a manifest shipped inside ComfyUI 0.30.0**
(`blueprints/*.json`), so it is ComfyUI-official. The rest follow the documented
upstream layout but could not be reached from the authoring environment — see
the honesty note below.

## Licensing — why Schnell and not dev

| Model | Licence | Commercial output |
|---|---|---|
| **FLUX.1 Schnell** | **Apache-2.0** | **yes, unrestricted** |
| FLUX.1 dev | FLUX.1-dev Non-Commercial | **no** |
| FLUX.1 pro | closed, API only | n/a |

Only Schnell is installed. It is also *ungated* — no HuggingFace token, no
licence click-through. `HUGGINGFACE_TOKEN` is supported but unnecessary.

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

`huggingface.co` was **unreachable** from the environment where this pack was
authored (blocked by egress policy), so:

- no weights were ever downloaded here
- the HuggingFace URLs marked without ✅ were **not** confirmed to return 200
- the GitHub RealESRGAN URL **was** confirmed reachable

This is exactly why the preflight exists: it checks on *your* machine, before
committing to 30 GB.

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
| `high` | ~34 GB | ~8 GB | 50 GB |
| `balanced` / `low` / `cpu` | ~29 GB | ~8 GB | 45 GB |
| `gguf` | ~12 GB | ~8 GB | 25 GB |

Generated images land in `$COMFY_HOME/output/` and grow over time — a 1024×1024
PNG is roughly 1–2 MB.
