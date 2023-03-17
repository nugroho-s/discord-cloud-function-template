# discord-cloud-function-template
Terraform and python code to get started with discord slash command using google cloud function.

## How to Use
- Create and download service account credential by following [this guide](https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/getting_started#adding-credentials) and store it in credentials/credential.json
- apply terraform and fill the required variable (function name and discord public key)
- navigate to the created google cloud function in gcp console and use the trigger url with path `/interaction` to set up discord interaction endpoint
