# NEO Alpha MARK-V

NEO Alpha is a Windows desktop assistant. Follow these steps to set up and run
the project from a fresh clone or extracted ZIP.

## 1. Install Python and download the project

Use 64-bit Python 3.11 on Windows 10 or 11. During Python installation, enable
the option to add Python to PATH. In PowerShell, check that the Python launcher
is available:

```powershell
py -3.11 --version
```

Clone the repository in PowerShell, or download it from GitHub using
**Code > Download ZIP** and extract it. For a clone, run:

```powershell
git clone https://github.com/rafaelrocks/NEO-ALPHA-MARK-V.git
cd NEO-ALPHA-MARK-V\MARK-V
```

For an extracted ZIP, `cd` into its `NEO-ALPHA-MARK-V\MARK-V` folder instead.

## 2. Create the API keys

The application uses both a Gemini key and an OpenRouter key:

1. Sign in to [Google AI Studio](https://aistudio.google.com/app/apikey), create
   an API key, and copy it.
2. Sign in to [OpenRouter](https://openrouter.ai/keys), create a key, and copy
   it. Provider accounts, usage limits, or billing may be required.

## 3. Add the keys to the configuration file

From the repository root, open `MARK-V\config\api_keys.json` in a text editor.
If you followed step 1 and are already in the `MARK-V` folder, open
`config\api_keys.json`. Replace the two `REPLACE_WITH_...` values with your
own keys, keeping the quotation marks and commas. Leave `os_system` set to
`windows`.

```json
{
  "gemini_api_key": "YOUR_GEMINI_KEY",
  "openrouter_api_key": "YOUR_OPENROUTER_KEY",
  "os_system": "windows"
}
```

Keep this file private. Do not paste keys into source code, screenshots, chat,
or commits. If a key is exposed, revoke it with its provider and create a new
one.

## 4. Install the project requirements

Run these commands from the `MARK-V` folder in PowerShell. The virtual
environment keeps this project's packages separate from other Python projects:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium
```

## 5. Start the application

From the `MARK-V` folder, run:

```powershell
.\start.bat
```

The launcher uses `.venv` when it exists and starts the app in the project
folder. You can also run it directly:

```powershell
.\.venv\Scripts\python.exe main.py
```

## 6. Check that it works

Wait for the NEO Alpha window to open, then send a simple prompt such as
`What is 2 + 2?`. A response confirms the application started and its Gemini
key is working. If the app reports a missing or invalid key, recheck the
matching value in `config\api_keys.json`. If browser automation reports a
missing browser, rerun the Playwright install command above.

## Optional Telegram integration

Telegram is not required to run the desktop app. To enable it, set the
`TG_TOKEN` and `TG_USER_ID` environment variables in the same PowerShell
window before starting `start.bat`. Do not put a Telegram bot token or personal
user ID in a committed file.
