<#
.SYNOPSIS
    Windows installer for ComfyUI + FLUX.1 Schnell + comfyui-mcp.
.DESCRIPTION
    Runs Check-Hardware.ps1 first and refuses to continue if it reports blockers,
    so no large download starts on unsuitable hardware.

    Steps: clone ComfyUI -> venv -> PyTorch -> custom nodes -> models -> MCP.
.PARAMETER Step
    Run a single step instead of all of them:
    check | comfyui | pytorch | nodes | models | mcp | all  (default: all)
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\Install-Studio.ps1
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\Install-Studio.ps1 -Step models
#>
[CmdletBinding()]
param(
    [ValidateSet('check','comfyui','pytorch','nodes','models','mcp','all')]
    [string]$Step = 'all',
    [string]$ComfyHome = "$env:USERPROFILE\ComfyUI",
    [string]$StateDir  = "$env:USERPROFILE\.comfyui-studio",
    [switch]$AssumeYes
)

$ErrorActionPreference = 'Stop'

function Write-Info { param($m) Write-Host "==> $m" -ForegroundColor Blue }
function Write-Ok   { param($m) Write-Host "  ok $m" -ForegroundColor Green }
function Write-Warn { param($m) Write-Host "warn $m" -ForegroundColor Yellow }
function Write-Fail { param($m) Write-Host "fail $m" -ForegroundColor Red }
function Write-Head { param($m) Write-Host "`n$m" -ForegroundColor White }
function Die { param($m) Write-Fail $m; exit 1 }

function Confirm-Action {
    param([string]$Prompt)
    if ($AssumeYes) { Write-Info "$Prompt -> yes (-AssumeYes)"; return $true }
    $r = Read-Host "$Prompt [y/N]"
    return ($r -match '^(y|yes)$')
}

$StudioDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)   # ...\comfyui-studio
$VenvDir   = Join-Path $ComfyHome '.venv'
$VenvPy    = Join-Path $VenvDir 'Scripts\python.exe'
$HwJson    = Join-Path $StateDir 'hardware.json'

function Get-Hw {
    if (-not (Test-Path $HwJson)) { Die "no hardware report - run .\Check-Hardware.ps1 first" }
    Get-Content $HwJson -Raw | ConvertFrom-Json
}

# ---------------------------------------------------------------- steps
function Step-Check {
    & (Join-Path $PSScriptRoot 'Check-Hardware.ps1') -ComfyHome $ComfyHome -StateDir $StateDir
    if ($LASTEXITCODE -ne 0) { Die "hardware check reported blockers - nothing installed" }
}

function Step-Comfyui {
    $hw = Get-Hw
    Write-Head "Step 1/5 - install ComfyUI into $ComfyHome"

    if (Test-Path (Join-Path $ComfyHome '.git')) {
        Write-Info "existing checkout found"
        if (Confirm-Action "Run 'git pull' to update it?") {
            git -C $ComfyHome pull --ff-only
        }
    } elseif (Test-Path $ComfyHome) {
        Die "$ComfyHome exists but is not a git checkout. Move it aside or pass -ComfyHome <other path>."
    } else {
        Write-Info "cloning Comfy-Org/ComfyUI"
        git clone --depth 1 https://github.com/Comfy-Org/ComfyUI.git $ComfyHome
        if ($LASTEXITCODE -ne 0) { Die "git clone failed" }
    }
    Write-Ok "ComfyUI at $ComfyHome"

    if (Test-Path $VenvPy) {
        Write-Ok "virtualenv already present"
    } else {
        Write-Info "creating isolated virtualenv"
        & $hw.pyBin -m venv $VenvDir
        if (-not (Test-Path $VenvPy)) { Die "venv creation failed" }
        Write-Ok "virtualenv created at $VenvDir"
    }
    & $VenvPy -m pip install --quiet --upgrade pip setuptools wheel

    foreach ($d in 'diffusion_models','text_encoders','vae','upscale_models','background_removal','loras','unet') {
        New-Item -ItemType Directory -Force -Path (Join-Path $ComfyHome "models\$d") | Out-Null
    }
    Write-Ok "model directories ready"
}

