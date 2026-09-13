@echo off
REM One-click run for college PCs (no Mongo needed)
cd backend
if not exist node_modules ( echo Installing... & npm install )
start "SIH backend" node server.js
timeout /t 3 >nul
start "" "..\frontend\index.html"
echo Open: frontend/index.html | API: http://localhost:5000/api/health
pause
