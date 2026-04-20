from constructs import Construct
from aws_cdk import Duration
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_iam as iam


class LambdaConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        function_name: str,
        role: iam.IRole,
        table_name: str,
        sns_topic_arn: str,
        cost_threshold: str,
        memory_size: int,
        timeout_seconds: int,
    ) -> None:
        super().__init__(scope, construct_id)

        self.function = _lambda.Function(
            self,
            "CostReporterFunction",
            function_name=function_name,
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="app.lambda_handler",
            code=_lambda.Code.from_asset("lambda/cost_reporter"),
            role=role,
            memory_size=memory_size,
            timeout=Duration.seconds(timeout_seconds),
            environment={
                "TABLE_NAME": table_name,
                "SNS_TOPIC_ARN": sns_topic_arn,
                "COST_THRESHOLD": cost_threshold,
            },
        )