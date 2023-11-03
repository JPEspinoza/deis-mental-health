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

# enter site first to get cookies
session.get(f"https://informesdeis.minsal.cl/SASVisualAnalytics/?reportUri=%2Freports%2Freports%2F0b3119f0-db06-4f10-a9cd-61092b5790bc&sectionIndex=0&sso_guest=true&reportViewOnly=true&reportContextBar=false&sas-welcome=false")



# executor
response = session.get("https://informesdeis.minsal.cl/reportData/executors")

executor = json.loads(response.text)["items"][0]["id"]
print(executor)





# content
response = session.post(f"https://informesdeis.minsal.cl/reportData/jobs?indexStrings=false&embeddedData=false&executorId={executor}&wait=30&sequence=39&dataDefinitions=dd14540")
print(response.text)