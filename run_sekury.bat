@echo off
REM Run SEKURY NETSUITE from this folder by double-clicking this batch file
cd /d "%~dp0"

echo Ejecutando SEKURY NETSUITE...
if exist SEKURY_NETSUITE.exe (
	echo Found SEKURY_NETSUITE.exe - ejecutando...
	SEKURY_NETSUITE.exe %*
) else (
	python main.py %*
)

echo Presiona una tecla para salir...
pause >nul
