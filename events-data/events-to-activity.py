import csv
import json
import requests
import os
import sys
import hashlib

token = os.environ["COMMONROOM_TOKEN"]

if not token:
    print("No value found for COMMONROOM_TOKEN environment variable.")
    exit()

destinationId = sys.argv[1]
csv_file_path = sys.argv[2]
event_name = sys.argv[3]

def send_post_request(json_record):
    url = 'https://api.commonroom.io/community/v1/source/'+destinationId+'/activity'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json_record)

    if response.status_code == 202:
        print("Successfully sent record")
    else:
        print(f"Failed to send data. Status Code: {response.status_code}, Response: {response.text}")


# Open CSV file

with open(csv_file_path, 'r') as csvfile:

    csvreader = csv.DictReader(csvfile)

    for row in csvreader:
        info_to_hash = row['Email'] + event_name
        id = hashlib.sha256(info_to_hash.encode('utf-8')).hexdigest()

        json_record= {
            "id": id,
            "activityType": "attended_gathering",
            "user":{
                "id": row['Email'],
                "firstName": row['First name'],
                "lastName": row['Last name'],
                "email": row['Email'],
                "country": row['Country'],
                "companyName": row['Company'],
                "titleAtCompany": row['Title']
            },
            "activityTitle":{
                "type": "text",
                "value": "Visited booth at \"{eventName}\"".format(eventName=event_name)
            },
            "content":{
                "type": "markdown",
                "value": '''**Event Name:** {eventName}'''.format(eventName=event_name)
            },
            "timestamp": 'Dec 4, 2023',
            "subSource":{
                "type": "name",
                "name": event_name
            }
        }

        json_data=json.dumps(json_record, indent=4)
        print(json_data)
        send_post_request(json_data)
        
        


