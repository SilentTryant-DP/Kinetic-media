@echo off
title Kinetic Social - Backend API (Port 3000)
set "PATH=C:\Users\vansh\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.20.0-win-x64;%PATH%"
cd /d "%~dp0backend"
if not exist "node_modules\" (
    echo [INFO] Backend requirements missing. Installing automatically...
    call npm install
)
echo Starting Express Backend API on http://localhost:3000 ...
npm start
pause
