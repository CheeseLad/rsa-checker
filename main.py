#!/usr/bin/env python3

import requests
import re

dtc_list = []

url = "https://rsa.powerappsportals.com/return-all-dtc/"
response = requests.get(url)
for i in response.json():
    dtc_list.append(i['name'])


for dtc in dtc_list[:2]:
    url2 = "https://rsa.powerappsportals.com/return-last-estimation/"
    payload = {'pdtcname': dtc}
    response = requests.post(url2, data=payload)
    
    eid = response.json()['rsa_estimationid']

    url3 = f"https://rsa.powerappsportals.com/drivertest-estimation-personal/?lastEstimationId={eid}"

    response = requests.get(url3)

    if response.status_code == 200:
        # Get the HTML content of the response
        html_content = response.text

        # Define a regex pattern to capture the name and dates
        pattern = re.compile(
            r'\$\("#lbl-tc-testcentre"\)\.text\("([^"]+)"\);.*?'
            r'\$\("#lbl-tc-expectedinvite"\)\.text\(moment\(new Date\("([^"]+)"\)\)\.format\("DD/MM/YYYY"\)\);.*?'
            r'\$\("#lbl-tc-modelpublisheddate"\)\.text\(moment\(new Date\("([^"]+)"\)\)\.format\(\'DD/MM/YYYY\'\)\);',
            re.DOTALL
        )

        # Search for the pattern in the HTML content
        match = pattern.search(html_content)

        if match:
            name = match.group(1)
            date1 = match.group(2)
            date2 = match.group(3)
            print(f"Test Centre: {name}")
            print(f"Expected Invite: {date1}")
            print(f"Last Updated: {date2}")
        else:
            print("No matches found.")
    else:
        print(f'Failed to retrieve content. Status code: {response.status_code}')