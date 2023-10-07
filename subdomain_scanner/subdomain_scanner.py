import sys
import requests
import re
from urllib.parse import urlparse
import urllib3


def validate_input(input_domain):
    if not re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', input_domain):
        print("Invalid format. Preferred format is 'example.com'")
        sys.exit(1)


def get_subdomains(url):
    domain = urlparse(url).netloc
    subdomains = set()

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    response = requests.get(url, verify=False)
    if response.status_code == 200:
        content = response.text
        pattern = r"https?://([^\s/$.?#]+)\." + re.escape(domain)
        matches = re.findall(pattern, content)

        for match in matches:
            subdomains.add(match)

    if subdomains:
        print("          ")
        print("Subdomains:")
        for subdomain in subdomains:
            print(subdomain)
    else:
        print("No subdomains found.")

    return subdomains


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <domain>")
        sys.exit(1)

    input_domain = sys.argv[1]
    validate_input(input_domain)

    url = 'https://' + input_domain
    get_subdomains(url)

