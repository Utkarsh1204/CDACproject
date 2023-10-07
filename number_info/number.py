import sys
import requests

def number(phonenum):
    if not (phonenum.startswith('9') or phonenum.startswith('8') or phonenum.startswith('7') or phonenum.startswith('6')):
        print("Invalid Mobile Number")
        print("Please enter a valid Mobile Number")
        exit()

    if not phonenum.startswith('91'):
        phonenum = '91' + phonenum
    
    url = (
        "http://apilayer.net/api/validate?access_key=cd3af5f7d1897dc1707c47d05c3759fd&number="
        + phonenum
    )
    resp = requests.get(url)
    details = resp.json()
    print("")
    print("Country : " + details["country_name"])
    print("Location : " + details["location"])
    print("Carrier : " + details["carrier"])
    print("Line Type : " + details["line_type"])
    print("Valid : " + str(details["valid"]))

    if "reachable" in details:
        print("Reachable : " + str(details["reachable"]))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <phone_number>")
        sys.exit(1)
    
    phonenum = sys.argv[1]
    number(phonenum)
