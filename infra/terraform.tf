terraform {
  required_version = "~>1.1"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~>5.7"
    }
  }
  backend "s3" {
    bucket         = "shopping-manager-bot-backend"
    key            = "tg_bot.tfstate"
    encrypt        = true
    use_lockfile   = true
  }
}