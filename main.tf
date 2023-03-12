resource "random_id" "bucket_suffix" {
  keepers     = {}
  byte_length = 8
}

resource "google_storage_bucket" "bucket" {
  name     = "function-${random_id.bucket_suffix.hex}"
  location = "US"
}

data "archive_file" "lambda_zip" {
  type        = "zip"
  output_path = "${path.module}/output/${var.function_name}.zip"
  source_dir  = "${path.module}/code"
}

resource "google_storage_bucket_object" "archive" {
  name   = local.filename_on_gcs
  bucket = google_storage_bucket.bucket.name
  source = "${path.module}/output/${var.function_name}.zip"
}

resource "google_cloudfunctions_function" "function" {
  name        = "function-test"
  description = "My function"
  runtime     = "python39"

  available_memory_mb          = 128
  source_archive_bucket        = google_storage_bucket.bucket.name
  source_archive_object        = google_storage_bucket_object.archive.name
  trigger_http                 = true
  https_trigger_security_level = "SECURE_ALWAYS"
  timeout                      = 60
  entry_point                  = "hello_http"
  labels = {
    my-label = "my-label-value"
  }

  environment_variables = {
    DISCORD_PUBLIC_KEY = var.discord_public_key
  }
}

# IAM entry for a single user to invoke the function
resource "google_cloudfunctions_function_iam_member" "invoker" {
  project        = google_cloudfunctions_function.function.project
  region         = google_cloudfunctions_function.function.region
  cloud_function = google_cloudfunctions_function.function.name

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}
