locals {
  filename_on_gcs = "${var.function_name}-${lower(replace(base64encode(data.archive_file.lambda_zip.output_md5), "=", ""))}.zip"
}