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

report_id = "0b3119f0-db06-4f10-a9cd-61092b5790bc"

# enter site first to get cookies
session.get(f"https://informesdeis.minsal.cl/SASVisualAnalytics/?reportUri=%2Freports%2Freports%2F{report_id}&sectionIndex=0&sso_guest=true&reportViewOnly=true&reportContextBar=false&sas-welcome=false")

# download content
response = session.get(f"https://informesdeis.minsal.cl/reports/reports/{report_id}/content")
print(response.text)