# SEKURY NETSUITE

[![Version](https://img.shields.io/badge/version-v3.0-0f766e.svg)](https://github.com/suport-mc-ti/sekury_project)
[![Platform](https://img.shields.io/badge/platform-Windows-1d4ed8.svg)](https://github.com/suport-mc-ti/sekury_project)
[![Python](https://img.shields.io/badge/python-3.8%2B-f59e0b.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-16a34a.svg)](LICENSE)

Suite unificada de seguridad local y mapeo de red para Windows.

SEKURY NETSUITE combina en una sola herramienta:
- Analisis de conexiones locales con NETSTAT.
- Gestion activa de amenazas con firewall, procesos y whitelist.
- Escaneo de red con Nmap a traves de NETMAPPER integrado.

## Caracteristicas

- Analisis completo de conexiones activas del sistema.
- Deteccion de conexiones sospechosas y procesos de alto riesgo.
- Puntaje de riesgo para priorizar respuesta.
- Panel de amenazas para bloquear IPs, desbloquearlas o terminar procesos.
- Exportacion de reportes JSON para auditoria.
- Modulo NETMAPPER para puertos, sistema operativo, servicios y vulnerabilidades.
- Flujo de build completo con EXE, ZIP e instalador NSIS.

## Modulos

### Seguridad local

- Escaneo completo de conexiones.
- Deteccion de amenazas basada en IP, puerto, estado y proceso.
- Exportacion a `netstat_security_report.json`.

### NETMAPPER

- Escaneo rapido de puertos.
- Deteccion de sistema operativo.
- Deteccion de versiones de servicios.
- Escaneo de vulnerabilidades conocidas.
- Exportacion de reportes en `%USERPROFILE%\NetMapperCK_Reports`.

## Requisitos

- Windows 10/11.
- Python 3.8 o superior.
- Nmap instalado en el sistema: https://nmap.org/download.html
- Dependencias Python:
  - psutil
  - python-nmap

## Instalacion

```powershell
install_dependencies.bat
python main.py
```

Tambien puedes ejecutar:

```powershell
run_sekury.bat
```

## Menu principal

- `1` Escanear todas las conexiones.
- `2` Ver conexiones sospechosas.
- `3` Analisis rapido.
- `4` Ayuda.
- `A` Ejecutar todo en modo silencioso.
- `5` Panel de amenazas.
- `6` Agregar IP a lista blanca.
- `7` Ver procesos de alto riesgo.
- `8` Estado del sistema.
- `9` NETMAPPER.
- `0` Salir.

## Flujo recomendado

1. Ejecutar opcion `1` para obtener el diagnostico inicial.
2. Revisar opcion `5` si hay amenazas detectadas.
3. Exportar reporte para auditoria o seguimiento.
4. Ejecutar opcion `9` para validar superficie de red del host objetivo.

## Build y distribucion

Build completo en un paso:

```powershell
build_all.bat
```

Build por etapas:

```powershell
build_sekury.bat
build_release.bat
```

Compilacion manual de instalador:

```powershell
makensis installer.nsi
```

Artefactos esperados:
- `SEKURY_NETSUITE.exe`
- `SEKURY_NETSUITE_release.zip`
- `SEKURY_NETSUITE_Installer.exe`

## Releases

Version actual:
- `v3.0` - unificacion de OG_SEKURY y OG_NETMAPPER en una sola base.

Para futuras releases se recomienda:
- generar artefactos con `build_all.bat`;
- publicar el ZIP y el instalador en GitHub Releases;
- incluir hash SHA256 de los binarios publicados.

## Seguridad y uso responsable

- Ejecutar como Administrador solo cuando necesites acciones de firewall o gestion de procesos.
- Usar la herramienta unicamente sobre sistemas y redes autorizadas.
- Revisar hallazgos antes de bloquear procesos o IPs de forma permanente.

## Documentacion adicional

- [GUIA_DE_USO.txt](GUIA_DE_USO.txt)
- [QUICK_START_v3.0.md](QUICK_START_v3.0.md)
- [DISTRIBUTION_README.txt](DISTRIBUTION_README.txt)
- [CHANGELOG.md](CHANGELOG.md)

## Licencia

Este proyecto se distribuye bajo licencia MIT. Consulta [LICENSE](LICENSE).
