# DEIS mental health dashboard scrapper in python
# https://informesdeis.minsal.cl/SASVisualAnalytics/

import requests
import json

# create session
headers = { 
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
}
session = requests.Session()
session.headers.update(headers)

### get csrf token from the form in the login page
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

#### get an executor, the executor is used to get data from the dashboard
# the website seems to get the executor through a complex process with some authorizes ending on a post
# I couldn't imitate it, but the get request gets it directly with no nuance, took me a while to figure it out
url = 'https://informesdeis.minsal.cl/reportData/executors'
response = session.get(url) 

# extract the executorid
response = json.loads(response.text)
executorid = response["items"][0]["id"]

### try to get the data by force using the acquired executorid
# no idea where the data definition comes from, but it looks like thats all we need
# if you need to scrape from another dashboard, you can get the data definition from the network tab in the browser
url = f'https://informesdeis.minsal.cl/reportData/jobs?indexStrings=true&embeddedData=true&executorId={executorid}&wait=30&jobId={executorid}_c0&sequence=1&dataDefinitions=dd34112'
response = session.get(url)

print(response.text)