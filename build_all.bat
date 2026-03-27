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
set "HASH_FILE=SHA256SUMS.txt"
set "HASH_SCRIPT=%TEMP%\sekury_generate_hashes.ps1"

echo.
echo [1/5] Instalando/actualizando dependencias...
%PYTHON% -m pip install --upgrade pip setuptools wheel
if errorlevel 1 goto :fail
%PYTHON% -m pip install -r requirements.txt
if errorlevel 1 goto :fail
%PYTHON% -m pip install pyinstaller
if errorlevel 1 goto :fail

echo.
echo [2/5] Compilando ejecutable...
%PYTHON% -m PyInstaller --noconfirm --onefile --name %APP_NAME% main.py
if errorlevel 1 goto :fail

if not exist "dist\%APP_NAME%.exe" (
  echo [ERROR] No se genero dist\%APP_NAME%.exe
  goto :fail
)

copy /y "dist\%APP_NAME%.exe" "%APP_NAME%.exe" >nul
if errorlevel 1 goto :fail

echo.
echo [3/5] Creando release ZIP...
powershell -NoProfile -Command "Compress-Archive -Path '%APP_NAME%.exe','README.md','GUIA_DE_USO.txt','DISTRIBUTION_README.txt','run_sekury.bat','install_dependencies.bat','requirements.txt','whitelist.json' -DestinationPath '%APP_NAME%_release.zip' -Force"
if errorlevel 1 goto :fail

echo.
echo [4/5] Compilando instalador NSIS...
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
echo [5/5] Generando hashes SHA256...
if exist "%HASH_FILE%" del /f /q "%HASH_FILE%" >nul 2>nul
> "%HASH_SCRIPT%" (
  echo $files = @^('%APP_NAME%.exe', '%APP_NAME%_release.zip', '%APP_NAME%_Installer.exe'^)
  echo $existing = $files ^| Where-Object { Test-Path $_ }
  echo if ^(-not $existing^) { exit 1 }
  echo $lines = foreach ^($file in $existing^) {
  echo   $hash = Get-FileHash $file -Algorithm SHA256
  echo   '{0} *{1}' -f $hash.Hash, ^(Split-Path $file -Leaf^)
  echo }
  echo $lines ^| Set-Content -Encoding ASCII '%HASH_FILE%'
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%HASH_SCRIPT%"
if exist "%HASH_SCRIPT%" del /f /q "%HASH_SCRIPT%" >nul 2>nul
if not exist "%HASH_FILE%" goto :fail

echo.
echo ============================================================
echo BUILD COMPLETO
echo - %APP_NAME%.exe
echo - %APP_NAME%_release.zip
if exist "%APP_NAME%_Installer.exe" echo - %APP_NAME%_Installer.exe
if exist "%HASH_FILE%" echo - %HASH_FILE%
echo ============================================================
exit /b 0

:fail
echo.
echo [ERROR] Build fallido. Revisa el log anterior.
exit /b 1
