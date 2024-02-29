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

        json_record= {
            "id": row['id'],
            "activityType": "liked_reacted",
            "user":{
                "id": row['email'],
                "username": row['username'],
                "email": row['email'],
            },
            "activityTitle":{
                "type": "text",
                "value": "Reacted to a post in topic \"" + row['title'] + "\""
            },
            "content":{
                "type": "markdown",
                "value": '''**Topic:** {postTitle}'''.format(postTitle=row['title'])
            },
            "timestamp": row['created_at'],
            "url": "https://community.sonarsource.com/t/"+row['topics_id']+"/"+row['post_number']
        }

        json_data=json.dumps(json_record, indent=4)
        print(json_data)
        send_post_request(json_data)

