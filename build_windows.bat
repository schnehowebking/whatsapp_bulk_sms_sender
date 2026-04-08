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

if exist "runtime" (
    echo [5/6] Copying bundled runtime folder...
    if exist "dist\WBSSender\runtime" rmdir /s /q "dist\WBSSender\runtime"
    xcopy /e /i /y "runtime" "dist\WBSSender\runtime" >nul || goto :error
) else (
    echo [5/6] No runtime folder found. Skipping runtime copy.
)

echo [6/6] Build finished.
echo Output: dist\WBSSender\WBSSender.exe
popd
exit /b 0

:error
echo Build failed.
popd
exit /b 1
