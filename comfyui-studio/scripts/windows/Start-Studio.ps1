<#
.SYNOPSIS
    One-click launcher (Windows): starts ComfyUI with the profile's VRAM flags
    and reports whether Claude Code's MCP bridge is wired up.
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\Start-Studio.ps1
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\Start-Studio.ps1 -Background
#>
[CmdletBinding()]
param(
    [string]$ComfyHome = "$env:USERPROFILE\ComfyUI",
    [string]$StateDir  = "$env:USERPROFILE\.comfyui-studio",
    [int]$Port = 8188,
    [switch]$Background
)

$ErrorActionPreference = 'Stop'

if ($PSVersionTable.PSVersion.Major -lt 6) {
    [Net.ServicePointManager]::SecurityProtocol =
        [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
}

function Write-Info { param($m) Write-Host "==> $m" -ForegroundColor Blue }
function Write-Ok   { param($m) Write-Host "  ok $m" -ForegroundColor Green }
function Write-Warn { param($m) Write-Host "warn $m" -ForegroundColor Yellow }
function Write-Fail { param($m) Write-Host "fail $m" -ForegroundColor Red }
function Write-Head { param($m) Write-Host "`n$m" -ForegroundColor White }

$VenvPy = Join-Path $ComfyHome '.venv\Scripts\python.exe'
$HwJson = Join-Path $StateDir 'hardware.json'
$Url    = "http://127.0.0.1:$Port"

if (-not (Test-Path $VenvPy)) { Write-Fail "no virtualenv at $ComfyHome\.venv - run Install-Studio.ps1 first"; exit 1 }
if (-not (Test-Path $HwJson)) { Write-Fail "no hardware report - run Check-Hardware.ps1 first"; exit 1 }
$hw = Get-Content $HwJson -Raw | ConvertFrom-Json

function Test-ComfyUp {
    try {
        $r = Invoke-WebRequest -Uri "$Url/system_stats" -UseBasicParsing -TimeoutSec 5
        return ($r.StatusCode -eq 200)
    } catch { return $false }
}

Write-Head "ComfyUI Studio"

if (Test-ComfyUp) {
    Write-Ok "ComfyUI is already running at $Url"
} else {
    $flags = @()
    if ($hw.launchFlags) { $flags = @($hw.launchFlags) }
    Write-Info "profile   $($hw.profile)"
    Write-Info "flags     $(if ($flags) { $flags -join ' ' } else { '<none>' })"
    Write-Info "url       $Url"

    # NOT $args - that is a reserved automatic variable in PowerShell.
    $comfyArgs = @('main.py','--port',"$Port",'--listen','127.0.0.1') + $flags
    New-Item -ItemType Directory -Force -Path $StateDir | Out-Null
    $log = Join-Path $StateDir 'comfyui.log'

    if ($Background) {
        $p = Start-Process -FilePath $VenvPy -ArgumentList $comfyArgs -WorkingDirectory $ComfyHome `
                           -RedirectStandardOutput $log -RedirectStandardError "$log.err" `
                           -WindowStyle Hidden -PassThru
        $p.Id | Set-Content (Join-Path $StateDir 'comfyui.pid')
        Write-Info "pid $($p.Id), logging to $log"

        $deadline = (Get-Date).AddSeconds(180)
        while ((Get-Date) -lt $deadline -and -not (Test-ComfyUp)) { Start-Sleep -Seconds 2 }
        if (Test-ComfyUp) { Write-Ok "ComfyUI API is up at $Url" }
        else {
            Write-Fail "ComfyUI did not come up in time - last lines of ${log}:"
            Get-Content $log -Tail 20 -ErrorAction SilentlyContinue
            exit 1
        }
    } else {
        Push-Location $ComfyHome
        try { & $VenvPy @comfyArgs } finally { Pop-Location }
        return
    }
}

# ---------------------------------------------------------------- MCP status
Write-Head "MCP bridge"
if ([int]($hw.nodeVer -split '\.')[0] -ge 22) { Write-Ok "Node $($hw.nodeVer) (>= 22 required)" }
else { Write-Fail "Node >= 22 not available - Claude Code cannot start comfyui-mcp" }

$settings = Join-Path $env:USERPROFILE '.claude\settings.json'
$registered = $false
if (Get-Command claude -ErrorAction SilentlyContinue) {
    if ((& claude mcp list 2>$null | Out-String) -match '(?m)^comfyui\b') {
        Write-Ok "MCP server registered (claude mcp list)"; $registered = $true
    }
}
if (-not $registered -and (Test-Path $settings) -and (Select-String -Path $settings -Pattern '"comfyui"' -Quiet)) {
    Write-Ok "MCP server registered (~\.claude\settings.json)"; $registered = $true
}
if (-not $registered) { Write-Warn "MCP server 'comfyui' is not registered - run Install-Studio.ps1 -Step mcp" }

Write-Head "Ready"
@"
  ComfyUI web UI    $Url
  Profile           $($hw.profile)
  Workflows         $(Split-Path -Parent (Split-Path -Parent $PSScriptRoot))\workflows
  Logs              $StateDir\comfyui.log

  Now ask Claude Code, for example:

    Generate a premium photorealistic e-commerce product advertisement,
    1:1 aspect ratio, professional studio lighting, clean composition,
    realistic shadows and sufficient negative space for marketing text.
"@ | Write-Host
