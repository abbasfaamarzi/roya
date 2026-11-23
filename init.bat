@echo off
echo ================================================
echo    Running initialization commands
echo ================================================

echo [Running terminal commands]
git rm -r -f --ignore-unmatch behaviors components controllers core effects foundation static templates templatetags theme _build_
rmdir /s /q behaviors 2>nul
rmdir /s /q components 2>nul
rmdir /s /q controllers 2>nul
rmdir /s /q core 2>nul
rmdir /s /q effects 2>nul
rmdir /s /q foundation 2>nul
rmdir /s /q static 2>nul
rmdir /s /q templates 2>nul
rmdir /s /q templatetags 2>nul
rmdir /s /q theme 2>nul
rmdir /s /q _build_ 2>nul
git add -A
git commit -m "chore: remove duplicate top-level packages and _build_ artifacts after move into roya/"
git push origin master
dir /b roya

echo ================================================
echo    All commands executed successfully.
echo ================================================
pause
