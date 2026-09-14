#!/usr/bin/env bash
# One-time setup for the KDP publish bot on macOS / Linux. Re-runnable.
# Windows users: run scripts/kdp/setup.ps1 in PowerShell instead.
set -euo pipefail
mkdir -p ~/kdp-bot/shots
cd ~/kdp-bot
[ -d .venv ] || python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q --upgrade pip playwright
python -m playwright install chromium
cp "$(dirname "$0")/publish.py" ~/kdp-bot/publish.py
echo "Ready. Run:  cd ~/kdp-bot && source .venv/bin/activate && python publish.py"
