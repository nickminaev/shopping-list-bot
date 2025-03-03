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

data "aws_iam_policy_document" "shopping_manager_dynamodb_access" {
  statement {
    sid = "dynamoDBAccess"

    effect = "Allow"

    actions = [
      "dynamodb:PutItem",
      "dynamodb:UpdateItem",
      "dynamodb:DeleteItem",
      "dynamodb:BatchWriteItem",
      "dynamodb:GetItem",
      "dynamodb:BatchGetItem",
      "dynamodb:Scan",
      "dynamodb:Query",
      "dynamodb:ConditionCheckItem",
    ]
    resources = [
      "${aws_dynamodb_table.shopping_list_bot_table.arn}",
      "${aws_dynamodb_table.shopping_list_bot_table.arn}/index/*",
    ]
  }
}

resource "aws_iam_policy" "tg_lambda_dynamodb_table_access" {
  policy = data.aws_iam_policy_document.shopping_manager_dynamodb_access.json
  name   = "testPolicyDocument"
}