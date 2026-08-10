# 04 — Workflows

Eight graphs in [`../workflows/`](../workflows/), ComfyUI **API format** (the flat
`{node_id: {class_type, inputs}}` shape that `/prompt` and the MCP consume).

**All eight use ComfyUI core nodes only.** Nothing here needs a custom node.

Every graph was validated against a live ComfyUI 0.30.0 — structurally (types,
links, slots, required inputs) and by submission to ComfyUI's own `/prompt`
validator. Re-check any time:

```bash
python3 scripts/validate-workflows.py            # needs ComfyUI running
python3 scripts/validate-workflows.py --skip-live
```

## FLUX.1 Schnell settings — do not "improve" these

```
steps          4        sampler   euler
cfg            1.0      scheduler simple
negative       ConditioningZeroOut
```

Schnell is **guidance-distilled and timestep-distilled**. It was trained to
produce a finished image in ~4 steps at CFG 1.0.

- Raising **CFG above 1.0** does not increase prompt adherence — it produces
  burnt, oversaturated output.
- Raising **steps** past ~8 costs time for no gain.
- The **negative prompt does nothing** at CFG 1.0. That is why the graphs use
  `ConditioningZeroOut` fed from the positive encode rather than a second
  `CLIPTextEncode` — it is the pattern ComfyUI itself ships, and it skips a
  redundant T5 pass.

If you want negative prompts and CFG, that is FLUX.1 **dev** — a different model
with a non-commercial licence, deliberately excluded here.

## The shared loader trio

Nodes `10`/`11`/`12` in every generating workflow:

```
VAELoader        ae.safetensors                        → VAE
DualCLIPLoader   clip_l.safetensors + t5xxl_*, type=flux → CLIP
UNETLoader       flux1-schnell.safetensors, weight_dtype → MODEL
```

`clip_name1` is CLIP-L, `clip_name2` is T5 — that order matters and matches
ComfyUI's own FLUX blueprint. `weight_dtype` is set per profile by
`apply-profile.py` (`default` or `fp8_e4m3fn`).

## 01 — text to image

```
UNETLoader ─┐
CLIPTextEncode(prompt) ─→ ConditioningZeroOut ─┐
EmptySD3LatentImage(1024×1024) ────────────────┴→ KSampler → VAEDecode → SaveImage
```

`EmptySD3LatentImage` — not `EmptyLatentImage`. FLUX uses the SD3-style 16-channel
latent; the wrong node produces noise.

## 02 — image to image

```
LoadImage → ImageScale(1024×1024, bicubic, crop=center) → VAEEncode → KSampler(denoise=0.75)
```

`denoise` is the dial: `0.3` nudges, `0.75` (default) restyles while keeping
composition, `0.95` keeps only the broadest layout.

## 03 — product background replacement

```
FLUX txt2img ──────────────────────────────→ new background ─┐
LoadImage → ImageScale(1024²) ─┬──────────────────────────────┤
                              └→ RemoveBackground → GrowMask(-2) → FeatherMask(2) ─┤
                                                                ImageCompositeMasked ─→ SaveImage
```

`RemoveBackground` (BiRefNet, core since ComfyUI 0.30) returns a mask where
**1 = product**. `ImageCompositeMasked` draws `source` where `mask == 1`, so the
mask is used **directly, with no inversion**.

`GrowMask(expand=-2)` shrinks the mask 2 px to kill the halo of original
background that always survives at the edge; `FeatherMask` then softens it.

Prompt the *background*, not the product — the product is composited in, not
generated.

## 04 — upscale

```
LoadImage → UpscaleModelLoader(RealESRGAN_x4plus.pth) → ImageUpscaleWithModel → SaveImage
```

Pure ESRGAN 4×; no diffusion, so it is fast and does not invent detail. To land
on an exact size, add an `ImageScale` after the upscale.

## 05 — transparent product (RGBA PNG)

```
LoadImage ─┬─────────────────────────────────────┐
           └→ RemoveBackground → InvertMask → JoinImageWithAlpha → SaveImage
```

**`InvertMask` is mandatory.** `JoinImageWithAlpha` computes
`alpha = 1.0 - mask` internally. `RemoveBackground` gives `1 = product`. Without
the inversion the product becomes transparent and the background opaque —
precisely inverted. This is ComfyUI's own shipped BiRefNet blueprint, node for node.

`SaveImage` writes 4-channel tensors straight through `Image.fromarray`, so the
result is a real RGBA PNG.

Note the polarity contrast with workflow 03: **same mask, opposite handling.**
`ImageCompositeMasked` wants it as-is; `JoinImageWithAlpha` wants it inverted.

## 06 / 07 / 08 — marketplace, social, thumbnail

Same graph as 01 at different dimensions, with prompts pre-tuned for negative space.

| | Ratio | Size | Why |
|---|---|---|---|
| `06-marketplace-1x1` | 1:1 | 1024×1024 | Amazon/eBay/Shopify square |
| `07-social-4x5` | 4:5 | 896×1120 | Instagram/Facebook feed max height |
| `08-youtube-16x9` | 16:9 | 1344×768 | YouTube thumbnail |

All three are ~1 megapixel and every dimension is a multiple of 16 — FLUX
degrades on non-multiple-of-16 sizes.

### Other safe sizes

| Ratio | Size |
|---|---|
| 1:1 | 1024×1024 |
| 4:5 | 896×1120 |
| 3:4 | 896×1184 |
| 16:9 | 1344×768 |
| 9:16 | 768×1344 |
| 3:2 | 1216×832 |

Going much past ~1 MP costs VRAM steeply and FLUX starts duplicating subjects.
Generate at ~1 MP, then use workflow 04 to upscale.

## Editing

Change the prompt in node `6`, the size in node `5`, the seed in node `3`:

```bash
python3 - <<'PY'
import json
p="workflows/06-marketplace-1x1.json"
w=json.load(open(p))
w["6"]["inputs"]["text"]="matte black ceramic mug on white seamless, soft studio light"
w["5"]["inputs"]["width"]=1024; w["5"]["inputs"]["height"]=1024
json.dump(w,open(p,"w"),indent=2)
PY
python3 scripts/validate-workflows.py     # always re-validate after editing
```

Or just ask Claude — the MCP can edit and run graphs directly
([05-MCP.md](05-MCP.md)).

## Loading in the ComfyUI web UI

These are **API format**. In the ComfyUI web UI use **Workflow → Open** and pick
the file; recent frontends import API-format graphs and lay them out
automatically. If your build refuses, run them through the MCP or `/prompt`
instead — that is the format's native home, and how Claude drives them.

## Validator

`scripts/validate-workflows.py` checks that every `class_type` exists, every
required input is present, no unknown inputs are passed, every link points at a
real node and slot, and linked types match. Then it POSTs to `/prompt` and treats
"model file not downloaded yet" as PENDING rather than failure.

It was negative-tested against six deliberately broken graphs — bad node type,
missing required input, unknown input, type mismatch, dangling link, bad output
slot — and correctly rejected all six.
