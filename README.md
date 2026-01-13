# aws-cloud-expense-tracker
Flow:
1. EventBridge triggers Lambda once per day
2. Lambda calls Cost Explorer
3. Lambda parses daily cost
4. Cost stored in DynamoDB
5. If cost > threshold → SNS sends alert
