@echo off
echo ========================================
echo   OpenAll-In-AI - One-Click Start
echo ========================================
echo.

cd /d %~dp0..

REM Start backend in a new window
echo Starting Backend Server...
start "OpenAll-In-AI Backend" cmd /c scripts\start_backend.bat

REM Wait for backend to start
timeout /t 5 /nobreak >nul

REM Start frontend in a new window
echo Starting Frontend Server...
start "OpenAll-In-AI Frontend" cmd /c scripts\start_frontend.bat

echo.
echo ========================================
echo   Both servers are starting!
echo   Backend: http://localhost:8000
echo   Frontend: http://localhost:3000
echo ========================================
echo.

pause