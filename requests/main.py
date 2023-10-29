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
# this is an opaque ritual
# I don't understand where the state comes from, i think the frontend generates a random one, so just putting a random string works

url = 'https://informesdeis.minsal.cl/reportData/executors'
session.post(url)

url = 'https://informesdeis.minsal.cl/SASLogon/oauth/authorize?client_id=sas.reportData&redirect_uri=/reportData/executors?sso_retry=POST&response_type=code&state=7bb636be'
session.get(url)

url = 'https://informesdeis.minsal.cl/reportData/executors?sso_retry=POST&code=tV6RLE79Dd&state=7bb636be'
session.get(url)

url = 'https://informesdeis.minsal.cl/reportData/executors'
response = session.get(url)

# extract the executorid
response = json.loads(response.text)
executorid = response["items"][0]["id"]

### try to get the data by force using the acquired executorid
url = f'https://informesdeis.minsal.cl/reportData/jobs?indexStrings=true&embeddedData=true&executorId={executorid}&wait=30&jobId={executorid}_c0&sequence=1'
response = session.post(url)

print(executorid)
print(response.text)


exit()

### get the dashboard first page 
url = 'https://informesdeis.minsal.cl/reports/reports/ad0c03ad-ee7a-4da4-bcc7-73d6e12920cf/content'
header = {
    "Accept": "application/vnd.sas.report.content+json" # force json version instead of xml one
}
response = session.get(url, headers=header)

### extract data definitions from response