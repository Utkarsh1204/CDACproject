import requests
import sys

def HostHeader(host):
    headers = {'Host': 'http://evil.com'}
    response = requests.get(host, headers=headers)

    if 'evil.com' in response.headers:
        print("                                   ")
        print("Vulnerable to Host Header Injection")
    else:
        print("                                       ")
        print("Not Vulnerable to Host header injection")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    if url.startswith('http://') or url.startswith('https://'):
        pass
    else:
        url = 'https://' + url
    HostHeader(url)
