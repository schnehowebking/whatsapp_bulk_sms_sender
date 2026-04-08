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

if [[ -d "runtime" ]]; then
  echo "[5/6] Copying bundled runtime folder..."
  rm -rf dist/WBSSender/runtime
  cp -r runtime dist/WBSSender/runtime
else
  echo "[5/6] No runtime folder found. Skipping runtime copy."
fi

echo "[6/6] Build finished."
echo "Output: dist/WBSSender/WBSSender"
