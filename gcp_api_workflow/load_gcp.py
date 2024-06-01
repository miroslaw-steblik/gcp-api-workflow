import requests
import pandas as pd
from google.cloud import storage


GCP_PROJECT_ID = '<project-name>'
GCP_BUCKET_NAME = '<bucket-name>'

url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
endpoint = 'teams'
filename = 'fantasy_league_teams.csv'


def api_to_gcs(url, endpoint, filename):
    data = requests.get(url )
    json = data.json()
    df = pd.DataFrame(json[endpoint])

    client = storage.Client(project=GCP_PROJECT_ID)
    bucket = client.get_bucket(GCP_BUCKET_NAME)

    blob = bucket.blob(filename)
    blob.upload_from_string(df.to_csv(index = False),content_type = 'csv')

def main(data, context):
    api_to_gcs(url, endpoint, filename)
    print('File uploaded to GCS')


