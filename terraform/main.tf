provider "google" {
  project = var.project_id
  region  = var.region
}

# Create Pub/Sub Topic
resource "google_pubsub_topic" "my_topic" {
  name = "my-topic"
}

# Create Pub/Sub Subscription
resource "google_pubsub_subscription" "my_subscription" {
  name  = "my-subscription"
  topic = google_pubsub_topic.my_topic.id
}

# Create Cloud Storage Bucket
resource "google_storage_bucket" "my_bucket" {
  name     = "b234cke5678t"  # Change to a globally unique bucket name
  location = var.region
}