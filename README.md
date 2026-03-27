# SEKURY NETSUITE v3.0

Suite unificada de seguridad local y mapeo de red.

Integra en una sola herramienta:
- Analisis de conexiones locales con NETSTAT.
- Gestion activa de amenazas (firewall, procesos, whitelist).
- Escaneo de red con Nmap (NETMAPPER integrado).

## Modulos

1. Modulo Seguridad Local
- Escaneo completo de conexiones.
- Deteccion de conexiones sospechosas.
- Puntaje de riesgo y procesos de alto riesgo.
- Exportacion a netstat_security_report.json.

2. Modulo NETMAPPER
- Escaneo rapido de puertos.
- Deteccion de sistema operativo.
- Deteccion de versiones de servicios.
- Escaneo de vulnerabilidades conocidas.
- Exportacion de reportes en %USERPROFILE%\NetMapperCK_Reports.

## Requisitos

- Windows 10/11 (compatible con 7/8 si entorno lo permite).
- Python 3.8+ recomendado.
- Dependencias Python:
  - psutil
  - python-nmap
- Nmap instalado en el sistema:
  - https://nmap.org/download.html

## Instalacion

1. Abrir terminal en la carpeta del proyecto.
2. Ejecutar:

```powershell
install_dependencies.bat
```

3. Ejecutar la app:

```powershell
python main.py
```

Tambien puedes usar el ejecutable:

```powershell
run_sekury.bat
```

## Menu Principal

- 1: Escanear todas las conexiones.
- 2: Ver conexiones sospechosas.
- 3: Analisis rapido.
- 4: Ayuda.
- A: Ejecutar todo (silencioso).
- 5: Panel de amenazas.
- 6: Agregar IP a lista blanca.
- 7: Ver procesos de alto riesgo.
- 8: Estado del sistema.
- 9: NETMAPPER (Nmap).
- 0: Salir.

## Flujo recomendado de uso

1. Ejecutar opcion 1 para diagnostico inicial.
2. Revisar opcion 5 si hay amenazas.
3. Exportar reporte para auditoria.
4. Ejecutar opcion 9 para validar superficie de red.

## Build y distribucion

- Build completo en un solo paso (EXE + ZIP + Installer):

```powershell
build_all.bat
```

- Build ejecutable:

```powershell
build_sekury.bat
```

- Build release ZIP:

```powershell
build_release.bat
```

- Crear instalador NSIS:

```powershell
makensis installer.nsi
```

Artefactos esperados:
- SEKURY_NETSUITE.exe
- SEKURY_NETSUITE_release.zip
- SEKURY_NETSUITE_Installer.exe

## Notas de seguridad

- Ejecutar como Administrador para acciones de firewall y procesos.
- Usar solo en sistemas y redes autorizadas.

## Version

- v3.0 (Marzo 2026): Proyecto unificado SEKURY + NETMAPPER.
