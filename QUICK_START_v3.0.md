# QUICK START - SEKURY NETSUITE v3.0

## Inicio rapido

1. Instala dependencias.

```powershell
install_dependencies.bat
```

2. Ejecuta la suite.

```powershell
python main.py
```

3. Escaneo inicial.
- Opcion 1 para analisis completo.
- Confirma con S.

4. Gestion de amenazas.
- Opcion 5 para abrir panel de amenazas.
- Acciones: bloquear IP, desbloquear IP, terminar proceso, whitelist.

5. Mapeo de red.
- Opcion 9 para abrir NETMAPPER.
- Escoge tipo de escaneo (puertos, SO, servicios, vulnerabilidades).

## Menu resumido

- 1 Analisis completo local.
- 2 Solo conexiones sospechosas.
- 3 Analisis rapido.
- 4 Ayuda.
- A Ejecutar todo silencioso.
- 5 Panel de amenazas.
- 6 Agregar IP a whitelist.
- 7 Procesos de alto riesgo.
- 8 Estado del sistema.
- 9 NETMAPPER.
- 0 Salir.

## Requisitos

- Python 3.8+
- psutil
- python-nmap
- Nmap instalado (sistema)

## Archivos de salida

- netstat_security_report.json
- whitelist.json
- %USERPROFILE%\NetMapperCK_Reports\nmap_scan_*.json

## Build y release

```powershell
build_sekury.bat
build_release.bat
```

## Recomendacion

Ejecuta como Administrador para acceso completo a conexiones, firewall y procesos.
