@echo off
REM Build script for PaperLens Mini Windows Executable
REM This script automates the build process using PyInstaller

echo ========================================
echo 🪟 PaperLens Mini Windows Build Script
echo ========================================
echo.

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..\..\..

echo 📁 Project root: %PROJECT_ROOT%
echo.

REM Check if PyInstaller is installed
where pyinstaller >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ PyInstaller not found
    echo    Install with: pip install pyinstaller
    pause
    exit /b 1
)
echo ✅ PyInstaller found
echo.

REM Clean previous builds
echo 🧹 Cleaning previous builds...
cd /d "%PROJECT_ROOT%"
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo ✅ Cleaned
echo.

REM Build the executable
echo 🔨 Building PaperLensMini.exe...
echo    This may take 3-5 minutes...
echo.

pyinstaller "%SCRIPT_DIR%paperlens_mini_windows.spec" --clean --noconfirm

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Build successful!
    echo.
    echo 📦 Executable created:
    echo    %PROJECT_ROOT%\dist\PaperLensMini.exe
    echo.
    
    REM Show size
    for %%A in ("%PROJECT_ROOT%\dist\PaperLensMini.exe") do (
        set size=%%~zA
        set /a sizeInMB=!size! / 1048576
        echo 💾 Executable size: !sizeInMB! MB
    )
    echo.
    
    REM Test if exe exists
    if exist "%PROJECT_ROOT%\dist\PaperLensMini.exe" (
        echo ✅ Executable created successfully
        echo.
        echo 🚀 To run the application:
        echo    dist\PaperLensMini.exe
        echo.
        echo 📤 To create installer:
        echo    Use Inno Setup with installer.iss
        echo    Or create ZIP: Compress-Archive -Path dist\PaperLensMini.exe
        echo.
        
        REM Ask if user wants to run
        set /p RUN="Run the application now? (Y/N): "
        if /i "%RUN%"=="Y" (
            start "" "%PROJECT_ROOT%\dist\PaperLensMini.exe"
        )
    ) else (
        echo ❌ Executable not found
        pause
        exit /b 1
    )
) else (
    echo.
    echo ❌ Build failed
    echo    Check the error messages above
    pause
    exit /b 1
)

pause
