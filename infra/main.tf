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

resource "aws_iam_role" "shopping_manager_lambda_role" {
  name               = "testRole"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json
}