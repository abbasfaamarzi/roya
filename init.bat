@echo off
echo ================================================
echo    Running initialization commands
echo ================================================

echo [Running terminal commands]
pip install -e .
python -c "import roya; print('roya OK ->', roya.__file__)"

echo ================================================
echo    All commands executed successfully.
echo ================================================
pause
