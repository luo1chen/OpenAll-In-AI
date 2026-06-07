@echo off
echo ========================================
echo   OpenAll-In-AI - Starting Frontend
echo ========================================
echo.

cd /d %~dp0..\frontend

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 18+ from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if dependencies are installed
if not exist "node_modules" (
    echo Installing dependencies...
    npm install
)

echo Starting frontend development server...
npm run dev

pause