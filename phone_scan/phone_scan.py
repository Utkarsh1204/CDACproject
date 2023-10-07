from bs4 import BeautifulSoup
import requests, requests.exceptions, urllib.parse
from collections import deque
import re
import sys

if len(sys.argv) != 2:
    print("Usage: python phone_scan.py <target_url>")
    sys.exit(1)

user_input = sys.argv[1]
try:
    if not (user_input.startswith('http://') or user_input.startswith('https://')):
        user_input = 'https://' + user_input

    if not re.match(r'^(https?://)?www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', user_input):
        print("Preferred format is 'www.example.com'")
    else:
        urls = deque([user_input])
        scrapped_url = set()
        count = 0

        try:
            while len(urls):
                count += 1
                if count == 20:
                    break
                url = urls.popleft()
                scrapped_url.add(url)

                parts = urllib.parse.urlsplit(url)
                base_url = '{0.scheme}://{0.netloc}'.format(parts)

                path = url[url.rfind('/') + 1:] if '/' in parts.path else url

                if url.lower().startswith('tel:') or url.lower().startswith('mailto:'):
                    continue

                try:
                    response = requests.get(url)
                except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                    continue

                number_pattern = r'\b\d+\b'
                all_numbers = set(re.findall(number_pattern, response.text))

                found_numbers = []

                for number in all_numbers:
                    cleaned_number = ''.join(number.split())
                    phone_pattern = r'^(?:\+?\d{10}|\+?\d{12}|\+?\d{11}|\d{10}|\d{12}|\d{11})$'

                    if re.match(phone_pattern, cleaned_number):
                        if (number.startswith('9') or number.startswith('8') or number.startswith('7') or number.startswith('6')) and (len(number) <= 10):
                            found_numbers.append(cleaned_number)

                for number in found_numbers:
                    print("                                        ")
                    print(f"Mobile Number found in {user_input} are: {number}")

                soup = BeautifulSoup(response.text, features="lxml")

                for anchor in soup.find_all('a'):
                    link = anchor.attrs.get('href', '')
                    if link.startswith('/'):
                        link = base_url + link
                    elif not link.startswith('http'):
                        link = urllib.parse.urljoin(url, link)
                    if not link in urls and not link in scrapped_url:
                        urls.append(link)

        except KeyboardInterrupt:
            print('[-] Closing!')
            
except Exception as e:
    print("Invalid Domain Error")
    print("Preferred Format: www.example.com")