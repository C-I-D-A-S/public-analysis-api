terraform {
  backend "s3" {
    encrypt = true
    bucket  = "qol-dev-terraform-cicd"
    region  = "us-east-2"
    key     = "terraform.qol-dev-cicd.public-qol-api.tfstate"
  }
}

provider "aws" {
  profile = "default"
  region  = "us-east-2"
}
resource "aws_ecr_repository" "qol-api_ecr-repo" {
  name = "qol/public-qol-api"
}
