variable "function_name" {
  type        = string
  description = "GCS cloud function name"
  default     = "discord-slash-function"
}

variable "discord_public_key" {
  type        = string
  description = "discord public key that can be found in discord developer portal"
}