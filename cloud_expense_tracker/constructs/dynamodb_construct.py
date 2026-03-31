from constructs import Construct
from aws_cdk import (
    RemovalPolicy,
    aws_dynamodb as dynamodb,
)


class DynamoDbConstruct(Construct):
    def __init__(self, scope: Construct, construct_id: str, *, table_name: str) -> None:
        super().__init__(scope, construct_id)

        self.table = dynamodb.Table(
            self,
            "CloudDailyCostsTable",
            table_name=table_name,
            partition_key=dynamodb.Attribute(
                name="date",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            point_in_time_recovery=True,
            removal_policy=RemovalPolicy.DESTROY,
        )