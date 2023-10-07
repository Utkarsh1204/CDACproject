from bs4 import BeautifulSoup
import requests, requests.exceptions, urllib.parse
from collections import deque
import re
import sys

if len(sys.argv) != 2:
    print("Usage: python email_scrapper.py <target_url>")
    sys.exit(1)

user_input = sys.argv[1]
try:
    if not (user_input.startswith('http://') or user_input.startswith('https://')):
        user_input = 'https://' + user_input

    urls = deque([user_input])
    scrapped_url = set()
    count = 0
    found_emails = set()

    try:
        while len(urls):
            count += 1
            if count == 10:
                break
            url = urls.popleft()

            if url.lower().startswith('tel:') or url.lower().startswith('mailto:'):
                continue

            scrapped_url.add(url)
            parts = urllib.parse.urlsplit(url)
            base_url = '{0.scheme}://{0.netloc}'.format(parts)

            path = url[url.rfind('/')+1:] if '/' in parts.path else url

            try:
                response = requests.get(url)

            except(requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
                continue

            new_emails = set(re.findall(r'[a-z0-9\. \-+_]+@[a-z0-9\. \-+_]+\.[a-z]+', response.text, re.I))

            new_emails -= found_emails
            found_emails.update(new_emails)

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
    print("                          ")
    print(f"Emails Found in {count} sub-links of {user_input} are:")
    for email in found_emails:
        cleaned_email = ''.join(email.split())
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if re.match(email_pattern, cleaned_email):
            if email.endswith('.com') or email.endswith('.in') or email.endswith('.co.in') or email.endswith('.co.uk'):
                print(cleaned_email)

except Exception as e:
    print("                          ")
    print("Invalid Domain Error")
    print("Preferred Format: www.example.com")
