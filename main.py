#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🛡️ SEKURY NETSUITE 🛡️
Suite unificada de ciberseguridad y mapeo de red
Analiza conexiones locales y escanea red con Nmap
VERSIÓN 3.0
"""

import sys
import io
import os

# Configurar encoding UTF-8 para stdout
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    if os.name == 'nt':  # Windows
        os.system('chcp 65001 >nul 2>&1')
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import subprocess
# re removed (unused)
import json
import psutil
import socket
try:
    import nmap
    NMAP_AVAILABLE = True
except ImportError:
    NMAP_AVAILABLE = False
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Tuple, Optional, Set
from abc import ABC, abstractmethod
from pathlib import Path


# ============================================================================
# ASCII ART - ESCUDO Y ESPADA
# ============================================================================
BANNER = r"""
╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║               ███████╗███████╗ ██████╗██╗   ██╗██████╗ ██╗   ██╗          ║
║               ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗╚██╗ ██╔╝          ║
║               ███████╗█████╗  ██║     ██║   ██║██████╔╝ ╚████╔╝           ║
║               ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗  ╚██╔╝            ║
║               ███████║███████╗╚██████╗╚██████╔╝██║  ██║   ██║             ║
║               ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝             ║
║                                                                            ║
║                     [*] SEKURY NETSUITE PRO [*]                            ║
║                       Análisis Profesional de Red                         ║
║                    Protección Contra Amenazas Cibernéticas               ║
║                            Autor: @CEKRO                                 ║
║                                                                            ║
║                ╔══════════════════════════════════════════╗               ║
║                ║  Versión 3.0 - SEKURY + NETMAPPER CK    ║               ║
║                ║     Seguridad Local + Escaneo Nmap      ║               ║
║                ╚══════════════════════════════════════════╝               ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""

MAIN_MENU = r"""
╔════════════════════════════════════╗
║           MENÚ PRINCIPAL           ║
╠════════════════════════════════════╣
║ 1. Escanear todas las conexiones   ║
║ 2. Ver conexiones sospechosas      ║
║ 3. Análisis rápido                 ║
║ 4. Ayuda                           ║
║ A. Ejecutar todo (silencioso)      ║
║ 5. Panel de amenazas               ║
║ 6. Agregar IP a lista blanca       ║
║ 7. Ver procesos de alto riesgo     ║
║ 8. Estado del sistema              ║
║ 9. NETMAPPER (Nmap)                ║
║ 0. Salir                           ║
╚════════════════════════════════════╝
"""

NETMAPPER_MENU = r"""
╔════════════════════════════════════╗
║            NETMAPPER CK            ║
╠════════════════════════════════════╣
║ 1. Escaneo rápido de puertos       ║
║ 2. Escaneo con detección de SO     ║
║ 3. Versiones de servicios          ║
║ 4. Vulnerabilidades conocidas      ║
║ A. Análisis completo (localhost)   ║
║ 5. Exportar último reporte         ║
║ 6. Ver configuración               ║
║ 0. Volver                          ║
╚════════════════════════════════════╝
"""

SWORD = r"""
    [>>]═══════════════════════════[>>]
       ANÁLISIS COMPLETADO
    [>>]═══════════════════════════[>>]
"""

SHIELD = r"""
    [SH]═══════════════════════════[SH]
       SISTEMA PROTEGIDO
    [SH]═══════════════════════════[SH]
"""

NMAP_CONFIG = {
    'default_ports': '1-1000',
    'timeout': 300,
    'output_dir': Path.home() / 'NetMapperCK_Reports',
}


SUCCESS_BANNER = r"""
[OK] ╔═══════════════════════════════════════════════════════════════╗
     ║  [OK] ANÁLISIS COMPLETADO CORRECTAMENTE                      ║
     ║  [OK] Reporte generado: netstat_security_report.json         ║
     ║  [OK] Presione Enter para volver al menú...                  ║
     ╚═══════════════════════════════════════════════════════════════╝
"""

WARNING_BANNER = r"""
[!] ╔═══════════════════════════════════════════════════════════════╗
    ║  [!] CONEXIONES SOSPECHOSAS DETECTADAS                       ║
    ║  Revise la lista de amenazas a continuación                  ║
    ║  Se recomienda investigación y acción inmediata              ║
    ╚═══════════════════════════════════════════════════════════════╝
"""


# ============================================================================
# DATOS DE CONFIGURACIÓN SEGURA
# ============================================================================

# Puertos y servicios conocidos y seguros
SAFE_PORTS = {
    80: "HTTP",
    443: "HTTPS",
    22: "SSH",
    21: "FTP",
    25: "SMTP",
    53: "DNS",
    110: "POP3",
    143: "IMAP",
    3306: "MySQL",
    5432: "PostgreSQL",
    5900: "VNC",
    3389: "RDP",
    8080: "HTTP Alt",
    8443: "HTTPS Alt",
    3000: "Dev Server",
    5000: "Dev Server",
    9000: "Dev Server",
    27017: "MongoDB",
    6379: "Redis",
    5984: "CouchDB",
}

# Direcciones IP conocidas y seguras
SAFE_IPS = {
    "127.0.0.1",
    "::1",
    "localhost",
}

# IPs privadas (redes internas)
PRIVATE_NETWORKS = [
    "10.",
    "172.16.", "172.17.", "172.18.", "172.19.", "172.20.", "172.21.", "172.22.", "172.23.",
    "172.24.", "172.25.", "172.26.", "172.27.", "172.28.", "172.29.", "172.30.", "172.31.",
    "192.168.",
    "169.254.",
]

# Puertos sospechosos comúnmente usados por malware
SUSPICIOUS_PORTS = {
    4444: "Potencial puerta trasera",
    5555: "Potencial puerta trasera",
    6666: "Potencial IRC/Botnet",
    6667: "IRC - Botnet",
    7777: "Potencial puerta trasera",
    8888: "Potencial puerta trasera",
    9999: "Potencial puerta trasera",
    31337: "BackOrifice (clásico)",
    12345: "NetBUS",
    27374: "Trojan.Generic",
    2222: "SSH alternativo sospechoso",
    1433: "MSSQL - Brute force",
    3389: "RDP - Acceso remoto sin autorizar",
    445: "SMB - Ransomware",
    139: "NetBIOS",
    23: "Telnet - Sin encriptación",
}

# Base de datos de IPs maliciosas conocidas (simplificada)
MALICIOUS_IPS = {
    # Botnets y servidores C&C conocidos
    "192.241.238.6": "Mirai Botnet C&C",
    "45.33.32.156": "Malware C&C",
    "5.188.7.0": "Malware distribuido",
}

