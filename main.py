

from time import sleep
import requests
import re
import json
import os

def write_data(new_data):
    file_path = 'data.json'
    
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.append(new_data)

    with open(file_path, 'w') as f:
        json.dump(existing_data, f, indent=4)

dtc_list = []

url = "https://rsa.powerappsportals.com/return-all-dtc/"
response = requests.get(url)
for i in response.json():
    dtc_list.append(i['name'])


for dtc in dtc_list:
    sleep(4)
    url2 = "https://rsa.powerappsportals.com/return-last-estimation/"
    payload = {'pdtcname': dtc}
    response = requests.post(url2, data=payload)
    
    eid = response.json()['rsa_estimationid']

    url3 = f"https://rsa.powerappsportals.com/drivertest-estimation-personal/?lastEstimationId={eid}"

    response = requests.get(url3)

    if response.status_code == 200:
        html_content = response.text

        pattern = re.compile(
            r'\$\("#lbl-tc-testcentre"\)\.text\("([^"]+)"\);.*?'
            r'\$\("#lbl-tc-expectedinvite"\)\.text\(moment\(new Date\("([^"]+)"\)\)\.format\("DD/MM/YYYY"\)\);.*?'
            r'\$\("#lbl-tc-modelpublisheddate"\)\.text\(moment\(new Date\("([^"]+)"\)\)\.format\(\'DD/MM/YYYY\'\)\);',
            re.DOTALL
        )

        match = pattern.search(html_content)

        if match:
            name = match.group(1)
            date1 = match.group(2)
            date2 = match.group(3)
            data = {
                "Test Centre": name,
                "Expected Invite": date1,
                "Last Updated": date2
            }

            write_data(data)
        else:
            print("No matches found.")
    else:
        print(f'Failed to retrieve content. Status code: {response.status_code}')