import os
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.cloud import pubsub_v1

# Set the scope for your application
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

# Path to the mounted credentials file (matches the deployment setting)
CREDENTIALS_FILE = '/secrets/gcp/gcp-k8s-event-driven-app-bd44f4a65fc2.json'

def get_credentials():
    # Load service account credentials
    credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    return credentials

def callback_function(message):
    print(f"Received message: {message.data}")
    message.ack()

def main():
    # Get credentials for authenticated API client
    credentials = get_credentials()
    
    # Use credentials to create a Pub/Sub client
    project_id = os.getenv('PROJECT_ID')
    subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

    # Subscribe to a Pub/Sub topic
    subscription_id = os.getenv('SUBSCRIPTION_ID')
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    # Listen for messages
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback_function)
    print(f'Listening for messages on {subscription_path}...')
    
    try:
        streaming_pull_future.result()
    except Exception as e:
        print(f'Listening for messages failed: {e}')

if __name__ == '__main__':
    main()