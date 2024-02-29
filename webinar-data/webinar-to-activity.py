import csv
import json
import requests
import os
import sys

# Path to CSV file

token = path = os.environ["COMMONROOM_TOKEN"]
destinationId = sys.argv[1]
csv_file_path = sys.argv[2]
webinar_name = sys.argv[3]

# Open CSV file

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

with open(csv_file_path, 'r') as csvfile:

    csvreader = csv.DictReader(csvfile)

    for row in csvreader:
        json_record= {
            "id": row['\ufeffID'],
            "activityType": "registered_for_webinar",
            "user":{
                "id": row['Email'],
                "fullName": row['User Name (Original Name)'],
                "email": row['Email'],
                "country": row['Country/Region Name'],
                "companyName": row['Organization'],
                "titleAtCompany": row['Job Title']
            },
            "activityTitle":{
                "type": "text",
                "value": "Registered for Webinar \"{webinarName}\"".format(webinarName=webinar_name)
            },
            "content":{
                "type": "markdown",
                "value": '''**Webinar:** {webinarName}\n\n**Source:** {sourceName}'''.format(webinarName=webinar_name, sourceName=row['Source Name'])
            },
            "timestamp": row['Registration Time'],
            "subSource":{
                "type": "name",
                "name": webinar_name
            }
        }

        json_data=json.dumps(json_record, indent=4)
        print(json_data)
        send_post_request(json_data)

        if row['Attended'] == 'Yes':

            json_record= {
            "id": row['\ufeffID'] + '_a',
            "activityType": "attended_webinar",
            "user":{
                "id": row['Email'],
                "fullName": row['User Name (Original Name)'],
                "email": row['Email'],
                "country": row['Country/Region Name'],
                "companyName": row['Organization'],
                "titleAtCompany": row['Job Title']
            },
            "activityTitle":{
                "type": "text",
                "value": "Attended Webinar \"{webinarName}\"".format(webinarName=webinar_name)
            },
            "content":{
                "type": "markdown",
                "value": '''**Time in Session (minutes):** {time}\n\n **Which Sonar product(s) do you currently use?** {sonarProducts}'''.format(time=row['Time in Session (minutes)'],sonarProducts=row['Which Sonar product(s) do you currently use?'])
                            
            },
            "timestamp": row['Join Time'],
            "subSource":{
                "type": "name",
                "name": webinar_name
            },
            "parentActivity":{
                "id": row['\ufeffID'],
                "activityType": "registered_for_webinar"

            }
        }

            json_data=json.dumps(json_record, indent=4)
            print(json_data)
            send_post_request(json_data)

        if row['NPS'].isnumeric():
            print('is int!')
            json_record= {
            "id": row['\ufeffID'] + '_s',
            "activityType": "answered_form_survey",
            "user":{
                "id": row['Email'],
                "fullName": row['User Name (Original Name)'],
                "email": row['Email'],
                "country": row['Country/Region Name'],
                "companyName": row['Organization'],
                "titleAtCompany": row['Job Title']
            },
            "activityTitle":{
                "type": "text",
                "value": "Filled out survey for Webinar \"{webinarName}\"".format(webinarName=webinar_name)
            },
            "content":{
                "type": "markdown",
                "value": '''**NPS:** {NPS}\n\n**What would you like to see presented during our next webinar?** {nextWebinar}\n\n**If you are a current customer, would you be interested in sharing your experience using Sonar?** {advocacy}\n\n**If you answered yes, what activities interest you? (select all that apply):** {advocacyActivities}\n\n**If you want to act as a customer reference, please enter your email so we can get in touch!** {customerReference}\n\n**Additional Comments or Questions?** {additionalComments}\n\n**Would you like to be contacted? (hot lead):** {contactYesNo}'''.format(NPS=row['NPS'], nextWebinar=row['What would you like to see presented during our next webinar?'], advocacy=row[' If you are a current customer, would you be interested in sharing your experience using Sonar?'], advocacyActivities=row['If you answered yes, what activities interest you? (select all that apply)'], customerReference=row['If you want to act as a customer reference, please enter your email so we can get in touch!'], additionalComments=row['Additional comments or questions?'], contactYesNo=row['Would you like to be contacted?'])
                            
            },
            "timestamp": row['Leave Time'],
            "subSource":{
                "type": "name",
                "name": webinar_name
            },
            "parentActivity":{
                "id": row['\ufeffID'] + '_a',
                "activityType": "attended_webinar"

            }
        }
            json_data=json.dumps(json_record, indent=4)
            print(json_data)
            send_post_request(json_data)

        
        


