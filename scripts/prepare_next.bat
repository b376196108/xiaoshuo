@echo off
setlocal
pushd "%~dp0.."
python tools\prepare_next_run.py %*
set EXITCODE=%ERRORLEVEL%
popd
exit /b %EXITCODE%