import nmap
import socket
import sys

def scan_network(target):
    host_list = []

    nmp = nmap.PortScanner()
    nmp.scan(hosts=target, arguments='-sn')

    for host in nmp.all_hosts():
        host_list.append(host)

    return host_list

def detect_os_version(target):
    nmp = nmap.PortScanner()

    resolved_ips = socket.gethostbyname_ex(target)[2]
    
    os_version = "Unknown OS"
    for ip in resolved_ips:
        try:
            nmp.scan(hosts=ip, arguments='-O')
            os_match = nmp[ip].get('osmatch', [])
            if os_match:
                os_version = os_match[0].get('name', 'Unknown OS')
                break
        except:
            pass

    return os_version

def scan_open_ports(target):
    nmp = nmap.PortScanner()
    nmp.scan(hosts=target, arguments='-T4 -p1-65535')

    open_ports = []
    for host in nmp.all_hosts():
        tcp_ports = nmp[host]['tcp']
        for port, port_info in tcp_ports.items():
            if port_info['state'] == 'open':
                open_ports.append(port)

    return open_ports

def main(target):
    print("[+] Initiating network scan for target: {}".format(target))

    live_hosts = scan_network(target)
    print("[+] Live hosts found: {}".format(', '.join(live_hosts)))

    os_version = detect_os_version(target)
    print("[+] Detected OS version of {}: {}".format(target, os_version))

    print("[+] Initiating port scan for target: {}".format(target))
    open_ports = scan_open_ports(target)
    if open_ports:
        print("[+] Open ports on {}: {}".format(target, ', '.join(map(str, open_ports))))
    else:
        print("[+] No open ports found on {}".format(target))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script_name.py target")
        sys.exit(1)
    
    target = sys.argv[1]
    main(target)