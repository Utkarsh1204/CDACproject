import sys
import requests
from bs4 import BeautifulSoup

def Links(url):
    try:
        if url.startswith("http://") or url.startswith("https://"):
            pass
        else:
            url = 'https://' + url

        print('')
        print("[+] Fetching links.....")

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        for link in soup.find_all('a'):
            lin = link.get('href')
            if lin and lin.startswith('http'):
                print("[+]", lin)

        print("Fetched Successfully...")

    except Exception as e:
        print("Invalid Domain Error")
        print("Preferred Format: www.example.com")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    Links(url)
