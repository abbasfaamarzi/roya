@echo off
echo ================================================
echo    Running initialization commands
echo ================================================

echo [Running terminal commands]
python manage.py migrate

echo ================================================
echo    All commands executed successfully.
echo ================================================
pause
