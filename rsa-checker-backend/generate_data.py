

from time import sleep
import requests
import re
import json
import os
import schedule
import time


def write_data(new_data):
    file_path = 'temp_data.json'
    
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


def generate_data():

    if os.path.exists('temp_data.json'):
        os.remove('temp_data.json')

    dtc_list = []

    url = "https://rsa.powerappsportals.com/return-all-dtc/"
    response = requests.get(url)
    for i in response.json():
        dtc_list.append(i['name'])


    for dtc in dtc_list:
        sleep(3)
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
                print(f"Data for {name} written to file.")
            else:
                print("No matches found.")
        else:
            print(f'Failed to retrieve content. Status code: {response.status_code}')

    with open('temp_data.json') as f:
        data = json.load(f)
        if os.path.exists('data.json'):
            os.remove('data.json')

        with open('data.json', 'w') as f2:
            json.dump(data, f2, indent=4)

    if os.path.exists('temp_data.json'):
        os.remove('temp_data.json')

    return

def run_scheduler():
    schedule.every(12).hours.do(generate_data)
    
    generate_data()
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    run_scheduler()