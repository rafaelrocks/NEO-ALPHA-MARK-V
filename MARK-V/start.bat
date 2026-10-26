@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" main.py
) else (
    python main.py
)
if errorlevel 1 (
    echo NEO Alpha exited with an error. Review the message above.
    pause
)