@echo off
REM Script to build SEKURY_NETSUITE.exe using PyInstaller
cd /d "%~dp0"

echo Installing wheel and PyInstaller (may require internet access)...
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python -m pip install pyinstaller

echo Building SEKURY NETSUITE (one-file executable)...
python -m PyInstaller --noconfirm --onefile --name SEKURY_NETSUITE main.py

if exist dist\SEKURY_NETSUITE.exe (
  echo Build successful - copying SEKURY_NETSUITE.exe to project root...
  copy /y dist\SEKURY_NETSUITE.exe SEKURY_NETSUITE.exe >nul
  echo SEKURY_NETSUITE.exe is ready in this folder.
) else (
  echo Build did not produce dist\SEKURY_NETSUITE.exe. Check PyInstaller output above.
)

echo Done. Presiona una tecla para salir...
pause >nul
