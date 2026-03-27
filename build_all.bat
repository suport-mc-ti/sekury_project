@echo off
setlocal
cd /d "%~dp0"

echo ============================================================
echo   SEKURY NETSUITE - BUILD ALL (EXE + ZIP + INSTALLER)
echo ============================================================

where python >nul 2>nul
if errorlevel 1 (
  echo [ERROR] Python no encontrado en PATH.
  exit /b 1
)

set "PYTHON=python"
set "APP_NAME=SEKURY_NETSUITE"
set "NSIS_EXE="

echo.
echo [1/4] Instalando/actualizando dependencias...
%PYTHON% -m pip install --upgrade pip setuptools wheel
if errorlevel 1 goto :fail
%PYTHON% -m pip install -r requirements.txt
if errorlevel 1 goto :fail
%PYTHON% -m pip install pyinstaller
if errorlevel 1 goto :fail

echo.
echo [2/4] Compilando ejecutable...
%PYTHON% -m PyInstaller --noconfirm --onefile --name %APP_NAME% main.py
if errorlevel 1 goto :fail

if not exist "dist\%APP_NAME%.exe" (
  echo [ERROR] No se genero dist\%APP_NAME%.exe
  goto :fail
)

copy /y "dist\%APP_NAME%.exe" "%APP_NAME%.exe" >nul
if errorlevel 1 goto :fail

echo.
echo [3/4] Creando release ZIP...
powershell -NoProfile -Command "Compress-Archive -Path '%APP_NAME%.exe','README.md','GUIA_DE_USO.txt','DISTRIBUTION_README.txt','run_sekury.bat','install_dependencies.bat','requirements.txt','whitelist.json' -DestinationPath '%APP_NAME%_release.zip' -Force"
if errorlevel 1 goto :fail

echo.
echo [4/4] Compilando instalador NSIS...
where makensis >nul 2>nul
if not errorlevel 1 (
  set "NSIS_EXE=makensis"
)
if not defined NSIS_EXE if exist "C:\Program Files (x86)\NSIS\makensis.exe" (
  set "NSIS_EXE=C:\Program Files (x86)\NSIS\makensis.exe"
)
if not defined NSIS_EXE if exist "C:\Program Files\NSIS\makensis.exe" (
  set "NSIS_EXE=C:\Program Files\NSIS\makensis.exe"
)

if defined NSIS_EXE (
  "%NSIS_EXE%" installer.nsi
  if errorlevel 1 goto :fail
) else (
  echo [WARN] NSIS no encontrado. Se omite instalador.
)

echo.
echo ============================================================
echo BUILD COMPLETO
echo - %APP_NAME%.exe
echo - %APP_NAME%_release.zip
if exist "%APP_NAME%_Installer.exe" echo - %APP_NAME%_Installer.exe
echo ============================================================
exit /b 0

:fail
echo.
echo [ERROR] Build fallido. Revisa el log anterior.
exit /b 1
