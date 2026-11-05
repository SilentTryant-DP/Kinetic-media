@echo off
setlocal
title Kinetic Social - Requirements Installer
echo ========================================================
echo       Installing All Requirements for Kinetic Social
echo ========================================================
echo.

set "PATH=C:\Users\vansh\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.20.0-win-x64;%PATH%"

echo [1/2] Installing Backend API Requirements (Express, mysql2, bcrypt, cors, dotenv)...
cd /d "%~dp0backend"
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install backend requirements.
    pause
    exit /b 1
)

echo.
echo [2/2] Installing Frontend Requirements (React 18, Vite, Lucide)...
cd /d "%~dp0frontend"
call npm install
if errorlevel 1 (
    echo [ERROR] Failed to install frontend requirements.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo   All requirements installed successfully!
echo   You can now launch the app with: run_project.bat
echo ========================================================
pause
