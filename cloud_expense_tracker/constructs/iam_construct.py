from constructs import Construct
from aws_cdk import (
    aws_iam as iam,
)


class ExpenseTrackerIamConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        dynamodb_table_arn: str,
        sns_topic_arn: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.lambda_role = iam.Role(
            self,
            "ExpenseTrackerLambdaRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Execution role for Cloud Expense Tracker Lambda",
        )

        self.lambda_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSLambdaBasicExecutionRole"
            )
        )

        self.lambda_role.add_to_policy(
            iam.PolicyStatement(
                sid="AllowCostExplorerRead",
                actions=[
                    "ce:GetCostAndUsage"
                ],
                resources=["*"]
            )
        )

        self.lambda_role.add_to_policy(
            iam.PolicyStatement(
                sid="AllowDynamoDbAccess",
                actions=[
                    "dynamodb:PutItem",
                    "dynamodb:UpdateItem",
                    "dynamodb:GetItem",
                    "dynamodb:Query",
                    "dynamodb:Scan"
                ],
                resources=[dynamodb_table_arn]
            )
        )

        self.lambda_role.add_to_policy(
            iam.PolicyStatement(
                sid="AllowSnsPublish",
                actions=[
                    "sns:Publish"
                ],
                resources=[sns_topic_arn]
            )
        )