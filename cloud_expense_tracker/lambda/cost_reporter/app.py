import os
import boto3
from decimal import Decimal
from datetime import datetime, timedelta

TABLE_NAME = os.environ["TABLE_NAME"]
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
COST_THRESHOLD = float(os.environ["COST_THRESHOLD"])

dynamodb = boto3.resource("dynamodb")
ce = boto3.client("ce")
sns = boto3.client("sns")


def lambda_handler(event, context):
    # Get yesterday's date
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    start = yesterday.strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")

    # Call Cost Explorer
    response = ce.get_cost_and_usage(
        TimePeriod={"Start": start, "End": end},
        Granularity="DAILY",
        Metrics=["UnblendedCost"],
    )

    amount = response["ResultsByTime"][0]["Total"]["UnblendedCost"]["Amount"]
    cost = Decimal(amount)

    # Store in DynamoDB
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(
        Item={
            "date": start,
            "cost": cost
        }
    )

    # Send alert if threshold exceeded
    if float(cost) > COST_THRESHOLD:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Cloud Cost Alert",
            Message=f"Daily cost exceeded threshold: ${cost}"
        )

    return {
        "statusCode": 200,
        "body": f"Daily cost: {cost}"
    }