import csv
import json
import markdownify
import requests
import os
import sys

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

        if "new idea" in row['note_title']:
            activityType = 'submitted_idea'
        else:
            activityType = 'activity_feature_idea'

        json_record= {
            "id": row['\ufeffid'],
            "activityType": activityType,
            "user":{
                "id": row['user_email'],
                "fullName": row['user_name'],
                "email": row['user_email']
            },
            "activityTitle":{
                "type": "text",
                "value": row['note_title']
            },
            "content":{
                "type": "markdown",
                "value": markdownify.markdownify(row['note_text'])
            },
            "url":"https://sonarsource.productboard.com/all-notes/notes/" + row['\ufeffid'],
            "timestamp": row['created_at'],
        }
        
        json_data=json.dumps(json_record, indent=4)
        print(json_data)
        send_post_request(json_data)


