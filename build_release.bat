@echo off
REM Build release: create SEKURY_NETSUITE.exe and package into a ZIP
cd /d "%~dp0"

echo Running build_sekury.bat to produce SEKURY_NETSUITE.exe...
call build_sekury.bat

if exist SEKURY_NETSUITE.exe (
  echo SEKURY_NETSUITE.exe found. Creating release ZIP...
  powershell -NoProfile -Command "Compress-Archive -Path 'SEKURY_NETSUITE.exe','README.md','GUIA_DE_USO.txt','DISTRIBUTION_README.txt','run_sekury.bat','install_dependencies.bat','requirements.txt','whitelist.json' -DestinationPath 'SEKURY_NETSUITE_release.zip' -Force"
  if exist SEKURY_NETSUITE_release.zip (
    echo Release created: SEKURY_NETSUITE_release.zip
  ) else (
    echo Failed to create ZIP. Check permissions.
  )
) else (
  echo SEKURY_NETSUITE.exe not found; build may have failed. Check build_sekury.bat output.
)

echo Done. Presiona una tecla para salir...
pause >nul
