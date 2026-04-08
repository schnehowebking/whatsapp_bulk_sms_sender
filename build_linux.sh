#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "[1/5] Creating virtual environment..."
if [[ ! -d ".venv" ]]; then
  python3 -m venv .venv
fi

echo "[2/5] Activating virtual environment..."
source .venv/bin/activate

echo "[3/5] Installing dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller

echo "[4/5] Building executable..."
pyinstaller --noconfirm --clean --windowed --name WBSSender main.py

echo "[5/5] Build finished."
echo "Output: dist/WBSSender/WBSSender"
