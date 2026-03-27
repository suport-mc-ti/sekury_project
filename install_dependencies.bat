@echo off
REM Instalador de dependencias para SEKURY NETSUITE
echo Verificando Python...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python no encontrado en PATH.
    echo Por favor instala Python 3.7+ desde: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Creando/actualizando pip y instalando dependencias desde requirements.txt...
python -m pip install --upgrade pip
if exist requirements.txt (
    python -m pip install -r requirements.txt
) else (
    echo requirements.txt no encontrado - instalando dependencias por defecto
    python -m pip install psutil python-nmap
)

echo.
echo Verificando Nmap en el sistema (requerido para modulo NETMAPPER)...
where nmap >nul 2>nul
if %errorlevel% neq 0 (
    echo [ADVERTENCIA] Nmap no esta en PATH.
    echo Descarga Nmap desde: https://nmap.org/download.html
)

echo.
echo Dependencias instaladas. Ejecuta: python main.py
echo Recomendado: Ejecutar como Administrador para analisis completo y acciones de firewall.
pause
