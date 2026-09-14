# One-time setup for the KDP publish bot on Windows. Re-runnable.
# Run in PowerShell from the repo root:
#     powershell -ExecutionPolicy Bypass -File scripts\kdp\setup.ps1
$ErrorActionPreference = "Stop"

$botDir = Join-Path $HOME "kdp-bot"
New-Item -ItemType Directory -Force -Path (Join-Path $botDir "shots") | Out-Null

# Find a usable Python 3.
$py = $null
foreach ($candidate in @("py", "python", "python3")) {
    if (Get-Command $candidate -ErrorAction SilentlyContinue) { $py = $candidate; break }
}
if (-not $py) {
    Write-Error "Python 3 not found. Install it from https://www.python.org/downloads/ (tick 'Add python.exe to PATH'), then re-run this script."
}

Push-Location $botDir
if (-not (Test-Path ".venv")) {
    if ($py -eq "py") { & py -3 -m venv .venv } else { & $py -m venv .venv }
}

$venvPy = Join-Path $botDir ".venv\Scripts\python.exe"
& $venvPy -m pip install --quiet --upgrade pip playwright
& $venvPy -m playwright install chromium

# Copy the bot next to the venv so it runs from a stable location.
$src = Join-Path $PSScriptRoot "publish.py"
Copy-Item $src (Join-Path $botDir "publish.py") -Force
Pop-Location

Write-Host ""
Write-Host "Ready. Now run:" -ForegroundColor Green
Write-Host "    cd `$HOME\kdp-bot"
Write-Host "    .\.venv\Scripts\Activate.ps1"
Write-Host "    python publish.py"
Write-Host ""
Write-Host "Before running, confirm these two files exist:" -ForegroundColor Yellow
Write-Host "    $HOME\Downloads\the-wife-he-scheduled-around_digital.epub"
Write-Host "    $HOME\Downloads\the-wife-he-scheduled-around_cover.jpg"
