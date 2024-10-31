import os
import json
from google.cloud import pubsub_v1, storage

# Initialize Pub/Sub and Storage clients
# No need to specify credentials, Workload Identity will handle it
subscriber = pubsub_v1.SubscriberClient()
storage_client = storage.Client()

# Configuration from environment variables
PROJECT_ID = "gcp-k8s-event-driven-app"
SUBSCRIPTION_ID = "my-subscription"
BUCKET_NAME = "b234cke5678t"

# Function to process incoming events
def process_event(message):
    print(f"Received message: {message.data.decode('utf-8')}")
    message.ack()

    # Process the message data (example: echoing the content)
    processed_data = {
        "original_message": message.data.decode('utf-8'),
        "processed": True
    }

    # Save the processed data to Cloud Storage
    save_to_gcs(processed_data)

# Function to save data to Google Cloud Storage
def save_to_gcs(data):
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob("processed_data.json")
    blob.upload_from_string(json.dumps(data), content_type="application/json")
    print(f"Data saved to {BUCKET_NAME}/processed_data.json")

# Main function to listen to Pub/Sub messages
def main():
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=process_event)
    print(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

if __name__ == "__main__":
    main()


