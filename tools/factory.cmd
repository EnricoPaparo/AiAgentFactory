@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%.."
set "FACTORY_SCRIPT=%SCRIPT_DIR%factory.py"

where python >nul 2>nul
if %ERRORLEVEL%==0 (
  pushd "%REPO_ROOT%"
  python "%FACTORY_SCRIPT%" %*
  set "EXIT_CODE=%ERRORLEVEL%"
  popd
  exit /b %EXIT_CODE%
)

set "BUNDLED=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%BUNDLED%" (
  pushd "%REPO_ROOT%"
  "%BUNDLED%" "%FACTORY_SCRIPT%" %*
  set "EXIT_CODE=%ERRORLEVEL%"
  popd
  exit /b %EXIT_CODE%
)

echo No Python runtime found. Install Python or use the Codex bundled runtime. 1>&2
exit /b 1
