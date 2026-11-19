terraform {
  required_version = ">= 1.10"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.90"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  # Where state lives. The details come from backend.hcl at init time.
  backend "s3" {}
}

provider "aws" {
  region = var.aws_region

  # Every resource automatically gets these tags. Useful for finding and costing things.
  default_tags {
    tags = {
      Project     = "PlantPulse"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
data "aws_partition" "current" {}

locals {
  name       = "${var.project}-${var.environment}" # "plantpulse-dev", the prefix on every resource name
  account_id = data.aws_caller_identity.current.account_id
  region     = data.aws_region.current.name
  partition  = data.aws_partition.current.partition
}