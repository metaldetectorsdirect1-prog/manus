<#
.SYNOPSIS
    Step 0 (Windows) - inspect the machine and pick a FLUX.1 Schnell profile.
.DESCRIPTION
    Downloads and installs nothing. Writes %USERPROFILE%\.comfyui-studio\hardware.json,
    which every later script reads.
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\Check-Hardware.ps1
#>
[CmdletBinding()]
param(
    [string]$ComfyHome = "$env:USERPROFILE\ComfyUI",
    [string]$StateDir  = "$env:USERPROFILE\.comfyui-studio"
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
function Write-Step { param($m) Write-Host "`n$m" -ForegroundColor White }

Write-Step "ComfyUI Studio - hardware inspection"

# ---------------------------------------------------------------- OS / CPU / RAM
$os      = Get-CimInstance Win32_OperatingSystem
$cs      = Get-CimInstance Win32_ComputerSystem
$osName  = $os.Caption
$arch    = $env:PROCESSOR_ARCHITECTURE
$cores   = $cs.NumberOfLogicalProcessors
$ramGb   = [math]::Floor($cs.TotalPhysicalMemory / 1GB)

Write-Info "OS:        $osName ($arch)"
Write-Info "CPU cores: $cores"
Write-Info "RAM:       $ramGb GB"

# ---------------------------------------------------------------- disk
$driveLetter = (Split-Path -Qualifier $ComfyHome).TrimEnd(':')
$drive       = Get-PSDrive -Name $driveLetter -ErrorAction SilentlyContinue
$diskGb      = if ($drive) { [math]::Floor($drive.Free / 1GB) } else { 0 }
Write-Info "Free disk: $diskGb GB (on $driveLetter`:)"

# ---------------------------------------------------------------- GPU
$gpuVendor = 'none'; $gpuName = 'none'; $vramGb = 0; $cudaVer = 'none'; $driverVer = 'none'

$nvidiaSmi = Get-Command nvidia-smi -ErrorAction SilentlyContinue
if ($nvidiaSmi) {
    try {
        $q = & nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv,noheader,nounits 2>$null
        if ($LASTEXITCODE -eq 0 -and $q) {
            $parts     = ($q | Select-Object -First 1) -split ',\s*'
            $gpuVendor = 'nvidia'
            $gpuName   = $parts[0]
            $vramGb    = [math]::Floor([double]$parts[1] / 1024)
            $driverVer = $parts[2]
            $smi       = & nvidia-smi 2>$null | Out-String
            if ($smi -match 'CUDA Version:\s*([\d.]+)') { $cudaVer = $Matches[1] }
        }
    } catch { Write-Warn "nvidia-smi present but failed: $_" }
}

if ($gpuVendor -eq 'none') {
    # Fall back to the display adapter so AMD cards are at least reported.
    $vid = Get-CimInstance Win32_VideoController |
           Where-Object { $_.AdapterRAM -gt 0 } | Select-Object -First 1
    if ($vid) {
        $gpuName = $vid.Name
        if ($vid.Name -match 'AMD|Radeon') { $gpuVendor = 'amd' }
        # AdapterRAM is a uint32 and wraps above 4 GB - treat it as unreliable.
        $vramGb = [math]::Floor($vid.AdapterRAM / 1GB)
    }
}

if ($gpuVendor -eq 'none') {
    Write-Warn "GPU:       none usable - CPU-only mode (very slow: minutes per image)"
} else {
    Write-Info "GPU:       $gpuName ($gpuVendor)"
    Write-Info "VRAM:      $vramGb GB"
    if ($cudaVer -ne 'none') { Write-Info "CUDA:      $cudaVer (driver $driverVer)" }
    if ($gpuVendor -eq 'amd') {
        Write-Warn "PyTorch has no ROCm build for Windows. This will run on CPU;"
        Write-Warn "use WSL2 + the Linux scripts for AMD GPU acceleration."
    }
}

# ---------------------------------------------------------------- toolchain
function Get-ToolVersion {
    param([string]$Exe, [string[]]$VersionArgs)
    $cmd = Get-Command $Exe -ErrorAction SilentlyContinue
    if (-not $cmd) { return 'none' }
    try { (& $Exe @VersionArgs 2>$null | Select-Object -First 1) } catch { 'none' }
}

$pyBin = 'none'; $pyVer = 'none'
foreach ($cand in @('python', 'python3', 'py')) {
    $c = Get-Command $cand -ErrorAction SilentlyContinue
    if (-not $c) { continue }
    try {
        $v = & $cand -c "import sys;print('%d.%d'%sys.version_info[:2])" 2>$null
        if ($v -and [version]"$v" -ge [version]'3.10') { $pyBin = $cand; $pyVer = $v; break }
    } catch { }
}
if ($pyBin -ne 'none') { Write-Info "Python:    $pyVer ($pyBin)" } else { Write-Warn "Python:    no >= 3.10 found" }

$gitVer  = (Get-ToolVersion git  @('--version'))  -replace 'git version\s*',''
$nodeVer = (Get-ToolVersion node @('--version'))  -replace '^v',''
$npmVer  =  Get-ToolVersion npm  @('--version')
Write-Info "Git:       $gitVer"
Write-Info "Node:      $nodeVer (npm $npmVer)"

# ---------------------------------------------------------------- profile
# Download sizes are the verified byte counts from config/model-profiles.json,
# rounded up: high 34.67, balanced/low/cpu 29.77, gguf 11.27.
$profile_ = 'cpu'; $flags = @('--cpu'); $dl = 30
if ($gpuVendor -eq 'nvidia') {
    if     ($vramGb -ge 24) { $profile_='high';     $flags=@();            $dl=35 }
    elseif ($vramGb -ge 16) { $profile_='balanced'; $flags=@();            $dl=30 }
    elseif ($vramGb -ge 10) { $profile_='low';      $flags=@('--lowvram'); $dl=30 }
    elseif ($vramGb -ge 6)  { $profile_='gguf';     $flags=@('--lowvram'); $dl=12 }
}

$qwenOk = ($vramGb -ge 12 -and $diskGb -ge 80)

Write-Step "Verdict"
Write-Host "  profile           $profile_"
Write-Host "  launch flags      $(if ($flags) { $flags -join ' ' } else { '<none>' })"
Write-Host "  model download    ~$dl GB"
Write-Host "  Qwen-Image (opt)  $(if ($qwenOk) { 'yes' } else { 'no' })"

$blockers = 0
if ($pyBin  -eq 'none') { Write-Fail "Python >= 3.10 is required"; $blockers++ }
if ($gitVer -eq 'none') { Write-Fail "Git is required"; $blockers++ }
if ($nodeVer -eq 'none') {
    Write-Fail "Node.js >= 22 is required for the MCP server"; $blockers++
} elseif ([int]($nodeVer -split '\.')[0] -lt 22) {
    Write-Fail "Node.js is $nodeVer - the MCP server needs >= 22"; $blockers++
}
$needGb = $dl + 15
if ($diskGb -lt $needGb) { Write-Fail "Need ~$needGb GB free, found $diskGb GB"; $blockers++ }
if ($ramGb -lt 16) { Write-Warn "RAM is $ramGb GB. FLUX needs ~16 GB system RAM to load comfortably." }
if ($profile_ -eq 'cpu') { Write-Warn "No usable GPU: generation will take MINUTES per image." }

New-Item -ItemType Directory -Force -Path $StateDir | Out-Null
[pscustomobject]@{
    generated = (Get-Date).ToUniversalTime().ToString('o')
    osName=$osName; arch=$arch; cpuCores=$cores; ramGb=$ramGb; diskAvailGb=$diskGb
    gpuVendor=$gpuVendor; gpuName=$gpuName; vramGb=$vramGb
    cudaVer=$cudaVer; driverVer=$driverVer
    pyBin=$pyBin; pyVer=$pyVer; gitVer=$gitVer; nodeVer=$nodeVer
    profile=$profile_; launchFlags=$flags; estDownloadGb=$dl
    qwenOk=$qwenOk; blockers=$blockers; comfyHome=$ComfyHome
} | ConvertTo-Json -Depth 4 | Set-Content -Encoding UTF8 (Join-Path $StateDir 'hardware.json')

Write-Host ""
if ($blockers -gt 0) {
    Write-Fail "$blockers blocker(s) above must be fixed before installing. Nothing was downloaded."
    exit 1
}
Write-Ok "hardware verified - report written to $StateDir\hardware.json"
Write-Ok "next: .\Install-Studio.ps1"
