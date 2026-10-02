@echo off
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start_match_review_windows.ps1"
if errorlevel 1 echo Setup stopped with an error. Read the message above.
pause
