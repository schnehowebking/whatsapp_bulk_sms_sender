# Desktop WhatsApp Bulk Sender

PySide6 desktop app to import contacts and send WhatsApp messages/files in bulk through WhatsApp Web (Selenium).

## Features
- Import contacts from `.csv`, `.xls`, `.xlsx`
- Validate Bangladeshi mobile numbers
- Preview valid/invalid contacts before import
- Send text and optional attachment to selected contacts
- Save send logs to SQLite and export logs to CSV

## Quick Start (End Users)

### Windows
1. Download the `WBSSender-windows` artifact/release.
2. Open `WBSSender.exe` inside the extracted `WBSSender` folder.
3. Click **Connect WhatsApp** and scan QR if needed.
4. Click **Import Contacts**, select your file, import valid contacts.
5. Select contacts, write message (and optional attachment), then click **Send**.

### Linux
1. Download the `WBSSender-linux` artifact/release.
2. Make binary executable:
```bash
chmod +x WBSSender
```
3. Run:
```bash
./WBSSender
```
4. Connect WhatsApp, import contacts, and send.

## Contact File Format
Your input file must have these columns:
- `name`
- `phone`

Column names are case-insensitive (`Name`, `PHONE`, etc. work).

## Bundled Browser (Recommended for Stable Deployment)
The app can use a fixed bundled Chromium + chromedriver if present.

Expected folder layout inside app directory:
```text
runtime/
  chromium/
    chrome.exe (Windows) OR chrome/chromium (Linux)
  chromedriver/
    chromedriver.exe (Windows) OR chromedriver (Linux)
```

If bundled binaries are not found, app falls back to system browser/Selenium Manager.

## Developer Setup
```bash
pip install -r requirements.txt
python main.py
```

## Build Executables

### Windows
```bat
build_windows.bat
```
Output:
- `dist\WBSSender\WBSSender.exe`

### Linux
```bash
chmod +x build_linux.sh
./build_linux.sh
```
Output:
- `dist/WBSSender/WBSSender`

If `runtime/` exists in repo root, build scripts copy it to `dist/WBSSender/runtime`.

## GitHub Actions (Automatic Builds)
Workflow file:
- `.github/workflows/build.yml`

Triggers:
- Push to `main` or `master`
- Manual run (`workflow_dispatch`)

Artifacts produced:
- `WBSSender-windows`
- `WBSSender-linux`

## Tests
```bash
python -m unittest discover -s tests -v
```

## Notes
- Use responsibly and comply with WhatsApp policies and local regulations.
- UI selectors in WhatsApp Web may change over time; update Selenium locators if needed.
