import csv
import json
import requests
import os
import sys
import hashlib

# Path to CSV file

token = os.environ["COMMONROOM_TOKEN"]
destinationId = sys.argv[1]
csv_file_path = sys.argv[2]

# Open CSV file

def send_post_request(json_record):
    url = 'https://api.commonroom.io/community/v1/source/' + destinationId + '/activity'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, data=json_record)


    if response.status_code == 202:
        print("Successfully sent record")
    else:
        print(f"Failed to send data. Status Code: {response.status_code}, Response: {response.text}")

with open(csv_file_path, 'r') as csvfile:

    csvreader = csv.DictReader(csvfile)

    for row in csvreader:

        info_to_hash = row['Email'] + row['Topic'] + row['Date']
        id = hashlib.sha256(info_to_hash.encode('utf-8')).hexdigest()

        json_record = {
            "id": id,
            "activityType": "attended_product_discovery_call",
            "user":{
                "id": row['Email'],
                "fullName": row['Name'],
                "email": row['Email'],
                "companyName": row['Company']
            },
            "activityTitle":{
                "type": "text",
                "value":'''Attended product discovery call on topic \"{topic}\""'''.format(topic=row['Topic'])
            },
            "content":{
                "type": "markdown",
                "value": '''**Interview Source:** {source}\n\n**Topic:** {topic}\n\n**DRI PM** {driPM}'''.format(source=row['Interview Source'],topic=row['Topic'],driPM=row['DRI PM']),
            },
            "url":row['Link to notes'],
            "timestamp": row['Timestamp'],
        }
        
        json_data=json.dumps(json_record, indent=4)
        print(json_data)
        send_post_request(json_data)


