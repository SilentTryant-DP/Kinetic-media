@echo off
title Kinetic Social - React Vite Frontend (Port 5173)
set "PATH=C:\Users\vansh\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.20.0-win-x64;%PATH%"
cd /d "%~dp0frontend"
if not exist "node_modules\" (
    echo [INFO] Frontend requirements missing. Installing automatically...
    call npm install
)
echo Starting Vite Frontend on http://localhost:5173 ...
npm run dev
pause
