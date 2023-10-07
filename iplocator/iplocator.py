import requests
import webbrowser
import socket
import sys

def get_public_ip(domain_name):
    try:
        ip_address = socket.gethostbyname(domain_name)
        return ip_address
    except socket.gaierror:
        return None

def iplocate(ip):
    ipinfo = {}
    url = "http://ip-api.com/json/" + ip
    r = requests.get(url)
    ipinfo = r.json()

    if ipinfo['status'] == 'success':
        lat = ipinfo['lat']
        lon = ipinfo['lon']
        result = []
        print("                            ")
        result.append("IP Location Found !!")
        result.append('Country     :' + ipinfo['country'])
        result.append('Region Name :' + ipinfo['regionName'])
        result.append('City        :' + ipinfo['city'])
        result.append('Time zone   :' + ipinfo['timezone'])
        result.append('ISP         :' + ipinfo['isp'])
        
        mapurl = "https://maps.google.com/maps?q=%s,+%s" % (lat, lon)
        result.append('Opening Location in browser: ' + mapurl)
        return '\n'.join(result)
    else:
        return "IP Location Not Found !!"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 iplocator.py <domain_name>")
        sys.exit(1)

    domain_name = sys.argv[1]
    ip_address = get_public_ip(domain_name)
    
    if ip_address:
        result = iplocate(ip_address)
        print(result)
    else:
        print("Domain name could not be resolved to an IP address.")
        print("Enter a domain name for example: www.example.com")