function Step-Pytorch {
    $hw = Get-Hw
    Write-Head "Step 2/5 - PyTorch for $($hw.gpuVendor) ($($hw.vramGb) GB VRAM)"
    if (-not (Test-Path $VenvPy)) { Die "no virtualenv - run -Step comfyui first" }

    $index = $null
    if ($hw.gpuVendor -eq 'nvidia') {
        $cu = $hw.cudaVer
        $maj = 0; $min = 0
        if ($cu -match '^(\d+)\.(\d+)') { $maj = [int]$Matches[1]; $min = [int]$Matches[2] }
        if     ($maj -ge 13)              { $index = 'https://download.pytorch.org/whl/cu130' }
        elseif ($maj -eq 12 -and $min -ge 8) { $index = 'https://download.pytorch.org/whl/cu128' }
        elseif ($maj -eq 12)              { $index = 'https://download.pytorch.org/whl/cu124' }
        else {
            Write-Warn "CUDA runtime reported as '$cu' - falling back to cu124."
            $index = 'https://download.pytorch.org/whl/cu124'
        }
        Write-Info "NVIDIA detected -> $index"
    } else {
        # No ROCm wheels on Windows; AMD and no-GPU both land on CPU.
        $index = 'https://download.pytorch.org/whl/cpu'
        Write-Warn "No CUDA GPU usable on Windows -> CPU-only PyTorch (slow)."
    }

    Write-Info "installing torch / torchvision / torchaudio (large download)"
    & $VenvPy -m pip install --upgrade torch torchvision torchaudio --index-url $index
    if ($LASTEXITCODE -ne 0) { Die "PyTorch install failed" }

    Write-Info "installing ComfyUI requirements"
    & $VenvPy -m pip install -r (Join-Path $ComfyHome 'requirements.txt')

    & $VenvPy -c @"
import torch
print('  torch         ', torch.__version__)
if torch.cuda.is_available():
    print('  CUDA device   ', torch.cuda.get_device_name(0))
    print('  VRAM          ', round(torch.cuda.get_device_properties(0).total_memory/1024**3,1), 'GB')
else:
    print('  accelerator    NONE - running on CPU')
"@
}

function Step-Nodes {
    $hw = Get-Hw
    Write-Head "Step 3/5 - custom nodes"
    $nodeDir = Join-Path $ComfyHome 'custom_nodes'
    New-Item -ItemType Directory -Force -Path $nodeDir | Out-Null

    function Install-Node {
        param($Name, $Url, $Why)
        $dest = Join-Path $nodeDir $Name
        if (Test-Path (Join-Path $dest '.git')) { Write-Ok "$Name already installed"; return }
        Write-Info "installing $Name ($Why)"
        git clone --depth 1 $Url $dest
        $req = Join-Path $dest 'requirements.txt'
        if (Test-Path $req) { & $VenvPy -m pip install --quiet -r $req }
    }

    Install-Node 'ComfyUI-Manager' 'https://github.com/Comfy-Org/ComfyUI-Manager.git' 'official node manager'
    if ($hw.profile -eq 'gguf') {
        Install-Node 'ComfyUI-GGUF' 'https://github.com/city96/ComfyUI-GGUF.git' 'quantised loaders for low VRAM'
        & $VenvPy -m pip install --quiet gguf
    } else {
        Write-Info "profile '$($hw.profile)' does not need ComfyUI-GGUF - skipping"
    }
}

