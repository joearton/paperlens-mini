@echo off
echo ====================================
echo PaperLens Mini Launcher
echo ====================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install/update dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Run application
echo Starting PaperLens Mini...
echo.
python app.py

pause

