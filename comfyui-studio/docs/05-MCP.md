# 05 — Claude Code ↔ ComfyUI (MCP)

[`artokun/comfyui-mcp`](https://github.com/artokun/comfyui-mcp) is an MCP server
that lets Claude Code drive your local ComfyUI: generate images, run and author
workflows, manage models and custom nodes, and view results.

| | |
|---|---|
| npm package | `comfyui-mcp` |
| Version confirmed | **0.49.8** |
| Licence | MIT |
| Requires | **Node.js ≥ 22** |
| Tools in catalogue | **151** (measured) |
| Tools Claude sees | **3** — see "Why only 3 tools" below |
| Install | none — runs via `npx` |

## Install

```bash
./scripts/05-install-mcp.sh
```

Prefers the official CLI:

```bash
claude mcp add --scope user comfyui -- npx -y comfyui-mcp
```

Falls back to merging into `~/.claude/settings.json` — after a timestamped
backup, and refusing outright if that file isn't valid JSON.

> **Where the config actually lands.** `claude mcp add --scope user` writes to
> **`~/.claude.json`**, not `~/.claude/settings.json`. Only the fallback path
> uses `settings.json`. Both work; `claude mcp list` is the reliable way to
> check, and that is what `verify.sh` uses.

## Configuration

Local ComfyUI (the normal case — the server auto-detects the install path and
probes port 8188 then 8000):

```json
{
  "mcpServers": {
    "comfyui": {
      "command": "npx",
      "args": ["-y", "comfyui-mcp"]
    }
  }
}
```

ComfyUI on another machine:

```json
{
  "mcpServers": {
    "comfyui": {
      "command": "npx",
      "args": ["-y", "comfyui-mcp", "--comfyui-url", "http://192.168.1.50:8188"]
    }
  }
}
```

A copy lives at [`../config/mcp.example.json`](../config/mcp.example.json).

### Useful environment variables

| Variable | Purpose |
|---|---|
| `COMFYUI_URL` | full URL, instead of `--comfyui-url` |
| `COMFYUI_HOST` / `COMFYUI_PORT` | override host/port separately |
| `COMFYUI_PATH` | explicit ComfyUI install path if auto-detection misses |
| `COMFYUI_DOWNLOAD_CACHE_DIR` | model download cache (default `~/.comfyui-mcp/cache`) |
| `HUGGINGFACE_TOKEN`, `CIVITAI_API_TOKEN` | gated downloads / rate limits |

> Do **not** set `COMFYUI_API_KEY` unless you deliberately want Comfy Cloud. It
> switches the server into cloud mode and local-only tools then fail with
> `CLOUD_UNSUPPORTED`. This pack is entirely local; leave it unset.

## Activate

1. Start ComfyUI: `./scripts/start-studio.sh`
2. **Restart Claude Code**, or run `/mcp` to reconnect
3. Check it connected: `claude mcp list` → `comfyui: npx -y comfyui-mcp - ✓ Connected`

## Why only 3 tools

`comfyui-mcp` runs a **tool router**. Ask Claude what ComfyUI tools it has and it
will report **three**, not 151:

```
call_tool      run a catalogue tool by name
describe_tool  get a tool's parameters
list_tools     enumerate the catalogue
```

That is by design — it keeps the tool surface small enough for weaker models,
and the full catalogue stays reachable through the router. I measured the
catalogue at **151 tools** in v0.49.8, across groups including `workflows` (10),
`workflow-authoring` (19), models, custom nodes, and queue control.

**Three tools is correct, not broken.** Ask for the real list instead:

> List all the ComfyUI tools available.

Claude calls `list_tools` and gets the catalogue. You do not need to name tools
yourself — just describe the outcome and Claude routes it.

## The test command

With ComfyUI running and weights installed:

> Generate a premium photorealistic e-commerce product advertisement, 1:1 aspect
> ratio, professional studio lighting, clean composition, realistic shadows and
> sufficient negative space for marketing text.

Claude will call the generation tool, ComfyUI renders (a few seconds on a decent
GPU, minutes on CPU), and an `asset_id` comes back.

**Claude can see the result** — it fetches the image back through the MCP's image
tool, so it can critique and refine:

> The shadow is too harsh and the product sits too low. Regenerate with softer
> diffused lighting and more headroom for a headline.

That loop — generate, look, adjust — is the point of wiring this up.

## Driving the bundled workflows

The eight graphs in `workflows/` are API-format, which is what the MCP submits:

> Run workflows/05-transparent-product.json on ~/photos/mug.png

> Use workflows/03-product-background-replace.json with my product photo and a
> warm marble surface background.

> Take the last image and run workflows/04-upscale.json on it.

Claude can also author new graphs — but for the eight covered here, the bundled
files are already validated, so prefer them.

## Prompting FLUX.1 Schnell

FLUX responds to natural descriptive sentences, not comma-separated tag soup.

Good:
> A matte black ceramic coffee mug on a white seamless studio backdrop, soft
> diffused key light from the upper left, gentle contact shadow, generous empty
> space on the right for headline text, shot on 85mm, shallow depth of field.

Less good:
> mug, black, studio, 8k, masterpiece, best quality, ultra detailed

Remember: **no negative prompt** at CFG 1.0. To remove something, describe the
scene without it rather than negating it.

## Troubleshooting

**"ComfyUI not detected on ports 8188, 8000"** — it isn't running.
`./scripts/start-studio.sh`.

**Only 3 tools showing** — expected. That's the router; see above.

**Tools missing after install** — Claude Code wasn't restarted. Run `/mcp`.

**`CLOUD_UNSUPPORTED`** — `COMFYUI_API_KEY` is set. Unset it for local use.

**Empty model lists** — run `health_check` via the MCP; usually an
`extra_model_paths.yaml` issue. Also check `./scripts/verify.sh`.

**Node version** — `node --version` must be ≥ 22. The MCP will not start below that.

More in [06-TROUBLESHOOTING.md](06-TROUBLESHOOTING.md).
