from constructs import Construct
from aws_cdk import Stack
from cloud_expense_tracker.constructs.iam_construct import ExpenseTrackerIamConstruct


class ExpenseTrackerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Placeholder values for Day 3
        dynamodb_table_arn = "arn:aws:dynamodb:us-east-1:478561403051:table/CloudDailyCosts"
        sns_topic_arn = "arn:aws:sns:us-east-1:478561403051:CloudCostAlerts"

        iam_construct = ExpenseTrackerIamConstruct(
            self,
            "ExpenseTrackerIam",
            dynamodb_table_arn=dynamodb_table_arn,
            sns_topic_arn=sns_topic_arn,
        )