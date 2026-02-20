**1. How do I know the Lambda is running daily?**
I check the CloudWatch Lambda metrics, especially the invocation count, which should increase once per day based on the EventBridge schedule.

**2. How do I know it failed if something breaks?**
The Lambda invocation will fail and I can see that in CloudWatch.

**3. What happens if DynamoDB write fails?**
The Lambda will throw an error.
That failure will show up in CloudWatch logs and increase the Lambda error metric, so it’s visible during monitoring.

**4. What happens if Lambda runs twice in one day?**
It writes to the same DynamoDB item because the partition key is the date.
This means the existing record is overwritten instead of creating a duplicate.

**5. How would I know if alerts stop working?**
I would compare the cost values shown in CloudWatch logs with the SNS notifications I receive.
If the logs show that the cost exceeded the threshold but no email was sent, that indicates a problem with the SNS alerting setup or subscription.
