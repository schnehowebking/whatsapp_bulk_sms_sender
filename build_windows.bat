@echo off
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
pushd "%SCRIPT_DIR%"

echo [1/5] Creating virtual environment...
if not exist ".venv" (
    py -3 -m venv .venv || goto :error
)

echo [2/5] Activating virtual environment...
call ".venv\Scripts\activate.bat" || goto :error

echo [3/5] Installing dependencies...
python -m pip install --upgrade pip || goto :error
python -m pip install -r requirements.txt pyinstaller || goto :error

echo [4/5] Building executable...
pyinstaller --noconfirm --clean --windowed --name WBSSender main.py || goto :error

echo [5/5] Build finished.
echo Output: dist\WBSSender\WBSSender.exe
popd
exit /b 0

:error
echo Build failed.
popd
exit /b 1
