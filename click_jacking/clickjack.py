import sys
import requests


def ClickJacking(host):
    try:
        if host.startswith('http://') or host.startswith('https://'):
            pass
        else:
            host = 'https://' + host
            response = requests.get(host)
            headers = response.headers

            if "X-Frame-Options" not in headers:
                print("                                     ")
                print("Website is vulnerable to ClickJacking")
            else:
                print("Website is not Vulnerable to ClickJacking")
    except Exception as e:
        print("Invalid URL: %s" % host)
        print("Please enter Valid URL")
        print("Preffered Format: www.example.com")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <URL>")
        sys.exit(1)

    host = sys.argv[1]
    ClickJacking(host)
