from constructs import Construct
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets
from aws_cdk.aws_lambda import IFunction


class ScheduleConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        target_lambda: IFunction,
        schedule_hour_utc: str,
        schedule_minute_utc: str,
    ) -> None:
        super().__init__(scope, construct_id)

        self.rule = events.Rule(
            self,
            "daily-cloud-cost-check",
            schedule=events.Schedule.cron(
                minute=schedule_minute_utc,
                hour=schedule_hour_utc,
            ),
        )

        self.rule.add_target(targets.LambdaFunction(target_lambda))