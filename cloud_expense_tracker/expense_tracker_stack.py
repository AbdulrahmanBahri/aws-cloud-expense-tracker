from constructs import Construct
from aws_cdk import Stack, CfnOutput

from cloud_expense_tracker.constructs.iam_construct import ExpenseTrackerIamConstruct
from cloud_expense_tracker.constructs.dynamodb_construct import DynamoDbConstruct


class ExpenseTrackerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Day 4 - DynamoDB table created in CDK
        self.dynamodb = DynamoDbConstruct(
            self,
            "DynamoDbConstruct",
            table_name="CloudDailyCosts",
        )

        CfnOutput(
            self,
            "DynamoTableName",
            value=self.dynamodb.table.table_name,
            description="DynamoDB table name for daily cloud cost records",
        )

        # Day 3 - IAM still uses placeholder SNS ARN for now
        sns_topic_arn = "arn:aws:sns:us-east-1:478561403051:CloudCostAlerts"

        self.iam = ExpenseTrackerIamConstruct(
            self,
            "ExpenseTrackerIam",
            dynamodb_table_arn=self.dynamodb.table.table_arn,
            sns_topic_arn=sns_topic_arn,
        )