from constructs import Construct
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subscriptions


class NotificationsConstruct(Construct):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        topic_name: str,
        alert_email: str | None = None,
    ) -> None:
        super().__init__(scope, construct_id)

        self.topic = sns.Topic(
            self,
            "ExpenseAlertsTopic",
            topic_name=topic_name,
        )

        if alert_email:
            self.topic.add_subscription(
                subscriptions.EmailSubscription(alert_email)
            )