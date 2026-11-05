@echo off
setlocal
title Kinetic Social - Master Launcher
echo ========================================================
echo       Starting Kinetic Social Full-Stack Application
echo ========================================================
echo.
set "PATH=C:\Users\vansh\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.20.0-win-x64;%PATH%"

:: 1. Auto-install backend requirements if missing
if not exist "%~dp0backend\node_modules\" (
    echo [INFO] Backend requirements not found. Installing automatically...
    cd /d "%~dp0backend"
    call npm install
    echo.
)

:: 2. Auto-install frontend requirements if missing
if not exist "%~dp0frontend\node_modules\" (
    echo [INFO] Frontend requirements not found. Installing automatically...
    cd /d "%~dp0frontend"
    call npm install
    echo.
)

echo Launching Backend API (Port 3000)...
start "Kinetic Social - Backend API" cmd /k "set \"PATH=C:\Users\vansh\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.20.0-win-x64;%PATH%\" && cd /d "%~dp0backend" && npm start"

timeout /t 2 /nobreak >nul

echo Launching Frontend Web Client (Port 5173)...
start "Kinetic Social - Frontend Client" cmd /k "set \"PATH=C:\Users\vansh\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.20.0-win-x64;%PATH%\" && cd /d "%~dp0frontend" && npm run dev"

echo.
echo Both services have been launched in separate terminal windows!
echo Once started, open your browser at: http://localhost:5173
echo.
pause
