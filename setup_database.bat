@echo off
setlocal
title Kinetic Social - Database Setup
set "PATH=C:\Users\vansh\AppData\Local\Microsoft\WinGet\Packages\OpenJS.NodeJS.LTS_Microsoft.Winget.Source_8wekyb3d8bbwe\node-v24.20.0-win-x64;%PATH%"
set "NODE_PATH=%~dp0backend\node_modules;%NODE_PATH%"

if not exist "%~dp0backend\node_modules\" (
    echo [INFO] Backend requirements not found. Installing automatically...
    cd /d "%~dp0backend"
    call npm install
    echo.
)

cd /d "%~dp0database"

echo ========================================================
echo       Kinetic Social DBMS - MySQL Database Setup
echo ========================================================
echo.

set /p MYSQL_PWD="Enter your MySQL root password (press Enter to use configured password): "

echo.
echo Running database migration and seeding via Node.js...
node setup_db.js "%MYSQL_PWD%"
if errorlevel 1 (
    echo.
    echo [ERROR] Database setup failed. Please check your MySQL password.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo   Database setup completed successfully!
echo   Password saved to backend\.env
echo ========================================================
pause
