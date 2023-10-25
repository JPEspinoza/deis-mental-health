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

# get csrf token
url = "https://informesdeis.minsal.cl/SASVisualAnalytics/"
response = session.get(url)
csrf_token = session.cookies.get_dict()["X-Uaa-Csrf"]

# login
url = "https://informesdeis.minsal.cl/SASLogon/login.do"
payload = {
    "X-Uaa-Csrf": csrf_token, # the form has a hidden input with the csrf token filled by js
    "username": "",
    "password": "",
    "_eventId": "guest",
}
response = session.post(url, data=payload)

#### get an executor
#### this is horribly opaque and i have no idea what the backend thinks about poking all these things
#### basically a ritual
# fail (449)
url = 'https://informesdeis.minsal.cl/reportData/executors'
response = session.post(url)
print(response.text)

# run authorize (449)
url = 'https://informesdeis.minsal.cl/SASLogon/oauth/authorize?client_id=sas.reportData&redirect_uri=/reportData/executors?sso_retry%3DPOST&response_type=code&state=75f9b88f'
response = session.get(url)
print(response.text)

# fail again
url = 'https://informesdeis.minsal.cl/reportData/executors?sso_retry=POST&code=2y8bwCYv5k&state=75f9b88f'
response = session.get(url)
print(response.text)

# succeed (200)
url = 'https://informesdeis.minsal.cl/reportData/executors'
response = session.post(url)
print(response.text)

exit()


# get the dashboard first page 
url = 'https://informesdeis.minsal.cl/reports/reports/ad0c03ad-ee7a-4da4-bcc7-73d6e12920cf/content'
header = {
    "Accept": "application/vnd.sas.report.content+json" # force json version instead of xml one
}
response = session.get(url, headers=header)

# get data definitions
#####


# try to get the data by force
url = 'https://informesdeis.minsal.cl/reports/reportData/jobs'
id = str(uuid.uuid4())
payload = { # this is where it gets comletely incomprehensible
    "indexString": "true",
    "embeddedData": "true",
    "wait": 30,
    "executorId": id,
    "jobId": id + "_c1",
    "sequence": 2,
    "dataDefinition": "dd374",
}
# add payload to url
url = url + "?" + "&".join([f"{k}={v}" for k,v in payload.items()])
print(url)
response = session.post(url)

print(response.text)