# Procesos del sistema confiables
TRUSTED_PROCESSES = {
    "svchost.exe": "Windows Service Host",
    "lsass.exe": "Local Security Authority",
    "csrss.exe": "Client Server Runtime Process",
    "explorer.exe": "Windows Explorer",
    "winlogon.exe": "Windows Logon",
    "services.exe": "Services",
    "spoolsv.exe": "Print Spooler",
    "SearchIndexer.exe": "Windows Search",
}

# Procesos potencialmente peligrosos
SUSPICIOUS_PROCESSES = {
    "cmd.exe": "Command Prompt",
    "powershell.exe": "PowerShell",
    "regsvcs.exe": "Reg Services",
    "rundll32.exe": "DLL Runner",
    "wscript.exe": "Windows Script Host",
    "cscript.exe": "Command Script Host",
    "msiexec.exe": "MSI Installer",
    "schtasks.exe": "Task Scheduler",
}


# ============================================================================
# CLASES BASE Y ABSTRACTAS (para extensibilidad)
# ============================================================================

class AnalysisModule(ABC):
    """Clase base para módulos de análisis"""
    
    @abstractmethod
    def analyze(self, connection: Dict) -> Tuple[str, str]:
        """Analiza una conexión y retorna (categoría, razón)"""
        pass


class SafeConnectionAnalyzer(AnalysisModule):
    """Módulo: Identifica conexiones seguras"""
    
    def analyze(self, conn: Dict) -> Tuple[str, str]:
        remote_ip = conn['remote_ip']
        remote_port = conn['remote_port']
        
        # Conexiones locales
        if remote_ip in SAFE_IPS or remote_ip.startswith("127."):
            return "SAFE", "Conexión local (localhost)"
        
        # IPs privadas
        for private_net in PRIVATE_NETWORKS:
            if remote_ip.startswith(private_net):
                return "SAFE", f"IP privada ({private_net}*)"
        
        # Puertos seguros
        try:
            port = int(remote_port)
            if port in SAFE_PORTS:
                return "SAFE", f"Puerto seguro: {SAFE_PORTS[port]}"
        except ValueError:
            pass
        
        return "UNKNOWN", ""


class SuspiciousConnectionAnalyzer(AnalysisModule):
    """Módulo: Identifica conexiones sospechosas"""
    
    def analyze(self, conn: Dict) -> Tuple[str, str]:
        remote_port = conn['remote_port']
        remote_ip = conn['remote_ip']
        
        # Verificar si la IP está en lista negra
        if remote_ip in MALICIOUS_IPS:
            return "SUSPICIOUS", f"🚨 IP MALICIOSA CONOCIDA: {MALICIOUS_IPS[remote_ip]}"
        
        try:
            port = int(remote_port)
            if port in SUSPICIOUS_PORTS:
                return "SUSPICIOUS", f"⚠️ Puerto sospechoso: {SUSPICIOUS_PORTS[port]}"
        except ValueError:
            pass
        
        # Conexiones extranjeras establecidas
        is_private = remote_ip in SAFE_IPS or remote_ip.startswith("127.")
        for private_net in PRIVATE_NETWORKS:
            is_private = is_private or remote_ip.startswith(private_net)
        
        if not is_private and conn['state'] == 'ESTABLISHED':
            return "SUSPICIOUS", "⚠️ Conexión ESTABLISHED con IP externa no catalogada"
        
        return "UNKNOWN", ""


class ProcessAnalyzer(AnalysisModule):
    """Módulo: Analiza procesos asociados a conexiones"""
    
    def analyze(self, conn: Dict) -> Tuple[str, str]:
        """Retorna información del proceso"""
        return "UNKNOWN", ""  # Solo para estructura, se usa directamente en el analizador
    
    def get_process_info(self, pid: str) -> Dict:
        """Obtiene información del proceso por PID - VERSIÓN CON PSUTIL"""
        try:
            pid_int = int(pid)
            process = psutil.Process(pid_int)
            return {
                'name': process.name(),
                'exe': process.exe(),
                'cmdline': ' '.join(process.cmdline()),
                'status': process.status(),
                'user': process.username(),
            }
        except (psutil.NoSuchProcess, psutil.AccessDenied, ValueError):
            return None
    
    def is_suspicious_process(self, process_name: str) -> Tuple[bool, str]:
        """Determina si un proceso es sospechoso"""
        process_lower = process_name.lower()
        
        if process_lower in [p.lower() for p in SUSPICIOUS_PROCESSES.keys()]:
            return True, f"Proceso potencialmente peligroso: {SUSPICIOUS_PROCESSES.get(process_name, 'Desconocido')}"
        
        return False, ""


class BehaviorAnalyzer(AnalysisModule):
    """Módulo: Analiza patrones de comportamiento sospechoso"""
    
    def analyze(self, conn: Dict) -> Tuple[str, str]:
        """Retorna información de comportamiento"""
        return "UNKNOWN", ""
    
    def detect_anomalies(self, connections: List[Dict]) -> Dict:
        """Detecta patrones anómalos en conexiones"""
        anomalies = {
            'excessive_connections': [],
            'rare_protocols': [],
            'pattern_changes': [],
        }
        
        # Contar conexiones por IP remota
        ip_counts = defaultdict(int)
        protocol_counts = defaultdict(int)
        
        for conn in connections:
            ip_counts[conn['remote_ip']] += 1
            protocol_counts[conn['protocol']] += 1
        
        # Detectar IPs con muchas conexiones
        for ip, count in ip_counts.items():
            if count > 10:
                anomalies['excessive_connections'].append({
                    'ip': ip,
                    'count': count,
                    'risk': 'ALTA' if count > 50 else 'MEDIA'
                })
        
        # Detectar protocolos inusuales
        for protocol, count in protocol_counts.items():
            if protocol not in ['TCP', 'UDP']:
                anomalies['rare_protocols'].append({
                    'protocol': protocol,
                    'count': count
                })
        
        return anomalies


# ============================================================================
# ANALIZADOR PRINCIPAL
# ============================================================================

