import csv
import json
import requests
import os
import sys
import hashlib

token = os.environ["COMMONROOM_TOKEN"]
apiKey = os.environ["DISCOURSE_API_KEY"]
apiUsername = os.environ["DISCOURSE_API_USERNAME"]

destinationId = sys.argv[1]

if not token:
    print("No value found for COMMONROOM_TOKEN environment variable.")
    exit()

if not apiKey:
    print("No value found for DISCOURSE_API_KEY environment variable.")
    exit()

if not apiUsername:
    print("No value found for DISCOURSE_API_USERNAME environment variable.")
    exit()


def get_likes():
    url = 'https://community.sonarsource.com/admin/plugins/explorer/queries/92/run'
    headers = {
        'Api-Key': apiKey,
        'Api-Username': apiUsername
    }

    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        print("Successfully ran query")
        return response;
    else:
        print(f"Failed to send data. Status Code: {response.status_code}, Response: {response.text}")


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
        
response = get_likes()
likes_data = json.loads(response.text)

for row in likes_data["rows"]:
        
    json_record= {
        "id": str(row[0]),
        "activityType": "liked_reacted",
         "user":{
            "id": row[2],
            "username": row[1],
            "email": row[2],
        },
        "activityTitle":{
            "type": "text",
            "value": "Reacted to a post in topic \"" + row[5] + "\""
        },
        "content":{
            "type": "markdown",
            "value": '''**Topic:** {postTitle}'''.format(postTitle=row[5])
        },
        "timestamp": row[6],
        "url": "https://community.sonarsource.com/t/"+str(row[4])+"/"+str(row[3])
    }


    json_data=json.dumps(json_record, indent=4)
    print(json_data)
    send_post_request(json_data)

