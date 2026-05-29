"""
Sentinel Red Team - Reconnaissance Module
Network and service discovery capabilities
"""

import subprocess
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
import xml.etree.ElementTree as ET


@dataclass
class HostInfo:
    """Information about a discovered host"""
    ip: str
    hostname: Optional[str]
    os: Optional[str]
    ports: List[Dict]
    services: List[Dict]


class ReconModule:
    """
    Reconnaissance and discovery module
    Integrates with nmap and custom scanning tools
    """
    
    def __init__(self, config: Dict):
        self.config = config
        self.nmap_path = config['tools']['nmap'].get('path', '/usr/bin/nmap')
        self.max_rate = config['tools']['nmap'].get('max_rate', 1000)
    
    def ping_sweep(self, target: str) -> List[str]:
        """
        Perform ping sweep to discover live hosts
        
        Args:
            target: IP range (e.g., '192.168.1.0/24')
        
        Returns:
            List of live IPs
        """
        print(f"[*] Performing ping sweep on {target}")
        
        try:
            # Use nmap for ping sweep
            cmd = [
                self.nmap_path,
                '-sn',  # Ping scan only
                '-T4',  # Timing template
                '--max-rate', str(self.max_rate),
                target
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # Parse output for live hosts
            live_hosts = []
            for line in result.stdout.split('\n'):
                if 'Nmap scan report for' in line:
                    ip = line.split()[-1].strip('()')
                    live_hosts.append(ip)
            
            print(f"[+] Found {len(live_hosts)} live hosts")
            return live_hosts
            
        except subprocess.TimeoutExpired:
            print("[!] Scan timed out")
            return []
        except Exception as e:
            print(f"[!] Error during ping sweep: {e}")
            return []
    
    def port_scan(self, target: str, ports: str = 'common') -> Dict:
        """
        Perform port scan on target
        
        Args:
            target: IP or hostname
            ports: 'common', 'all', or specific ports (e.g., '80,443,8080')
        
        Returns:
            Scan results dictionary
        """
        print(f"[*] Scanning ports on {target}")
        
        # Determine port range
        if ports == 'common':
            port_arg = '--top-ports=1000'
        elif ports == 'all':
            port_arg = '-p-'
        else:
            port_arg = f'-p {ports}'
        
        try:
            # Build nmap command
            cmd = [
                self.nmap_path,
                '-sV',  # Version detection
                '-sC',  # Default scripts
                '-T4',  # Timing
                '--max-rate', str(self.max_rate),
                port_arg,
                '-oX', '-',  # XML output to stdout
                target
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            # Parse XML output
            scan_results = self._parse_nmap_xml(result.stdout)
            
            print(f"[+] Scan complete: {len(scan_results.get('ports', []))} ports open")
            return scan_results
            
        except subprocess.TimeoutExpired:
            print("[!] Scan timed out")
            return {}
        except Exception as e:
            print(f"[!] Error during port scan: {e}")
            return {}
    
    def _parse_nmap_xml(self, xml_output: str) -> Dict:
        """Parse nmap XML output"""
        try:
            root = ET.fromstring(xml_output)
            
            results = {
                'host': '',
                'hostname': '',
                'os': '',
                'ports': [],
                'services': []
            }
            
            # Parse host information
            host = root.find('.//host')
            if host is None:
                return results
            
            # Get IP address
            address = host.find('.//address[@addrtype="ipv4"]')
            if address is not None:
                results['host'] = address.get('addr', '')
            
            # Get hostname
            hostname = host.find('.//hostname')
            if hostname is not None:
                results['hostname'] = hostname.get('name', '')
            
            # Get OS information
            os_match = host.find('.//osmatch')
            if os_match is not None:
                results['os'] = os_match.get('name', '')
            
            # Parse ports
            for port in host.findall('.//port'):
                port_id = port.get('portid')
                protocol = port.get('protocol')
                
                state = port.find('.//state')
                if state is None or state.get('state') != 'open':
                    continue
                
                service = port.find('.//service')
                service_name = service.get('name', 'unknown') if service is not None else 'unknown'
                service_version = service.get('version', '') if service is not None else ''
                
                port_info = {
                    'port': port_id,
                    'protocol': protocol,
                    'state': 'open',
                    'service': service_name,
                    'version': service_version
                }
                
                results['ports'].append(port_info)
                results['services'].append({
                    'name': service_name,
                    'version': service_version,
                    'port': port_id
                })
            
            return results
            
        except Exception as e:
            print(f"[!] Error parsing nmap XML: {e}")
            return {}
    
    def service_enumeration(self, target: str, port: int, service: str) -> Dict:
        """
        Enumerate specific service for vulnerabilities
        
        Args:
            target: IP or hostname
            port: Port number
            service: Service name (http, ssh, smb, etc.)
        
        Returns:
            Enumeration results
        """
        print(f"[*] Enumerating {service} on {target}:{port}")
        
        results = {
            'service': service,
            'port': port,
            'findings': []
        }
        
        try:
            # Use nmap NSE scripts for enumeration
            script_name = self._get_nse_script(service)
            
            if script_name:
                cmd = [
                    self.nmap_path,
                    '-p', str(port),
                    '--script', script_name,
                    target
                ]
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                results['raw_output'] = result.stdout
                results['findings'] = self._parse_script_output(result.stdout)
            
            return results
            
        except Exception as e:
            print(f"[!] Error during service enumeration: {e}")
            return results
    
    def _get_nse_script(self, service: str) -> str:
        """Get appropriate NSE script for service"""
        script_map = {
            'http': 'http-enum,http-headers,http-methods,http-robots.txt',
            'https': 'ssl-cert,ssl-enum-ciphers,http-enum',
            'ssh': 'ssh-auth-methods,ssh-hostkey',
            'ftp': 'ftp-anon,ftp-bounce',
            'smb': 'smb-enum-shares,smb-os-discovery,smb-security-mode',
            'mysql': 'mysql-info,mysql-empty-password',
            'mssql': 'ms-sql-info,ms-sql-empty-password',
            'rdp': 'rdp-enum-encryption',
            'dns': 'dns-zone-transfer,dns-nsid'
        }
        return script_map.get(service.lower(), '')
    
    def _parse_script_output(self, output: str) -> List[str]:
        """Parse NSE script output for findings"""
        findings = []
        
        # Simple parsing - extract interesting lines
        for line in output.split('\n'):
            line = line.strip()
            if line.startswith('|'):
                findings.append(line)
        
        return findings
    
    def subdomain_enumeration(self, domain: str) -> List[str]:
        """
        Enumerate subdomains (passive)
        
        Args:
            domain: Target domain
        
        Returns:
            List of discovered subdomains
        """
        print(f"[*] Enumerating subdomains for {domain}")
        
        # TODO: Integrate with tools like:
        # - Amass
        # - Subfinder
        # - Certificate transparency logs
        
        subdomains = []
        
        # Placeholder for certificate transparency lookup
        # In production, query crt.sh or similar
        
        print(f"[+] Found {len(subdomains)} subdomains")
        return subdomains
    
    def generate_report(self, results: Dict) -> str:
        """Generate markdown report from scan results"""
        report = f"""# Reconnaissance Report

## Target: {results.get('host', 'Unknown')}
**Hostname:** {results.get('hostname', 'N/A')}
**OS:** {results.get('os', 'Unknown')}

## Open Ports

| Port | Protocol | Service | Version |
|------|----------|---------|---------|
"""
        
        for port in results.get('ports', []):
            report += f"| {port['port']} | {port['protocol']} | {port['service']} | {port['version']} |\n"
        
        report += "\n## Services Identified\n\n"
        for service in results.get('services', []):
            report += f"- **{service['name']}** (port {service['port']})\n"
            if service['version']:
                report += f"  - Version: {service['version']}\n"
        
        return report


# Example usage
if __name__ == "__main__":
    import yaml
    
    # Load config
    with open('../config/settings.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    # Initialize recon module
    recon = ReconModule(config)
    
    # Example: Scan localhost
    print("\n" + "="*60)
    print("Testing Reconnaissance Module")
    print("="*60 + "\n")
    
    target = "127.0.0.1"
    print(f"Target: {target}\n")
    
    # Port scan
    results = recon.port_scan(target, ports='80,443,8080')
    
    if results:
        print("\n" + recon.generate_report(results))
