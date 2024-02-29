This script allows us to import a CSV of Webinar registration/attendee data into Common Room.

The CSV needs to include the following columns, in no particular order:

- ID
- User Name (Original Name)
- Email
- Organization
- Job Title
- Registration Time
- Join Time
- Leave Time
- Time in Session
- Country/Region Name
- Source Name
- NPS
- What would you like to see presented during our next webinar?
- If you are a current customer, would you be interested in sharing your experience using Sonar?
- If you answered yes, what activities interest you? (select all that apply)
- If you want to act as a customer reference, please enter your email so we can get in touch!
- Additional comments or questions?
- Would you like to be contacted?
- Which Sonar product(s) do you currently use?

The script relies on a single environment variable `COMMONROOM_TOKEN`  for authentication.

The script accepts three arguments:

- Destination ID
- CSV file path
- Webinar Name

**Example:**
```
  python3 webinar-to-activity.py 45474 ccprinciplespractices.csv "Clean Code Principles and Practices"
```

For each webinar registration, up to 3 activities may be created in CommonRoom

- Webinar Registration
- Webinar Attendance
- Completing the survey after the Webinar

Each activity is a child activity of the previous one
