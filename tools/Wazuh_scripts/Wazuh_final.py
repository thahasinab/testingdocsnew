from __future__ import unicode_literals
import csv
import subprocess
import requests
import simplejson as json
import datetime
import os
import time
from requests.structures import CaseInsensitiveDict
import sys

######################################################## Splunk query to extract the vulnerability data ########################################################

headers = {
    'Content-Type': 'application/json',
}

if(sys.argv[1] == "C"):
    sys.argv[1]  = "Critical"  
if(sys.argv[1] == "H"):
    sys.argv[1]  = "High"  
if(sys.argv[1] == "M"):
    sys.argv[1]  = "Medium"  
if(sys.argv[1] == "L"):
    sys.argv[1]  = "Low"  
    
data = 'output_mode=json&search=search index=wazuh rule.groups{}=vulnerability-detector (data.vulnerability.severity=' + sys.argv[1] + ') earliest=-1d'

url = 'https://10.151.10.161:8089/services/search/jobs/export'
c = 0

today = datetime.date.today()
time = time.time()

header =  ['Title','Agent ID','CVE','Description','CWE', 'Severity','Agent Name','Reference','Agent IP']

r = requests.request("POST",url, headers=headers, data=data,verify=False, auth=('csw-api-user', 'QWq3jqQKjCyrw7CnktF7'),stream=True)

#######################################################  Breaking the response into chunks  ######################################################################

r.raise_for_status()
with open("Splunk_data.json", 'wb') as f:
    for chunk in r.iter_content(chunk_size=10000):
        f.write(chunk)

f.close()

print("\nExtracting the {0} vulnerabilities from Splunk".format(sys.argv[1]))

data_list=[]

with open('Splunk_data.json') as f:
     for jsonObj in f:
        data_dict = json.loads(jsonObj)
        data_list.append(data_dict)
f.close()

count=0

##################################################################  Writing it to a file ########################################################################################

with open('Data'+ '_' + str(today) + str(time) + "_" +'.csv', 'a') as f:
    for splunk_data in data_list:
        string =  json.loads(str(splunk_data["result"]["_raw"]))
        writer = csv.writer(f)
        if(count==0):
            writer.writerow(header)
        try:
            f.write(string["data"]["vulnerability"]["title"] + ",")           
        except Exception as e:
            f.write(""+",")

        try:
            f.write(string["agent"]["id"] + ",")
        except Exception as e:
            f.write(""+",")

        try:
            f.write(string["data"]["vulnerability"]["cve"] + ",")
        except Exception as e:
            f.write(""+",")
        try:
            rationale = (string["data"]["vulnerability"]["rationale"]).replace(",","")
            f.write(rationale + ",")
        except Exception as e:
            f.write(""+",")
        try:
            f.write(string["data"]["vulnerability"]["cwe_reference"] + ",")
        except Exception as e:
            f.write(""+",")
        try:    
            f.write(string["data"]["vulnerability"]["cvss"]["cvss3"]["base_score"] + ",")
        except Exception as e:
            f.write(""+",")
        '''try:
            severity = string["data"]["vulnerability"]["severity"]
            if(severity == "Critical"):
                severity = "9"
            if(severity == "Medium"):
                severity = "5"
            if(severity == "High"):
                severity = "7"
            if(severity == "Low"):
                severity = "3"
            f.write(severity+",")       
        except Exception as e:
            f.write(""+",")'''

        try:
            f.write(string["agent"]["name"] + ",")
        except Exception as e:
            f.write(""+",")

        try:
            f.write(string["data"]["vulnerability"]["references"][0] + ",")
        except Exception as e:
            f.write(""+",")

        try:
            f.write(string["agent"]["ip"])
        except Exception as e:
            f.write(""+",")  
        count += 1
        f.write("\n")
f.close()