class NetstatSecurityAnalyzer:
    """Herramienta principal de análisis de ciberseguridad local"""
    
    def __init__(self):
        self.connections = []
        self.safe_connections = []
        self.suspicious_connections = []
        self.unknown_connections = []
        self.risk_score = 0
        
        # Módulos de análisis (extensible)
        self.analyzers: List[AnalysisModule] = [
            SafeConnectionAnalyzer(),
            SuspiciousConnectionAnalyzer(),
        ]
        
        # Módulos especializados
        self.process_analyzer = ProcessAnalyzer()
        self.behavior_analyzer = BehaviorAnalyzer()
    
    def register_analyzer(self, analyzer: AnalysisModule):
        """Permite registrar nuevos módulos de análisis"""
        self.analyzers.append(analyzer)

    def run_scan(self) -> bool:
        """Ejecuta netstat, parsea y categoriza. Retorna True si hubo salida."""
        netstat_output = self.get_netstat_output()
        if not netstat_output:
            return False

        connections = self.parse_netstat(netstat_output)
        self.connections = connections
        self.categorize_connections(connections)
        return True
    
    def get_netstat_output(self) -> str:
        """Obtiene la salida del comando netstat"""
        try:
            result = subprocess.run(
                ['netstat', '-ano'],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout
        except Exception as e:
            print(f"❌ Error ejecutando netstat: {e}")
            return ""
    
    def parse_netstat(self, netstat_output: str) -> List[Dict]:
        """Parsea la salida de netstat en formato estructurado"""
        connections = []
        lines = netstat_output.split('\n')
        
        for line in lines[4:]:
            if not line.strip():
                continue
            
            parts = line.split()
            if len(parts) >= 4:
                try:
                    protocol = parts[0]
                    local = parts[1]
                    remote = parts[2]
                    state = parts[3] if len(parts) > 3 else "UNKNOWN"
                    pid = parts[-1] if len(parts) > 4 else "?"
                    
                    local_ip, local_port = self.extract_ip_port(local)
                    remote_ip, remote_port = self.extract_ip_port(remote)
                    
                    connections.append({
                        'protocol': protocol,
                        'local_ip': local_ip,
                        'local_port': local_port,
                        'remote_ip': remote_ip,
                        'remote_port': remote_port,
                        'state': state,
                        'pid': pid,
                        'raw': line.strip()
                    })
                except Exception:
                    continue
        
        return connections
    
    @staticmethod
    def extract_ip_port(address: str) -> Tuple[str, str]:
        """Extrae IP y puerto de una dirección"""
        if ':' in address:
            parts = address.rsplit(':', 1)
            return parts[0], parts[1]
        return address, "?"
    
    def categorize_connections(self, connections: List[Dict]):
        """Categoriza conexiones usando módulos de análisis"""
        # Resetear listas y puntuación para evitar acumulación entre escaneos
        self.safe_connections = []
        self.suspicious_connections = []
        self.unknown_connections = []
        self.risk_score = 0

        for conn in connections:
            categorized = False
            
            for analyzer in self.analyzers:
                category, reason = analyzer.analyze(conn)
                
                if category == "SAFE":
                    conn['category'] = "SAFE"
                    conn['reason'] = reason
                    self.safe_connections.append(conn)
                    categorized = True
                    break
                elif category == "SUSPICIOUS":
                    conn['category'] = "SUSPICIOUS"
                    conn['reason'] = reason
                    
                    # Obtener info del proceso
                    process_info = self.process_analyzer.get_process_info(conn['pid'])
                    conn['process'] = process_info
                    
                    # Calcular riesgo
                    conn['risk_level'] = self._calculate_risk_level(conn, process_info)
                    self.risk_score += self._get_risk_points(conn['risk_level'])
                    
                    self.suspicious_connections.append(conn)
                    categorized = True
                    break
            
            if not categorized:
                conn['category'] = "UNKNOWN"
                conn['reason'] = "Requiere verificación manual"
                
                # Obtener info del proceso incluso para desconocidas
                process_info = self.process_analyzer.get_process_info(conn['pid'])
                conn['process'] = process_info
                
                self.unknown_connections.append(conn)
    
    def _calculate_risk_level(self, conn: Dict, process_info: Optional[Dict]) -> str:
        """Calcula el nivel de riesgo de una conexión"""
        risk_points = 0
        
        # Puntos por puerto
        try:
            port = int(conn['remote_port'])
            if port in SUSPICIOUS_PORTS:
                risk_points += 30
        except ValueError:
            pass
        
        # Puntos por estado
        if conn['state'] == 'ESTABLISHED':
            risk_points += 20
        
        # Puntos por proceso
        if process_info:
            is_suspicious, _ = self.process_analyzer.is_suspicious_process(process_info['name'])
            if is_suspicious:
                risk_points += 25
        
        # Determinar nivel
        if risk_points >= 70:
            return "CRÍTICO"
        elif risk_points >= 50:
            return "ALTO"
        elif risk_points >= 30:
            return "MEDIO"
        else:
            return "BAJO"
    
    def _get_risk_points(self, risk_level: str) -> int:
        """Retorna puntos de riesgo por nivel"""
        levels = {
            "CRÍTICO": 50,
            "ALTO": 25,
            "MEDIO": 10,
            "BAJO": 1,
        }
        return levels.get(risk_level, 0)
    
    def print_banner(self):
        """Muestra el banner de inicio"""
        print(BANNER)
    
    def print_results(self):
        """Imprime los resultados de forma formateada"""
        print("\n" + "="*90)
        print("📊 ANÁLISIS DE NETSTAT - CATEGORIZACIÓN DE CONEXIONES")
        print("="*90)
        
        # Conexiones seguras
        print(f"\n✅ CONEXIONES SEGURAS ({len(self.safe_connections)})")
        print("-" * 90)
        if self.safe_connections:
            for conn in self.safe_connections[:10]:
                print(f"  {conn['remote_ip']:20} : {conn['remote_port']:6} "
                      f"({conn['state']:11}) | {conn['reason']}")
            if len(self.safe_connections) > 10:
                print(f"  ... y {len(self.safe_connections) - 10} más")
        else:
            print("  No hay conexiones seguras")
        
        # Conexiones sospechosas
        print(f"\n⚠️  CONEXIONES SOSPECHOSAS ({len(self.suspicious_connections)})")
        print("-" * 90)
        if self.suspicious_connections:
            for conn in sorted(self.suspicious_connections, key=lambda x: self._get_risk_priority(x.get('risk_level', 'BAJO')), reverse=True):
                risk_emoji = "🔴" if conn.get('risk_level') == 'CRÍTICO' else "🟠" if conn.get('risk_level') == 'ALTO' else "🟡"
                print(f"  {risk_emoji} [{conn.get('risk_level', 'DESCONOCIDO'):7}] {conn['remote_ip']:20} : {conn['remote_port']:6}")
                print(f"     ├─ Razón: {conn['reason']}")
                if conn['process']:
                    print(f"     ├─ Proceso: {conn['process']['name']} (PID: {conn['pid']})")
                    print(f"     └─ Usuario: {conn['process']['user']}")
                else:
                    print(f"     └─ PID: {conn['pid']} (Proceso inaccesible)")
        else:
            print("  ✓ No hay conexiones sospechosas detectadas")
        
        # Conexiones desconocidas
        print(f"\n❓ CONEXIONES DESCONOCIDAS ({len(self.unknown_connections)})")
        print("-" * 90)
        if self.unknown_connections:
            for conn in self.unknown_connections[:15]:
                process_name = conn['process']['name'] if conn['process'] else "Desconocido"
                print(f"  {conn['remote_ip']:20} : {conn['remote_port']:6} ({conn['state']:11}) | {process_name}")
            if len(self.unknown_connections) > 15:
                print(f"  ... y {len(self.unknown_connections) - 15} más")
        else:
            print("  No hay conexiones desconocidas")
        
        # Análisis de comportamiento
        self._print_behavior_analysis()
        
        # Resumen
        self._print_summary()
    
    def _print_behavior_analysis(self):
        """Imprime análisis de comportamiento anómalo"""
        anomalies = self.behavior_analyzer.detect_anomalies(self.connections)
        
        if any(anomalies.values()):
            print(f"\n🔍 ANÁLISIS DE COMPORTAMIENTO ANÓMALO")
            print("-" * 90)
            
            if anomalies['excessive_connections']:
                print("  📈 IPs con conexiones excesivas:")
                for item in anomalies['excessive_connections'][:5]:
                    print(f"     • {item['ip']}: {item['count']} conexiones (Riesgo: {item['risk']})")
            
            if anomalies['rare_protocols']:
                print("  📡 Protocolos inusuales detectados:")
                for item in anomalies['rare_protocols']:
                    print(f"     • {item['protocol']}: {item['count']} conexiones")
    
    def _print_summary(self):
        """Imprime resumen general"""
        print("\n" + "="*90)
        print("📈 RESUMEN GENERAL DE SEGURIDAD")
        print("="*90)
        total = len(self.safe_connections) + len(self.suspicious_connections) + len(self.unknown_connections)
        print(f"  Total de conexiones: {total}")
        print(f"  ✅ Seguras:        {len(self.safe_connections):5} ({self._percentage(len(self.safe_connections), total)}%)")
        print(f"  ⚠️  Sospechosas:    {len(self.suspicious_connections):5} ({self._percentage(len(self.suspicious_connections), total)}%)")
        print(f"  ❓ Desconocidas:   {len(self.unknown_connections):5} ({self._percentage(len(self.unknown_connections), total)}%)")
        
        # Puntuación de riesgo
        print(f"\n🎯 PUNTUACIÓN DE RIESGO: {self.risk_score}/100")
        if self.risk_score >= 70:
            print("   ⛔ RIESGO CRÍTICO - Se recomienda acción inmediata")
        elif self.risk_score >= 50:
            print("   🔴 RIESGO ALTO - Investigación urgente recomendada")
        elif self.risk_score >= 30:
            print("   🟠 RIESGO MEDIO - Monitoreo recomendado")
        else:
            print("   🟢 RIESGO BAJO - Sistema relativamente seguro")
        
        print("="*90 + "\n")
    
    def _get_risk_priority(self, risk_level: str) -> int:
        """Retorna prioridad para ordenamiento"""
        priority = {"CRÍTICO": 4, "ALTO": 3, "MEDIO": 2, "BAJO": 1}
        return priority.get(risk_level, 0)
    
    @staticmethod
    def _percentage(part: int, total: int) -> int:
        """Calcula porcentaje"""
        return int((part / total * 100)) if total > 0 else 0
    
    def export_report(self, filename: str = "netstat_report.json"):
        """Exporta reporte a JSON y retorna la ruta completa"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'risk_score': self.risk_score,
            'summary': {
                'total': len(self.connections),
                'safe': len(self.safe_connections),
                'suspicious': len(self.suspicious_connections),
                'unknown': len(self.unknown_connections),
            },
            'suspicious_connections': self.suspicious_connections,
            'high_risk_processes': self._get_high_risk_processes(),
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        full_path = Path(filename).resolve()
        print(f"✓ Reporte exportado a: {full_path}")
        return str(full_path)
    
    def _get_high_risk_processes(self) -> List[Dict]:
        """Extrae procesos de alto riesgo"""
        high_risk = []
        seen_pids = set()
        
        for conn in self.suspicious_connections:
            if conn['pid'] not in seen_pids and conn.get('process'):
                seen_pids.add(conn['pid'])
                high_risk.append({
                    'pid': conn['pid'],
                    'name': conn['process']['name'],
                    'exe': conn['process']['exe'],
                    'connections': sum(1 for c in self.suspicious_connections if c['pid'] == conn['pid']),
                    'risk_level': conn.get('risk_level', 'DESCONOCIDO'),
                })
        
        return sorted(high_risk, key=lambda x: x['connections'], reverse=True)


class NetmapperAnalyzer:
    """Módulo NETMAPPER integrado para escaneo de red con Nmap"""

    def __init__(self):
        self.nm = nmap.PortScanner() if NMAP_AVAILABLE else None
        self.last_scan_results = None
        self.last_host = None
        NMAP_CONFIG['output_dir'].mkdir(exist_ok=True)

    def _run_scan(self, host: str, arguments: str) -> bool:
        if not NMAP_AVAILABLE:
            print("❌ python-nmap no está disponible. Instala dependencias primero.")
            return False

        try:
            self.nm.scan(host, arguments=arguments)
            self.last_host = host
            self.last_scan_results = self.nm
            return True
        except Exception as e:
            print(f"❌ Error durante el escaneo Nmap: {e}")
            return False

    def quick_port_scan(self, host: str) -> bool:
        print("\n" + "=" * 90)
        print(f"🔍 ESCANEO RÁPIDO DE PUERTOS - {host}")
        print("=" * 90)
        if not self._run_scan(host, f'-p {NMAP_CONFIG["default_ports"]}'):
            return False
        self._print_scan_results()
        return True

    def os_detection_scan(self, host: str) -> bool:
        print("\n" + "=" * 90)
        print(f"🔍 ESCANEO CON DETECCIÓN DE SO - {host}")
        print("=" * 90)
        if not self._run_scan(host, f'-O -p {NMAP_CONFIG["default_ports"]}'):
            return False
        self._print_scan_results()
        self._print_os_detection()
        return True

    def service_version_scan(self, host: str) -> bool:
        print("\n" + "=" * 90)
        print(f"🔍 ESCANEO DE VERSIONES DE SERVICIOS - {host}")
        print("=" * 90)
        if not self._run_scan(host, f'-sV -p {NMAP_CONFIG["default_ports"]}'):
            return False
        self._print_scan_results_with_versions()
        return True

    def vulnerability_check(self, host: str) -> bool:
        print("\n" + "=" * 90)
        print(f"🔍 ANÁLISIS DE VULNERABILIDADES CONOCIDAS - {host}")
        print("=" * 90)
        if not self._run_scan(host, f'--script vuln -p {NMAP_CONFIG["default_ports"]}'):
            return False
        self._print_vulnerability_results()
        return True

    def _print_scan_results(self):
        if not self.last_scan_results:
            return

        for host in self.last_scan_results.all_hosts():
            print(f"\n📊 HOST: {host}")
            print(f"   Estado: {self.last_scan_results[host].state()}\n")

            for proto in self.last_scan_results[host].all_protocols():
                ports = self.last_scan_results[host][proto].keys()
                print(f"   Protocolo: {proto.upper()}")
                for port in sorted(ports):
                    state = self.last_scan_results[host][proto][port]['state']
                    print(f"     Puerto {port:5d}: {state:10s}")

    def _print_scan_results_with_versions(self):
        if not self.last_scan_results:
            return

        for host in self.last_scan_results.all_hosts():
            print(f"\n📊 HOST: {host}")
            print(f"   Estado: {self.last_scan_results[host].state()}\n")

            for proto in self.last_scan_results[host].all_protocols():
                ports = self.last_scan_results[host][proto].keys()
                for port in sorted(ports):
                    data = self.last_scan_results[host][proto][port]
                    state = data.get('state', 'unknown')
                    name = data.get('name', 'unknown')
                    product = data.get('product', '')
                    version = data.get('version', '')

                    service_info = f"{name}"
                    if product:
                        service_info += f" ({product} {version})"

                    print(f"   Puerto {port:5d}: {state:10s} - {service_info}")

    def _print_os_detection(self):
        if not self.last_scan_results:
            return

        for host in self.last_scan_results.all_hosts():
            if 'osmatch' in self.last_scan_results[host]:
                print("\n🖥️  DETECCIÓN DE SO:")
                for osmatch in self.last_scan_results[host]['osmatch']:
                    print(f"   • {osmatch['name']} ({osmatch['accuracy']}% confianza)")

    def _print_vulnerability_results(self):
        if not self.last_scan_results:
            return
        print("\n⚠️  ANÁLISIS DE VULNERABILIDADES:")
        print("   Escaneo NSE ejecutado para detección de CVEs conocidas.")

    def export_report(self, filename: str = None) -> bool:
        if not self.last_scan_results or not self.last_host:
            print("❌ No hay escaneo Nmap previo para exportar.")
            return False

        if not filename:
            filename = f"nmap_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        filepath = NMAP_CONFIG['output_dir'] / filename

        try:
            report = {
                'timestamp': datetime.now().isoformat(),
                'host': self.last_host,
                'scan_summary': str(self.last_scan_results.summarize()),
            }
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)

            print(f"✓ Reporte Nmap exportado a: {filepath}")
            return True
        except Exception as e:
            print(f"❌ Error exportando reporte Nmap: {e}")
            return False


def get_target_host() -> str:
    """Solicita host para escaneo Nmap"""
    while True:
        host = input("\n📍 Ingrese dirección IP o dominio a escanear: ").strip()
        if host:
            return host
        print("❌ Por favor ingrese un host válido")


def run_netmapper_silent(analyzer: NetmapperAnalyzer) -> bool:
    """Ejecuta escaneo Nmap completo en localhost sin prompts extra"""
    print("\n" + "=" * 90)
    print("🚀 INICIANDO ANÁLISIS NETMAPPER COMPLETO")
    print("=" * 90)

    host = "localhost"
    print(f"\n📍 Escaneando: {host}")

    if not analyzer.quick_port_scan(host):
        return False
    if not analyzer.os_detection_scan(host):
        return False
    if not analyzer.service_version_scan(host):
        return False

    analyzer.export_report()
    return True


def netmapper_menu(netmapper_analyzer: NetmapperAnalyzer):
    """Submenú NETMAPPER integrado"""
    if not NMAP_AVAILABLE:
        print("\n⚠️  python-nmap no está disponible.")
        print("Instala dependencias con install_dependencies.bat o pip install -r requirements.txt")
        input("\nPresione Enter para volver al menú...")
        return

    while True:
        print("\n" + NETMAPPER_MENU)
        choice = input("Ingrese su opción NETMAPPER (0-6 o A): ").strip().lower()

        if choice == '1':
            host = get_target_host()
            netmapper_analyzer.quick_port_scan(host)
            input("\nPresione Enter para continuar...")
        elif choice == '2':
            host = get_target_host()
            netmapper_analyzer.os_detection_scan(host)
            input("\nPresione Enter para continuar...")
        elif choice == '3':
            host = get_target_host()
            netmapper_analyzer.service_version_scan(host)
            input("\nPresione Enter para continuar...")
        elif choice == '4':
            host = get_target_host()
            netmapper_analyzer.vulnerability_check(host)
            input("\nPresione Enter para continuar...")
        elif choice == 'a':
            if run_netmapper_silent(netmapper_analyzer):
                print("\n✓ Análisis NETMAPPER completado.")
            input("Presione Enter para continuar...")
        elif choice == '5':
            netmapper_analyzer.export_report()
            input("\nPresione Enter para continuar...")
        elif choice == '6':
            print("\n⚙️  CONFIGURACIÓN NETMAPPER")
            print(f"   • Puertos por defecto: {NMAP_CONFIG['default_ports']}")
            print(f"   • Timeout: {NMAP_CONFIG['timeout']}s")
            print(f"   • Directorio reportes: {NMAP_CONFIG['output_dir']}")
            input("\nPresione Enter para continuar...")
        elif choice == '0':
            break
        else:
            print("❌ Opción inválida. Use 0-6 o A.")


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

# ============================================================================
# FUNCIÓN PRINCIPAL CON MENÚ INTERACTIVO
# ============================================================================

def show_help():
    """Muestra información de ayuda"""
    help_text = r"""
╔════════════════════════════════════════════════════════════════════════════╗
║                   📚 INFORMACIÓN DE AYUDA 📚                              ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║ ¿QUÉ HACE ESTE PROGRAMA?                                                  ║
║ • Analiza todas las conexiones de red activas en tu sistema              ║
║ • Clasifica conexiones como SEGURAS, SOSPECHOSAS o DESCONOCIDAS          ║
║ • Detecta procesos potencialmente maliciosos                             ║
║ • Calcula un nivel de riesgo para tu sistema                             ║
║ • Bloquea/desbloquea conexiones sospechosas                              ║
║ • Gestiona procesos maliciosos                                           ║
║ • Incluye NETMAPPER para escaneo con Nmap                                ║
║                                                                            ║
║ CATEGORÍAS DE CONEXIONES:                                                ║
║ ✅ SEGURAS      - Conexiones legítimas (localhost, IPs privadas, etc)    ║
║ ⚠️  SOSPECHOSAS - Posibles amenazas que requieren atención               ║
║ ❓ DESCONOCIDAS - Conexiones que requieren verificación manual           ║
║                                                                            ║
║ NIVELES DE RIESGO:                                                        ║
║ 🔴 CRÍTICO (70+) - Acción inmediata requerida                           ║
║ 🟠 ALTO (50+)    - Investigación urgente recomendada                    ║
║ 🟡 MEDIO (30+)   - Monitoreo recomendado                                ║
║ 🟢 BAJO (<30)    - Sistema relativamente seguro                         ║
║                                                                            ║
║ OPCIONES DE GESTIÓN DE AMENAZAS:                                         ║
║ 🚫 Bloquear IP en Firewall - Evita conexiones de IPs maliciosas         ║
║ 🔓 Desbloquear IP - Revierte el bloqueo en caso de error                ║
║ ⛔ Terminar Proceso - Detiene procesos sospechosos                       ║
║ ⭕ Lista Blanca - Excepciona IPs confiables de análisis                  ║
║                                                                            ║
║ REQUISITOS:                                                               ║
║ • Python 3.7 o superior                                                  ║
║ • Ejecutar como Administrador para análisis completo                     ║
║ • Librerías: psutil, python-nmap                                         ║
║ • Nmap instalado en el sistema                                           ║
║                                                                            ║
║ ARCHIVOS GENERADOS:                                                       ║
║ • netstat_security_report.json - Reporte completo en formato JSON        ║
║ • whitelist.json - Lista de IPs permitidas                               ║
║ • %USERPROFILE%\NetMapperCK_Reports\*.json - Reportes Nmap              ║
║                                                                            ║
║ ⚠️  IMPORTANTE: Este programa incluye funciones de seguridad - úsalo      ║
║    con precaución y solo en sistemas donde tengas autorización           ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""
    print(help_text)
    input("Presione Enter para volver al menú...")


def confirm_scan():
    """Pide confirmación antes de ejecutar el escaneo"""
    confirm = r"""
╔════════════════════════════════════════════════════════════════════════════╗
║                     ⚠️  CONFIRMACIÓN DE ESCANEO ⚠️                         ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  Este programa va a:                                                      ║
║  • Analizar TODAS las conexiones de red activas                          ║
║  • Identificar procesos asociados                                        ║
║  • Detectar posibles amenazas de seguridad                               ║
║  • Generar un reporte detallado                                          ║
║                                                                            ║
║  ✅ NO modifica nada del sistema - Solo analiza y reporta                ║
║  ✅ Es completamente seguro ejecutarlo                                   ║
║                                                                            ║
║  Esto puede tomar unos segundos...                                        ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""
    print(confirm)
    response = input("¿Deseas continuar con el escaneo? (S/N): ").strip().upper()
    return response == 'S'


def ask_export(analyzer: NetstatSecurityAnalyzer):
    """Pregunta si el usuario quiere exportar el reporte"""
    export_prompt = r"""
╔════════════════════════════════════════════════════════════════════════════╗
║                    💾 ¿EXPORTAR REPORTE EN JSON? 💾                       ║
╠════════════════════════════════════════════════════════════════════════════╣
║                                                                            ║
║  El reporte incluirá:                                                     ║
║  • Todas las conexiones analizadas                                        ║
║  • Conexiones sospechosas con detalles                                    ║
║  • Procesos de alto riesgo identificados                                  ║
║  • Puntuación de riesgo general                                           ║
║  • Timestamp del análisis                                                 ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝
"""
    print(export_prompt)
    response = input("¿Deseas guardar el reporte? (S/N): ").strip().upper()
    
    if response == 'S':
        full_path = analyzer.export_report("netstat_security_report.json")
        print(SUCCESS_BANNER)
        print(f"\n📁 Ruta del archivo: {full_path}")


def quick_scan(analyzer: NetstatSecurityAnalyzer):
    """Realiza un escaneo rápido sin mostrar todos los detalles"""
    if not confirm_scan():
        print("❌ Escaneo cancelado.")
        return
    
    print("\n🔍 Escaneando (modo rápido)...\n")
    if not analyzer.run_scan():
        print("❌ No se pudo obtener la salida de netstat")
        print("💡 Asegúrate de ejecutar este script como Administrador")
        return
    
    print("📊 RESUMEN RÁPIDO")
    print("=" * 90)
    total = len(analyzer.safe_connections) + len(analyzer.suspicious_connections) + len(analyzer.unknown_connections)
    print(f"Total de conexiones: {total}")
    print(f"✅ Seguras:        {len(analyzer.safe_connections):5}")
    print(f"⚠️  Sospechosas:    {len(analyzer.suspicious_connections):5} ⚠️")
    print(f"❓ Desconocidas:   {len(analyzer.unknown_connections):5}")
    print(f"\n🎯 NIVEL DE RIESGO GENERAL: {analyzer.risk_score}/100")
    
    if analyzer.risk_score >= 70:
        print("⛔ RIESGO CRÍTICO")
    elif analyzer.risk_score >= 50:
        print("🔴 RIESGO ALTO")
    elif analyzer.risk_score >= 30:
        print("🟠 RIESGO MEDIO")
    else:
        print("🟢 RIESGO BAJO")
    
    print("=" * 90)
    
    # Preguntar si exportar
    ask_export(analyzer)
    input("\nPresione Enter para volver al menú...")


def full_scan(analyzer: NetstatSecurityAnalyzer):
    """Realiza un escaneo completo con todos los detalles"""
    if not confirm_scan():
        print("❌ Escaneo cancelado.")
        return
    
    print("\n🔍 Escaneando conexiones de red...\n")
    if not analyzer.run_scan():
        print("❌ No se pudo obtener la salida de netstat")
        print("💡 Asegúrate de ejecutar este script como Administrador")
        return

    print(f"✓ Se encontraron {len(analyzer.connections)} conexiones\n")
    
    analyzer.print_results()
    
    if analyzer.suspicious_connections:
        print(WARNING_BANNER)
    
    print(SWORD)
    
    # Preguntar si exportar
    ask_export(analyzer)
    input("\nPresione Enter para volver al menú...")


def suspicious_only(analyzer: NetstatSecurityAnalyzer):
    """Muestra solo las conexiones sospechosas"""
    if not confirm_scan():
        print("❌ Escaneo cancelado.")
        return
    
    print("\n🔍 Escaneando...\n")
    if not analyzer.run_scan():
        print("❌ No se pudo obtener la salida de netstat")
        return
    
    print("\n" + "=" * 90)
    print("⚠️  CONEXIONES SOSPECHOSAS ÚNICAMENTE")
    print("=" * 90)
    
    if analyzer.suspicious_connections:
        for conn in sorted(analyzer.suspicious_connections, key=lambda x: analyzer._get_risk_priority(x.get('risk_level', 'BAJO')), reverse=True):
            risk_emoji = "🔴" if conn.get('risk_level') == 'CRÍTICO' else "🟠" if conn.get('risk_level') == 'ALTO' else "🟡"
            print(f"\n{risk_emoji} [{conn.get('risk_level', 'DESCONOCIDO'):7}] {conn['remote_ip']:20} : {conn['remote_port']:6}")
            print(f"   Razón: {conn['reason']}")
            if conn['process']:
                print(f"   Proceso: {conn['process']['name']} (PID: {conn['pid']})")
    else:
        print("✓ ¡Excelente! No hay conexiones sospechosas detectadas.")
    
    print("\n" + "=" * 90)
    
    # Preguntar si exportar
    ask_export(analyzer)
    input("Presione Enter para volver al menú...")


def block_ip_firewall(ip: str, port: str = None):
    """Bloquea una IP en el firewall de Windows"""
    try:
        rule_name = f"SEGURIDAD_BLOCK_{ip}_{port if port else 'ALL'}"
        
        if port:
            cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block protocol=tcp remoteip={ip} remoteport={port}'
        else:
            cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={ip}'
        
        subprocess.run(cmd, shell=True, capture_output=True, check=False)
        print(f"✅ Regla de bloqueo creada: {rule_name}")
        return True
    except Exception as e:
        print(f"❌ Error al crear regla de bloqueo: {e}")
        return False


def unblock_ip_firewall(ip: str, port: str = None):
    """Desbloquea una IP en el firewall de Windows"""
    try:
        rule_name = f"SEGURIDAD_BLOCK_{ip}_{port if port else 'ALL'}"
        cmd = f'netsh advfirewall firewall delete rule name="{rule_name}"'
        
        result = subprocess.run(cmd, shell=True, capture_output=True, check=False)
        if result.returncode == 0:
            print(f"✅ Regla de desbloqueo eliminada: {rule_name}")
            return True
        else:
            print(f"⚠️  No se encontró la regla: {rule_name}")
            return False
    except Exception as e:
        print(f"❌ Error al desbloquear: {e}")
        return False


def kill_suspicious_process(pid: int, process_name: str):
    """Termina un proceso sospechoso"""
    try:
        print(f"\n⚠️  CONFIRMACIÓN REQUERIDA")
        print(f"Proceso: {process_name} (PID: {pid})")
        response = input("¿Estás seguro de que deseas terminar este proceso? (S/N): ").strip().upper()
        
        if response == 'S':
            try:
                ps = psutil.Process(int(pid))
                ps.terminate()
            except (psutil.NoSuchProcess, ValueError, psutil.AccessDenied) as e:
                print(f"❌ No se pudo terminar el proceso: {e}")
                return False
            print(f"✅ Proceso terminado: {process_name} (PID: {pid})")
            return True
        else:
            print("❌ Operación cancelada")
            return False
    except Exception as e:
        print(f"❌ Error al terminar proceso: {e}")
        return False


def ping_ip(ip: str, timeout: int = 1000) -> bool:
    """Hace ping a una IP (Windows) y retorna True si responde."""
    try:
        # -n 1 ping uno solo, -w timeout en ms
        result = subprocess.run(["ping", "-n", "1", "-w", str(timeout), ip], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False


def resolve_hostname(ip: str) -> str:
    """Intenta resolver el nombre de host inverso para una IP."""
    try:
        host, _, _ = socket.gethostbyaddr(ip)
        return host
    except Exception:
        return "Desconocido"


def port_probe(ip: str, port: int, timeout: float = 1.0) -> bool:
    """Intenta conectar a una IP:port, retorna True si el puerto está abierto."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip, int(port)))
            return result == 0
    except Exception:
        return False


def scan_common_ports(ip: str, ports: List[int] = None) -> List[int]:
    """Escanea puertos comunes y retorna la lista de abiertos."""
    if ports is None:
        ports = [21, 22, 23, 80, 443, 445, 3306, 5432, 3389, 8080, 6379]
    open_ports = []
    for p in ports:
        if port_probe(ip, p, timeout=0.8):
            open_ports.append(p)
    return open_ports


def threat_management_panel(analyzer: NetstatSecurityAnalyzer):
    """Panel de control para gestionar amenazas detectadas"""
    if not analyzer.suspicious_connections:
        print("✓ No hay amenazas detectadas actualmente")
        print("Ejecute un escaneo primero para detectar amenazas")
        input("Presione Enter para continuar...")
        return
    
    while True:
        print("\n" + "=" * 90)
        print("🛡️  PANEL DE CONTROL DE AMENAZAS")
        print("=" * 90)
        print(f"\n⚠️  Amenazas detectadas: {len(analyzer.suspicious_connections)}\n")
        
        # Mostrar las amenazas
        for idx, conn in enumerate(sorted(analyzer.suspicious_connections, key=lambda x: analyzer._get_risk_priority(x.get('risk_level', 'BAJO')), reverse=True)[:10], 1):
            risk_emoji = "🔴" if conn.get('risk_level') == 'CRÍTICO' else "🟠" if conn.get('risk_level') == 'ALTO' else "🟡"
            print(f"{idx}. {risk_emoji} {conn['remote_ip']:20} : {conn['remote_port']:6} - {conn.get('reason', 'Desconocida')[:40]}")
        
        print("\n" + "-" * 90)
        print("0. Volver al menú principal")
        print("\nOpciones: Ingrese el número de la amenaza para acciones específicas")
        
        choice = input("\nSeleccione una amenaza (0-{0}): ".format(len(analyzer.suspicious_connections[:10]))).strip()
        
        if choice == '0':
            break
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(analyzer.suspicious_connections[:10]):
                threat = sorted(analyzer.suspicious_connections, key=lambda x: analyzer._get_risk_priority(x.get('risk_level', 'BAJO')), reverse=True)[idx]
                
                print("\n" + "=" * 90)
                print(f"🎯 DETALLES DE LA AMENAZA")
                print("=" * 90)
                print(f"IP Remota: {threat['remote_ip']}")
                print(f"Puerto: {threat['remote_port']}")
                print(f"Estado: {threat.get('state', 'DESCONOCIDO')}")
                print(f"Razón: {threat['reason']}")
                print(f"Nivel de Riesgo: {threat.get('risk_level', 'DESCONOCIDO')}")
                if threat.get('process'):
                    print(f"Proceso: {threat['process']['name']} (PID: {threat['pid']})")
                
                print("\n" + "-" * 90)
                print("¿Qué deseas hacer?")
                print("1. 🚫 Bloquear IP en Firewall")
                print("2. 🔓 Desbloquear IP (si estaba bloqueada)")
                print("3. ⛔ Terminar Proceso Asociado")
                print("4. ⭕ Agregar a Lista Blanca (Excepcionar)")
                print("5. 🔎 Más detalles (Ping / Reverse DNS)")
                print("0. Volver")
                
                action = input("Seleccione acción: ").strip()
                
                if action == '1':
                    block_ip_firewall(threat['remote_ip'], threat['remote_port'])
                elif action == '2':
                    unblock_ip_firewall(threat['remote_ip'], threat['remote_port'])
                elif action == '3':
                    if threat.get('process') and threat.get('pid'):
                        kill_suspicious_process(threat['pid'], threat['process']['name'])
                elif action == '4':
                    add_to_whitelist(threat['remote_ip'])
                elif action == '5':
                    ip = threat['remote_ip']
                    print(f"\n🔎 Detalles para {ip}")
                    host = resolve_hostname(ip)
                    print(f"   Host inverso: {host}")
                    print("   Haciendo ping (timeout 1s)...")
                    alive = ping_ip(ip, timeout=1000)
                    print(f"   Ping exitoso: {'SÍ' if alive else 'NO'}")
                elif action == '0':
                    continue
                else:
                    print("❌ Opción inválida")
                
                input("Presione Enter para continuar...")
            else:
                print("❌ Opción inválida")
        except ValueError:
            print("❌ Por favor ingrese un número válido")


def add_to_whitelist(ip: str):
    """Agrega una IP a la lista blanca"""
    try:
        whitelist_file = "whitelist.json"
        
        # Cargar lista existente
        try:
            with open(whitelist_file, 'r') as f:
                whitelist = json.load(f)
        except:
            whitelist = {"ips": [], "ports": []}
        
        if ip not in whitelist["ips"]:
            whitelist["ips"].append(ip)
            
            with open(whitelist_file, 'w') as f:
                json.dump(whitelist, f, indent=2)
            
            print(f"✅ IP agregada a lista blanca: {ip}")
        else:
            print(f"⚠️  IP ya está en la lista blanca: {ip}")
        
        return True
    except Exception as e:
        print(f"❌ Error al agregar a lista blanca: {e}")
        return False


def view_high_risk_processes(analyzer: NetstatSecurityAnalyzer):
    """Muestra procesos activos de alto riesgo"""
    if not analyzer.suspicious_connections:
        print("✓ No hay procesos de alto riesgo detectados")
        input("Presione Enter para continuar...")
        return
    
    print("\n" + "=" * 90)
    print("⚠️  PROCESOS ACTIVOS DE ALTO RIESGO")
    print("=" * 90)
    
    # Agrupar por proceso
    processes_dict = defaultdict(list)
    for conn in analyzer.suspicious_connections:
        if conn.get('process'):
            proc_name = conn['process']['name']
            processes_dict[proc_name].append(conn)
    
    for idx, (proc_name, conns) in enumerate(processes_dict.items(), 1):
        risk_level = max([conn.get('risk_level', 'BAJO') for conn in conns])
        print(f"\n{idx}. {proc_name} (PID: {conns[0].get('pid', 'DESCONOCIDO')})")
        print(f"   Nivel de Riesgo: {risk_level}")
        print(f"   Conexiones Sospechosas: {len(conns)}")
        for conn in conns[:3]:
            print(f"   • {conn['remote_ip']}:{conn['remote_port']} - {conn.get('reason', 'Desconocida')[:50]}")
    
    print("\n" + "=" * 90)
    input("Presione Enter para volver al menú...")


def view_system_status(analyzer: NetstatSecurityAnalyzer):
    """Muestra estado y configuración del sistema"""
    print("\n" + "=" * 90)
    print("📊 ESTADO Y CONFIGURACIÓN DEL SISTEMA")
    print("=" * 90)
    
    print(f"\n🖥️  INFORMACIÓN GENERAL:")
    print(f"   Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        print(f"   Memoria RAM: {psutil.virtual_memory().percent}% en uso")
        print(f"   CPU: {psutil.cpu_percent(interval=1)}% en uso")
    except:
        pass
    
    print(f"\n🌐 CONEXIONES GLOBALES:")
    if analyzer.connections:
        total = len(analyzer.connections)
        safe = len(analyzer.safe_connections)
        suspicious = len(analyzer.suspicious_connections)
        unknown = len(analyzer.unknown_connections)
        print(f"   Total: {total}")
        print(f"   ✅ Seguras: {safe} ({safe*100//total if total > 0 else 0}%)")
        print(f"   ⚠️  Sospechosas: {suspicious} ({suspicious*100//total if total > 0 else 0}%)")
        print(f"   ❓ Desconocidas: {unknown} ({unknown*100//total if total > 0 else 0}%)")
        print(f"\n🎯 PUNTUACIÓN DE RIESGO: {analyzer.risk_score}/100")
    else:
        print("   Ejecute un escaneo primero para ver estadísticas")
    
    print("\n📋 LISTAS Y CONFIGURACIÓN:")
    
    # Ver lista blanca
    try:
        with open("whitelist.json", 'r') as f:
            whitelist = json.load(f)
            print(f"   IPs en Lista Blanca: {len(whitelist.get('ips', []))}")
            if whitelist.get('ips'):
                for ip in whitelist.get('ips', [])[:5]:
                    print(f"   • {ip}")
    except:
        print("   IPs en Lista Blanca: 0")
    
    print("\n" + "=" * 90)
    input("Presione Enter para volver al menú...")


def interactive_menu():
    """Menú interactivo principal"""
    analyzer = NetstatSecurityAnalyzer()
    netmapper_analyzer = NetmapperAnalyzer()
    
    while True:
        print("\n" * 2)
        print(BANNER)
        print(MAIN_MENU)
        
        choice = input("Ingrese su opción (0-9 o A): ").strip()
        
        if choice == '1':
            full_scan(analyzer)
        elif choice == '2':
            suspicious_only(analyzer)
        elif choice == '3':
            quick_scan(analyzer)
        elif choice == '4':
            show_help()
        elif choice.lower() == 'a':
            # Opción automática silenciosa
            success = run_all_silent(analyzer)
            if success:
                print("\nAnálisis silencioso completado. Regresando al menú...")
        elif choice == '5':
            threat_management_panel(analyzer)
        elif choice == '6':
            ip_to_add = input("Ingrese la IP a agregar a lista blanca: ").strip()
            if ip_to_add:
                add_to_whitelist(ip_to_add)
            input("Presione Enter para continuar...")
        elif choice == '7':
            view_high_risk_processes(analyzer)
        elif choice == '8':
            view_system_status(analyzer)
        elif choice == '9':
            netmapper_menu(netmapper_analyzer)
        elif choice == '0':
            print("\n" + "=" * 90)
            print("👋 ¡Gracias por usar SEKURY NETSUITE!")
            print("Programa finalizado correctamente.")
            print("=" * 90 + "\n")
            break
        else:
            print("❌ Opción inválida. Por favor, ingrese un número del 0 al 9.")
            input("Presione Enter para continuar...")


def run_all_silent(analyzer: NetstatSecurityAnalyzer):
    """Ejecuta el análisis completo en modo silencioso (sin pausas ni prompts).
    Diseñado para uso automatizado: no solicita confirmaciones ni espera input.
    """
    # Mismos pasos que run_all_automated pero sin prompts ni mensajes que requieran Enter
    try:
        if not analyzer.run_scan():
            return False

        analyzer.print_results()

        # Exportar reporte sin preguntar
        analyzer.export_report("netstat_security_report.json")
        return True
    except Exception:
        return False


def main():
    """Función principal del programa"""
    interactive_menu()


if __name__ == "__main__":
    main()
