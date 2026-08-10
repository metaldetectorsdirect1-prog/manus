# 02 — Install

## One command

```bash
./scripts/install.sh                # interactive
ASSUME_YES=1 ./scripts/install.sh   # unattended
```

It runs, and stops at the first failure:

```
00-check-hardware.sh   gate — nothing proceeds if this reports blockers
01-install-comfyui.sh  git clone + isolated venv
02-install-pytorch.sh  the right torch build for the detected GPU
04-install-custom-nodes.sh   (before models: the gguf profile needs the node)
03-download-models.sh  preflight, confirm, then fetch
05-install-mcp.sh      register 'comfyui' with Claude Code
```

## Environment overrides

| Variable | Default | Meaning |
|---|---|---|
| `COMFY_HOME` | `~/ComfyUI` | where ComfyUI is installed |
| `VENV_DIR` | `$COMFY_HOME/.venv` | virtualenv location |
| `COMFY_PORT` | `8188` | API/UI port |
| `COMFY_HOST` | `127.0.0.1` | bind address (see warning below) |
| `STATE_DIR` | `~/.comfyui-studio` | hardware report, logs, pid |
| `ASSUME_YES` | `0` | answer yes to all prompts |
| `PROFILE_OVERRIDE` | — | force a profile in step 03 |
| `FORCE_GGUF` | `0` | install ComfyUI-GGUF regardless of profile |
| `HUGGINGFACE_TOKEN` | — | only needed for gated repos (Schnell is **not** gated) |
| `EXTRA_COMFY_ARGS` | — | extra flags for `start-comfyui.sh` |

```bash
COMFY_HOME=/mnt/big/ComfyUI ./scripts/install.sh
```

> **Binding.** `COMFY_HOST` defaults to `127.0.0.1` — local only. ComfyUI has no
> authentication. Setting `COMFY_HOST=0.0.0.0` exposes an unauthenticated service
> that can read and write files and execute custom-node code, to everyone who can
> reach the port. Only do that on a trusted network, behind a firewall.

## Step by step

### 0 — hardware
```bash
./scripts/00-check-hardware.sh
```
Writes `~/.comfyui-studio/hardware.env`. Exits non-zero on blockers.
See [01-HARDWARE.md](01-HARDWARE.md).

### 1 — ComfyUI + isolated venv
```bash
./scripts/01-install-comfyui.sh
```
Shallow-clones `Comfy-Org/ComfyUI` to `$COMFY_HOME` and creates `$COMFY_HOME/.venv`.
If `$COMFY_HOME` exists and is a git checkout it offers to `git pull`; if it
exists and is *not* a checkout it **stops** rather than risk your files.

### 2 — PyTorch
```bash
./scripts/02-install-pytorch.sh
```
Picks the index automatically:

| Detected | Index |
|---|---|
| NVIDIA, CUDA ≥ 13 | `download.pytorch.org/whl/cu130` |
| NVIDIA, CUDA ≥ 12.8 | `.../cu128` |
| NVIDIA, CUDA 12.x | `.../cu124` |
| AMD (Linux) | `.../rocm6.2` |
| Apple Silicon | default PyPI (MPS) |
| No GPU | `.../cpu` |

Then installs ComfyUI's `requirements.txt` and prints the detected accelerator.
If a GPU exists but torch reports CPU, it says so loudly — that's almost always
a driver older than the wheel line.

### 3 — custom nodes
```bash
./scripts/04-install-custom-nodes.sh
```
Installs only:

- **ComfyUI-Manager** (Comfy-Org) — the official node/model manager
- **ComfyUI-GGUF** (city96) — quantised loaders, **only** on the `gguf` profile

None of the eight bundled workflows needs either one. Every extra custom node is
code that runs in your Python process and one more thing to break on upgrade, so
this list is deliberately short.

### 4 — models
```bash
./scripts/03-download-models.sh
```
Two phases:

1. **Preflight** — prints every file with size and licence, checks free disk,
   then HEAD-checks every URL (falling back to a mirror where one is configured).
   If anything is unreachable it **aborts having downloaded nothing** and tells
   you which URL to fix.
2. **Download** — only after preflight is clean and you confirm. Uses
   `curl -C -` so an interrupted run resumes, and writes to `.part` first so a
   killed download never leaves a truncated file that looks complete.

Finally it runs `apply-profile.py` so the workflows point at what was installed.

### 5 — MCP
```bash
./scripts/05-install-mcp.sh
```
Prefers `claude mcp add --scope user comfyui -- npx -y comfyui-mcp`. If the CLI
isn't available it merges into `~/.claude/settings.json` — after taking a
timestamped backup, and refusing outright if that file isn't valid JSON.
See [05-MCP.md](05-MCP.md).

## Windows

> **Do not paste the bash commands into PowerShell.** `&&` is not a statement
> separator in Windows PowerShell 5.1, and `.sh` files are not executable there.
> You will get `The token '&&' is not a valid statement separator in this version.`
> Run one command per line, and use the `.ps1` scripts below.

```powershell
cd $HOME\comfyui-studio\scripts\windows
powershell -ExecutionPolicy Bypass -File .\Check-Hardware.ps1
powershell -ExecutionPolicy Bypass -File .\Install-Studio.ps1
powershell -ExecutionPolicy Bypass -File .\Start-Studio.ps1
```

`Install-Studio.ps1` takes `-Step check|comfyui|pytorch|nodes|models|mcp|all`,
plus `-ComfyHome`, `-AssumeYes`. Downloads use BITS (resumable) with an
`Invoke-WebRequest` fallback.

### Windows PowerShell 5.1

5.1 (the blue `powershell.exe` that ships with Windows) is supported. Two things
it needs that PowerShell 7 does not, both handled automatically:

- **TLS 1.2.** 5.1 negotiates TLS 1.0 by default, which GitHub and HuggingFace
  both refuse — every download would fail with *"Could not create SSL/TLS secure
  channel."* Each script now forces TLS 1.2 when running under 5.1.
- **JSON merging.** `ConvertFrom-Json -AsHashtable` is PowerShell 6+ only, so the
  `~/.claude/settings.json` merge is done through the venv's Python instead —
  the same merge the bash installer performs.

PowerShell 7 (`pwsh`) also works and is a nicer shell (it supports `&&`), but is
not required: <https://aka.ms/powershell>

Check which you're on:

```powershell
$PSVersionTable.PSVersion
```

> **Testing status.** These scripts are AST-parse-clean on PowerShell 7.6.4 and
> were audited for 5.1-incompatible constructs, but **were never executed on a
> Windows host** — no Windows machine was available. They are the least-tested
> part of this pack. If you want the path that was actually run end-to-end, use
> WSL2 + the bash scripts.

## Launch and check

```bash
./scripts/start-studio.sh    # ComfyUI in background + MCP status
./scripts/verify.sh          # full health check
./scripts/stop-comfyui.sh
```

## Uninstall

Everything lives in three places:

```bash
rm -rf ~/ComfyUI            # engine, venv, models, outputs  (check outputs first!)
rm -rf ~/.comfyui-studio    # hardware report, logs, pid
# and remove the "comfyui" entry from ~/.claude/settings.json
claude mcp remove comfyui   # if you registered via the CLI
```

Nothing is installed system-wide. No services, no PATH edits, no registry keys.