function Step-Models {
    $hw  = Get-Hw
    $cfg = Get-Content (Join-Path $StudioDir 'config\model-profiles.json') -Raw | ConvertFrom-Json
    $p   = $cfg.profiles.$($hw.profile)

    Write-Head "Step 4/5 - models for profile '$($hw.profile)'"

    $models = @($cfg.common_models)
    if ($p.inherits_models_from) { $models += $cfg.profiles.$($p.inherits_models_from).models }
    else                         { $models += $p.models }

    $total = ($models | Measure-Object -Property size_gb -Sum).Sum
    $models | ForEach-Object {
        '{0,-44} models\{1,-22} {2,6} GB' -f $_.name, $_.dir, $_.size_gb | Write-Host
    }
    Write-Host ("`n  total download: {0:N1} GB" -f $total)

    # ---- Phase 1: preflight. Verify every URL BEFORE transferring anything.
    Write-Head "Phase 1 - preflight (no data transferred)"
    $driveLetter = (Split-Path -Qualifier $ComfyHome).TrimEnd(':')
    $freeGb = [math]::Floor((Get-PSDrive -Name $driveLetter).Free / 1GB)
    Write-Info "free disk: $freeGb GB (need ~$([math]::Ceiling($total) + 5) GB)"
    if ($freeGb -lt ($total + 5)) { Die "not enough free disk - nothing was downloaded" }

    $bad = 0
    $plan = @()
    foreach ($m in $models) {
        $dest = Join-Path $ComfyHome "models\$($m.dir)\$($m.name)"
        if (Test-Path $dest) { Write-Ok "already present, skipping: $($m.name)"; continue }
        $useUrl = $null
        foreach ($cand in @($m.url, $m.mirror) | Where-Object { $_ }) {
            try {
                $r = Invoke-WebRequest -Uri $cand -Method Head -MaximumRedirection 5 `
                                       -UseBasicParsing -TimeoutSec 45
                if ($r.StatusCode -eq 200) { $useUrl = $cand; break }
            } catch { }
        }
        if ($useUrl) {
            Write-Ok "reachable: $($m.name)"
            $plan += [pscustomobject]@{ Name=$m.name; Dir=$m.dir; Url=$useUrl; SizeGb=$m.size_gb }
        } else {
            Write-Fail "$($m.name) unreachable - $($m.url)"; $bad++
        }
    }
    if ($bad -gt 0) {
        Write-Fail "$bad file(s) could not be verified. NOTHING has been downloaded."
        Write-Fail "Fix the URLs in $StudioDir\config\model-profiles.json and re-run."
        exit 1
    }
    if ($plan.Count -eq 0) { Write-Ok "all models already present"; return }
    if (-not (Confirm-Action ("Download {0:N1} GB of model weights now?" -f $total))) {
        Write-Info "aborted - nothing downloaded"; return
    }

    # ---- Phase 2: download. BITS gives resumable transfers + progress.
    Write-Head "Phase 2 - downloading"
    foreach ($m in $plan) {
        $dest = Join-Path $ComfyHome "models\$($m.Dir)\$($m.Name)"
        New-Item -ItemType Directory -Force -Path (Split-Path $dest) | Out-Null
        Write-Info "downloading $($m.Name) ($($m.SizeGb) GB)"
        $part = "$dest.part"
        try {
            Start-BitsTransfer -Source $m.Url -Destination $part -Description $m.Name -ErrorAction Stop
        } catch {
            Write-Warn "BITS failed ($_), falling back to Invoke-WebRequest"
            Invoke-WebRequest -Uri $m.Url -OutFile $part -UseBasicParsing
        }
        Move-Item -Force $part $dest
        Write-Ok $m.Name
    }

    Write-Info "aligning workflows with profile '$($hw.profile)'"
    & $VenvPy (Join-Path $StudioDir 'scripts\apply-profile.py') --profile $hw.profile | Out-Null
    Write-Ok "workflows updated"
}

function Step-Mcp {
    $hw = Get-Hw
    Write-Head "Step 5/5 - comfyui-mcp for Claude Code"
    if ([int]($hw.nodeVer -split '\.')[0] -lt 22) { Die "comfyui-mcp needs Node >= 22 (found $($hw.nodeVer))" }

    Write-Info "warming the npx cache for comfyui-mcp"
    & npm exec --yes comfyui-mcp -- --version 2>$null | Out-Null

    $settings = Join-Path $env:USERPROFILE '.claude\settings.json'
    $claude = Get-Command claude -ErrorAction SilentlyContinue
    $registered = $false

    if ($claude) {
        $list = (& claude mcp list 2>$null | Out-String)
        if ($list -match '(?m)^comfyui\b') {
            Write-Ok "MCP server 'comfyui' already registered"; $registered = $true
        } else {
            & claude mcp add --scope user comfyui -- npx -y comfyui-mcp
            if ($LASTEXITCODE -eq 0) { Write-Ok "registered MCP server 'comfyui'"; $registered = $true }
            else { Write-Warn "'claude mcp add' failed - falling back to settings.json" }
        }
    }

    if (-not $registered) {
        New-Item -ItemType Directory -Force -Path (Split-Path $settings) | Out-Null
        $data = @{}
        if (Test-Path $settings) {
            # This is a real user config file - back it up and merge, never overwrite.
            Copy-Item $settings "$settings.bak.$(Get-Date -Format yyyyMMdd-HHmmss)"
            Write-Ok "backed up existing settings.json"
            try { $data = Get-Content $settings -Raw | ConvertFrom-Json -AsHashtable }
            catch { Die "settings.json is not valid JSON - refusing to touch it: $settings" }
        }
        if (-not $data.ContainsKey('mcpServers')) { $data['mcpServers'] = @{} }
        if ($data['mcpServers'].ContainsKey('comfyui')) {
            Write-Ok "'comfyui' entry already present - left unchanged"
        } else {
            $data['mcpServers']['comfyui'] = @{ command = 'npx'; args = @('-y','comfyui-mcp') }
            $data | ConvertTo-Json -Depth 10 | Set-Content -Encoding UTF8 $settings
            Write-Ok "added mcpServers.comfyui to $settings"
        }
    }
    Write-Warn "Restart Claude Code (or run /mcp) so it picks up the new server."
}

# ---------------------------------------------------------------- dispatch
switch ($Step) {
    'check'   { Step-Check }
    'comfyui' { Step-Comfyui }
    'pytorch' { Step-Pytorch }
    'nodes'   { Step-Nodes }
    'models'  { Step-Models }
    'mcp'     { Step-Mcp }
    'all'     {
        Step-Check; Step-Comfyui; Step-Pytorch; Step-Nodes; Step-Models; Step-Mcp
        Write-Head "Install complete"
        Write-Ok "start everything with: .\Start-Studio.ps1"
    }
}
