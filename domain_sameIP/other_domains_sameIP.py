import sys
from requests import get


def ReverseIP(host):
    lookup_url = 'https://api.hackertarget.com/reverseiplookup/?q=%s' % host

    try:
        response = get(lookup_url)

        if response.status_code == 200:
            result = response.text
            print("      ")
            print(result)
        else:
            print("[-] Error: Unable to retrieve data. Status Code:", response.status_code)
    except Exception as e:
        print("[-] An error occurred:", str(e))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("[-] Usage: python script.py <host>")
    else:
        host = sys.argv[1]
        ReverseIP(host)