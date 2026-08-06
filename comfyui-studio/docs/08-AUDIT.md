# 08 — Self-audit findings

A full independent re-check of this pack after it was first written. Seven real
defects were found and fixed. Recording them here because several are the kind
that would have failed silently or halfway through a 30 GB download.

## Defects found and fixed

### 1. FLUX.1-schnell is a gated repo — docs said it wasn't (**high**)

`docs/03-MODELS.md` claimed:

> It is also *ungated* — no HuggingFace token, no licence click-through.

**Wrong.** The HuggingFace Hub API reports `black-forest-labs/FLUX.1-schnell` as
`🔒 Gated`. Its files return 401/403 without a token whose account has accepted
the licence. A user following the old docs would have watched the preflight fail
on the two largest files with no idea why.

**Fixed:** documented the gating; the preflight now recognises 401/403
specifically, falls back to the ungated `Comfy-Org/flux1-schnell` mirror, and
prints how to use a token if you'd rather pull from the official BFL source. The
mirrors were confirmed **byte-identical**:

| File | BFL (gated) | Comfy-Org (ungated) |
|---|---|---|
| `flux1-schnell.safetensors` | 23,782,506,688 | 23,782,506,688 |
| `ae.safetensors` | 335,304,388 | 335,304,388 |

### 2. `Start-Studio.ps1` had a syntax error — the script could not run at all (**high**)

```powershell
Write-Fail "ComfyUI did not come up in time - last lines of $log:"
```

PowerShell parses `$log:` as a *scope-qualified* variable reference and fails at
parse time, so the entire script was unrunnable — not just that line. Found by
installing pwsh 7.6.4 and running the AST parser over all three scripts.

**Fixed:** `${log}:`. All three scripts now parse clean.

### 3. `$args` is a reserved automatic variable (**medium**)

`Start-Studio.ps1` assigned to `$args`, which PowerShell owns. **Fixed:** renamed
to `$comfyArgs`, and the audit now scans the AST for assignments to any
automatic variable.

### 4. `sed \t` in the mirror rewrite breaks on macOS (**medium**)

The preflight rewrote the manifest in place with

```bash
sed -i.bak "s|^$name\t$dir\t[^\t]*|...|"
```

`\t` is a GNU extension; BSD/macOS `sed` treats it as a literal `t`, so the
mirror fallback would silently not apply — and the loop was editing the same
file it was reading.

**Fixed:** removed `sed` entirely. Phase 1 now writes a separate *resolved*
manifest naming the URL that actually answered, and phase 2 reads that.

### 5. MCP tool count was wrong, and the shape was wrong (**medium**)

Docs said "~86 tools" and told you to expect ~86. Measured by speaking MCP over
stdio to `comfyui-mcp` 0.49.8:

- the catalogue is **151 tools**, not 86
- the server presents a **3-tool router** (`call_tool`, `describe_tool`,
  `list_tools`), so Claude sees **3**

A user following the old docs would see 3 tools and reasonably conclude the
install was broken.

**Fixed:** documented the router explicitly, with "three tools is correct, not
broken" and how to reach the catalogue.

### 6. MCP config path was wrong (**medium**)

Docs said registration lands in `~/.claude/settings.json`. Running it showed
`claude mcp add --scope user` writes to **`~/.claude.json`**. `settings.json` is
only used by the fallback path.

**Fixed:** corrected docs and file map; `verify.sh` now checks both.

### 7. Model sizes were off (**low**)

Real byte counts from the Hub API:

| File | Was | Actual |
|---|---|---|
| `birefnet.safetensors` | 0.9 GB | **0.44 GB** (0.9 GB is `lucida.safetensors`, a different file) |
| `t5-v1_1-xxl-encoder-Q5_K_M.gguf` | 3.9 GB | **3.39 GB** |

**Fixed:** every entry now carries a verified `size_bytes`, and profile totals
were recomputed (`high` 34.67, `balanced`/`low`/`cpu` 29.77, `gguf` 11.27 GB) and
propagated into the hardware-check disk gate and all docs.

### 8. Running step 3 before step 1 died with a confusing `df` error (**low**)

`03-download-models.sh` assumed `$COMFY_HOME` existed and went straight to
`df "$COMFY_HOME"`, which printed `df: ...: No such file or directory` and
exited — not obviously "you skipped step 1".

**Fixed:** explicit guard, plus `CFG` is now overridable so the download logic
can be exercised against a test manifest.

## Earlier defects (found during initial build)

| # | Defect | Impact |
|---|---|---|
| 8 | `STUDIO_DIR` resolved one level too shallow | `verify.sh` reported a **false "all models present"** |
| 9 | `set -e` aborted `verify.sh` on its first failed check | health check stopped instead of reporting everything |
| 10 | `curl … \|\| echo 000` appended to `tail` output | HTTP codes printed as `000000` |

## What the audit confirmed as correct

- All 8 workflows: **8/8** structural + live `/prompt` validation, on both the
  safetensors and GGUF profiles
- Validator negative test: **6/6** broken graphs correctly rejected
- Mask polarity in workflows 03 and 05 (opposite, and both right)
- Every model URL, byte count and licence — **9/9** confirmed via the Hub API
- `01`, `04`, `05` install steps run end-to-end against a clean prefix
- MCP → ComfyUI round trip returning live server stats
- **Mirror fallback proven end-to-end**: with a deliberately 404ing primary the
  preflight logged `primary returned 404 - using the mirror` and phase 2
  downloaded 67,040,989 bytes — exactly the verified byte count. This path is
  load-bearing, because it is what handles the gated FLUX repo.

## How to re-run this audit

```bash
./scripts/verify.sh                                  # full health check
python3 scripts/validate-workflows.py                # graphs vs live server
pwsh -NoProfile -Command '                           # PowerShell parse check
  Get-ChildItem scripts/windows/*.ps1 | ForEach-Object {
    $e=$null; [System.Management.Automation.Language.Parser]::ParseFile(
      $_.FullName,[ref]$null,[ref]$e) | Out-Null
    if ($e.Count) { "FAIL $($_.Name)"; $e } else { "ok $($_.Name)" } }'
```
