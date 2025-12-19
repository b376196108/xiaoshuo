@echo off
setlocal enabledelayedexpansion

REM Resolve repo root as parent of this script directory.
set "ROOT_DIR=%~dp0.."
cd /d "%ROOT_DIR%" || exit /b 1

python tools\run_daily.py %*
exit /b %ERRORLEVEL%

