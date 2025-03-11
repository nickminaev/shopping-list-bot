data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy" "lambda_deployer_permission_boundary" {
  name = "DeployerPermissions"
  path_prefix = "/developers/"
}

resource "aws_iam_role" "shopping_manager_lambda_role" {
  name                 = "testRole"
  assume_role_policy   = data.aws_iam_policy_document.lambda_assume_role_policy.json
  permissions_boundary = data.aws_iam_policy.lambda_deployer_permission_boundary.arn
  path                 = "/developers/"
}