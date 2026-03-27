SEKURY NETSUITE - Release Notes and Installation
================================================

Contenido del paquete:
- SEKURY_NETSUITE.exe          -> Aplicacion principal (one-file)
- run_sekury.bat               -> Lanza SEKURY_NETSUITE.exe o python main.py
- install_dependencies.bat     -> Instalador de dependencias Python
- README.md                    -> Documentacion principal
- GUIA_DE_USO.txt              -> Guia corta para usuario final
- whitelist.json               -> Lista blanca editable

Artefactos de salida esperados:
- SEKURY_NETSUITE.exe
- SEKURY_NETSUITE_release.zip
- SEKURY_NETSUITE_Installer.exe

Instalacion y ejecucion:
1) Descomprime SEKURY_NETSUITE_release.zip.
2) Ejecuta SEKURY_NETSUITE.exe.
3) Para acciones de firewall/procesos, ejecuta como Administrador.

Dependencias (si ejecutas python main.py):
- Python 3.8+ en PATH.
- Nmap instalado en el sistema.
- Ejecuta install_dependencies.bat.

Build y empaquetado:
- build_all.bat (flujo completo automatizado)
- build_sekury.bat
- build_release.bat
- makensis installer.nsi

Recomendaciones de distribucion:
- Probar en VM o entorno de staging.
- Firmar el ejecutable para reducir falsos positivos.
- Publicar hash SHA256 del EXE distribuido.

Contacto del proyecto:
- Proyecto: SEKURY NETSUITE v3.0
