# DEIS mental health dashboard scrapper in python
# https://informesdeis.minsal.cl/SASVisualAnalytics/

import requests
import json
import uuid

# create session
headers = { 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
}
session = requests.Session()
session.headers.update(headers)

### get csrf token
url = "https://informesdeis.minsal.cl/SASVisualAnalytics/"
response = session.get(url)
csrf_token = session.cookies.get_dict()["X-Uaa-Csrf"]

### login
url = "https://informesdeis.minsal.cl/SASLogon/login.do"
payload = {
    "X-Uaa-Csrf": csrf_token, # the form has a hidden input with the csrf token filled by js
    "username": "",
    "password": "",
    "_eventId": "guest",
}
response = session.post(url, data=payload)

#### get an executor
url = 'https://informesdeis.minsal.cl/reportData/executors'
response = session.get(url)

# extract the executorid
response = json.loads(response.text)
executorid = response["items"][0]["id"]

### get the data definitions from the dashboard
url = 'https://informesdeis.minsal.cl/reports/reports/ad0c03ad-ee7a-4da4-bcc7-73d6e12920cf/content'
header = {
    "Accept": "application/vnd.sas.report.content+json" # force json version instead of xml one
}
response = session.get(url, headers=header)

print(response.text)

### try to get the data by force using the acquired executorid
url = f'https://informesdeis.minsal.cl/reportData/jobs?indexStrings=true&embeddedData=true&executorId={executorid}&wait=30&jobId={executorid}_c1&sequence=2&dataDefinitions=dd34112'
response = session.get(url)

print(response.text)