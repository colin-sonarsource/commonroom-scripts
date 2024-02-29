This script allows us to import a CSV of Productboard insights into CommonRoom

The CSV needs to include the following columns, in no particular order:

- ID
- note_title
- user_email
- user_name
- note_text
- created_at

The script relies on a single environment variable `COMMONROOM_TOKEN`  for authentication.

The script accepts two arguments:

- Destination ID
- CSV file path

**Example:**
```
  python3 insights-to-activity.py 45233 insights.csv
```

For each insight, 1 activity will be created in CommonRoom, which two different types depending on wheter it's a new idea (`submitted_idea`) or activity on an existing idea (`activity_feature_idea`)
