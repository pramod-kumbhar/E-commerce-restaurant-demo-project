:: @echo off

:: Change directory
cd /d "%~dp0"

:: Activate virtual environment and running project
start cmd /k "call env\Scripts\activate && python manage.py runserver"

:: Wait for a moment to let the server start
timeout /t 5 /nobreak >nul

:: Open project in browser
start msedge http://127.0.0.1:8000/