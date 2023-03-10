terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "~> 4.56"
    }
  }
}

provider "google" {
  credentials = file("credentials/credential.json")

  project = "<PROJECT_ID>"
  region  = "asia-southeast2"
  zone    = "asia-southeast2-b"
}