import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urlparse
from urllib.parse import urljoin

s = requests.Session()
s.headers[
    "User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"


def get_forms(url):
    soup = BeautifulSoup(s.get(url).content, "html.parser")
    return soup.find_all("form")


def form_details(form):
    detailsOfForm = {}
    action = form.attrs.get("action")
    method = form.attrs.get("method", "get")
    inputs = []

    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({
            "type": input_type,
            "name": input_name,
            "value": input_value,
        })

    detailsOfForm['action'] = action
    detailsOfForm['method'] = method
    detailsOfForm['inputs'] = inputs
    return detailsOfForm


def vulnerable(response):
    errors = {"quoted string not properly terminated",
              "unclosed quotation mark after the character string",
              "you have an error in your SQL syntax"
              }
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False


def sql_injection_scan(url):
    forms = get_forms(url)
    print("                                          ")
    print(f"[+] Detected {len(forms)} forms on {url}.")

    for form_number, form in enumerate(forms, start=1):
        details = form_details(form)

        for i in "\"'":
            data = {}
            for input_tag in details["inputs"]:
                if input_tag["type"] == "hidden" or input_tag["value"]:
                    data[input_tag['name']] = input_tag["value"] + i
                elif input_tag["type"] != "submit":
                    data[input_tag['name']] = f"test{i}"

            form_details(form)

            if details["method"] == "post":
                res = s.post(url, data=data)
            elif details["method"] == "get":
                res = s.get(url, params=data)

            if 'res' in locals() and vulnerable(res):
                print(f"SQL injection attack vulnerability in link (Form {form_number}):", url)
            else:
                print(f"No SQL injection attack vulnerability detected on Form {form_number}")
                break


def scan_sql_injection_in_url(url):
    print(f"[+] Scanning SQL injection vulnerabilities in {url}.")
    js_script = "'; alert('SQL Injection Detected!'); --"
    parsed_url = urlparse(url)
    query_params = parsed_url.query

    for param in query_params.split("&"):
        if "=" in param:
            param_name, param_value = param.split("=")
            malicious_param = f"{param_name}={param_value}{js_script}"
            malicious_url = url.replace(param, malicious_param)
            response = s.get(malicious_url)

            if vulnerable(response):
                print("SQL injection attack vulnerability in link:", url)
                print("Affected parameter:", param_name)
                break

        else:
            print("No SQL injection attack vulnerability detected on the URL:", url)


if __name__ == "__main__":
    user_input = sys.argv[1]
    if user_input.startswith('http://') or user_input.startswith('https://'):
        pass
    else:
        user_input = 'https://' + user_input
    urlToBeChecked = user_input
    sql_injection_scan(urlToBeChecked)
    scan_sql_injection_in_url(urlToBeChecked)
