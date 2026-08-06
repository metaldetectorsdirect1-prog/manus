# 06 — Troubleshooting

Start with:

```bash
./scripts/verify.sh
```

It checks the venv, PyTorch and accelerator, the ComfyUI API, every model file
for the active profile, custom nodes, all eight workflows, and MCP registration.

---

## PyTorch can't see the GPU

`verify.sh` says `accelerator - cpu` but you have a GPU.

```bash
~/ComfyUI/.venv/bin/python -c "import torch;print(torch.__version__, torch.cuda.is_available())"
nvidia-smi
```

- `torch` ends in `+cpu` → the CPU wheel got installed. Re-run
  `./scripts/02-install-pytorch.sh` after confirming `nvidia-smi` works.
- `torch` is a CUDA build but `is_available()` is `False` → **driver older than
  the wheel line**. Either update the NVIDIA driver, or force an older line:
  ```bash
  ~/ComfyUI/.venv/bin/python -m pip install --force-reinstall \
      torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
  ```
- `nvidia-smi` missing entirely → no driver. Install it first; nothing else will help.
- AMD on Windows → expected. There is no ROCm PyTorch for Windows. Use WSL2 with
  the bash scripts.

---

## Out of memory

### CUDA out of memory

Move down a profile:

```bash
PROFILE_OVERRIDE=gguf ./scripts/03-download-models.sh
python3 scripts/apply-profile.py --profile gguf
```

Or just add the flag without changing weights:

```bash
EXTRA_COMFY_ARGS="--lowvram" ./scripts/start-comfyui.sh
```

Escalating: `--normalvram` → `--lowvram` → `--novram` → `--cpu`.

Other levers, in order of effect:

1. Reduce size — 1024×1024 is ~1 MP. 1344×768 is comparable. Going to 1536² is
   2.25× the pixels and much more than 2.25× the VRAM.
2. `batch_size: 1` in node `5`.
3. Close other GPU users (browsers with hardware acceleration are common culprits).
4. Use the `gguf` profile — Q4_K_S is ~6.8 GB on disk and correspondingly lighter.

### Killed / OOM while loading (system RAM, not VRAM)

FLUX needs roughly **16 GB of system RAM** to load, separate from VRAM. On 8–16 GB
machines the process gets killed during load. Add swap, close applications, or
use the `gguf` profile — it loads a much smaller file.

---

## Generation is extremely slow

Seconds is normal on a decent GPU. Minutes means CPU.

```bash
grep PROFILE ~/.comfyui-studio/hardware.env
```

If it says `cpu` and you have a GPU, see the PyTorch section above. If you have
no GPU, that is simply the cost — FLUX on CPU is minutes per image, and there is
no configuration that changes that.

---

## Output looks burnt, oversaturated, or melted

Almost always CFG or steps.

```bash
python3 -c "
import json;w=json.load(open('workflows/01-txt2img.json'))
print(w['3']['inputs'])"
```

Must be `cfg: 1.0`, `steps: 4`. Schnell is guidance-distilled — raising CFG
degrades it. See [04-WORKFLOWS.md](04-WORKFLOWS.md).

If it's noise rather than burn, check node `5` is `EmptySD3LatentImage`, not
`EmptyLatentImage`.

---

## Transparent PNG is inverted

Background opaque, product see-through → the `InvertMask` between
`RemoveBackground` and `JoinImageWithAlpha` is missing or bypassed.
`JoinImageWithAlpha` computes `alpha = 1.0 - mask`. Re-run:

```bash
python3 scripts/validate-workflows.py
git checkout workflows/05-transparent-product.json    # restore the shipped graph
```

Note the opposite rule in workflow 03: `ImageCompositeMasked` uses the mask
**uninverted**. Don't "fix" one by copying the other.

## Halo of old background around the cutout

Increase the shrink in node `32` (`GrowMask.expand`, default `-2`) to `-4`, and
raise `FeatherMask` to `3`–`4`. Very fine detail (hair, mesh, glass) is where
BiRefNet struggles most.

---

## Workflow fails to run

```bash
python3 scripts/validate-workflows.py
```

- `value_not_in_list` for a model filename → the file isn't downloaded, or the
  active profile doesn't match the workflows. Fix with
  `python3 scripts/apply-profile.py --profile <yours>`.
- `unknown node type 'UnetLoaderGGUF'` → the GGUF profile is applied but
  ComfyUI-GGUF isn't installed: `FORCE_GGUF=1 ./scripts/04-install-custom-nodes.sh`,
  then restart ComfyUI.
- Anything else → the validator names the node and input.

---

## ComfyUI won't start

```bash
tail -50 ~/.comfyui-studio/comfyui.log
```

- **Port in use** → `COMFY_PORT=8189 ./scripts/start-comfyui.sh`
- **A custom node fails to import** → move it out of
  `~/ComfyUI/custom_nodes/` and restart. Custom nodes are the most common cause
  of a ComfyUI that won't boot after an update.
- **Import errors after a `git pull`** →
  `~/ComfyUI/.venv/bin/python -m pip install -r ~/ComfyUI/requirements.txt`

---

## MCP problems

| Symptom | Cause / fix |
|---|---|
| Claude has no ComfyUI tools | Claude Code not restarted — run `/mcp` |
| "ComfyUI not detected on ports 8188, 8000" | not running — `./scripts/start-studio.sh` |
| MCP server won't start | `node --version` must be ≥ 22 |
| `CLOUD_UNSUPPORTED` | `COMFYUI_API_KEY` set — unset it for local use |
| Empty model lists | run `health_check` via the MCP; check `verify.sh` |

Check registration:

```bash
claude mcp list
grep -A3 '"comfyui"' ~/.claude/settings.json
```

---

## Model download problems

The preflight refuses to start when a URL is unreachable, and names it. Fix the
entry in `config/model-profiles.json` — see
[03-MODELS.md](03-MODELS.md#if-a-url-has-moved) — and re-run. Files already on
disk are skipped, so re-running is cheap.

An interrupted download resumes (`curl -C -`) and partial files are kept as
`.part`, so a killed transfer never leaves a truncated file that looks complete.
If you suspect a corrupt file, delete it and re-run step 3.

---

## Starting clean

```bash
./scripts/stop-comfyui.sh
rm -rf ~/ComfyUI/.venv                 # keeps models and outputs
./scripts/01-install-comfyui.sh && ./scripts/02-install-pytorch.sh
```

Full reset (**deletes weights and generated images** — copy `~/ComfyUI/output`
first if you want to keep them):

```bash
rm -rf ~/ComfyUI ~/.comfyui-studio
./scripts/install.sh
```
