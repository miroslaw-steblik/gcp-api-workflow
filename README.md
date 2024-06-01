# Loading API Data into Google BigQuery with Cloud Functions and Scheduler

Workflow and Google Cloud functions we’ll be using:
![Architecture Diagram](./resources/flow.png)
## Prerequisites

Google Cloud Project with neccessary IAM permissions.


## Workflow
API used for this project:
https://fantasy.premierleague.com/api/bootstrap-static/

`load_gcp.py` script is used within Cloud Function.

Script simply imports the **`teams`** endpoint data from our API location into a dataframe. As we want to store this data in Google Cloud Storage so it can be streamed into BigQuery, we’ll also need to use the Google Cloud Storage Python library. 

### Cloud Function
Now let’s create the Cloud Function that we’ll use to run this code. Navigate to the [Cloud Functions](https://console.cloud.google.com/functions) and click Create Function.

1. Add function name and choose region
2. Add Pub/Sub as Trigger & create new Topic
3. Click Next
4. Choose Inline Edito and copy `load_gcp.py` script into `main.py`
5. Add requirement.txt
6. Test function and Deploy

### Scheduling Updates

Navigate to [Cloud Scheduler](https://console.cloud.google.com/cloudscheduler) and select Create Job.

> [!NOTE]
> Cloud Scheduler uses unix-cron format

Set the Target to Pub/Sub , and the Topic to the one that you created earlier with the Cloud Function — this is how we’re going to trigger the function. 

Pub/Sub (publish/subscribe) is a secure service that allows communication between our Google Cloud platforms — our scheduled job will publish a “message” to our Pub/Sub topic. Our function will be listening out for this, and will run when the message is received.

### Uploading to BigQuery

