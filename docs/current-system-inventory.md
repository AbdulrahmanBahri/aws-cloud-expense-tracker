# Current System Inventory — Cloud Expense Tracker

## 1) System Purpose
This system runs once per day, pulls AWS cost data from Cost Explorer, stores summarized results in DynamoDB, and sends SNS notifications when spending conditions require attention. It is currently working and was built manually through the AWS console. The purpose of the CDK migration is to make the infrastructure reproducible and safer to modify.
---

## 2) Deployment Context
- AWS Account ID: 478561403051
- AWS Region: us-east-1
- Environment Name: personal / dev / prod-like
- Current deployment method: manually created in console
- Primary owner: me

---

## 3) Lambda Details
- Function name: NotifySNSCostExplorer
- Runtime: Python 3.14
- Timeout: 10 sec
- Handler: lambda_function.lambda_handler
- Memory size: 128 MB
- Architecture: x86_64
- Log group name: /aws/lambda/NotifySNSCostExplorer
  
---

## 4) IAM Details
### Lambda Execution Role
- Role name: CloudExpenseTrackerLambdaRole 
- Trusted entity: Lambda
- Managed policies attached: AWSLambdaBasicExecutionRole - AWSLambdaBasicExecutionRole-007b5d47-1895-420c-abaa-d5e2ed30a3bd

### Required permissions observed
- Cost Explorer: Read
- DynamoDB: Write
- SNS: Write
  
---

## 5) DynamoDB Details
- Table name: CloudDailyCosts
- Partition key: date (String)
- TTL enabled?: No
- Approximate current data stored: 23.96 bytes

---

## 6) SNS Details
- Topic name: CloudCostAlerts
- Topic ARN: arn:aws:sns:us-east-1:478561403051:CloudCostAlerts
- Subscription type(s): EMAIL
- Number of subscriptions: 1

---

## 7) EventBridge Details
- Rule name: daily-cloud-cost-check
- Schedule expression: 0 0 * * ? *
- Target: Lambda function: NotifySNSCostExplorer 

---

## 8) CloudWatch / Monitoring Details
- Log group name(s): /aws/lambda/NotifySNSCostExplorer
- Log retention: Never expire

---

## 10) Configuration That Must Match Exactly in CDK
- 
- 
- 

---

## 11) Migration Risks
- 
- 
- 

---

## 12) Things I Will Not Change in the First CDK Version
- 
- 
- 

---

## 13) Future Improvements After Parity
- 
- 
- 
