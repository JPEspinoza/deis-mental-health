# DEIS mental health dashboard scrapper in python
# https://informesdeis.minsal.cl/SASVisualAnalytics/

import requests

# create session
headers = { 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
}
session = requests.Session()
session.headers.update(headers)

# get csrf token
url = "https://informesdeis.minsal.cl/SASVisualAnalytics/"
response = session.get(url)
csrf_token = session.cookies.get_dict()["X-Uaa-Csrf"]

# login
url = "https://informesdeis.minsal.cl/SASLogon/login.do"
payload = {
    "X-Uaa-Csrf": csrf_token,
    "username": "",
    "password": "",
    "_eventId": "guest",
}
response = session.post(url, data=payload)

# get report?
url = "https://informesdeis.minsal.cl/reports/reports/ad0c03ad-ee7a-4da4-bcc7-73d6e12920cf/content"
response = session.get(url)
print(response.text)

# get csvs

# extract data