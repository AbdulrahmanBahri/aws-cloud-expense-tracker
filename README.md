**Cloud Expense Tracker — CDK Migration**

This started as a simple Lambda that checks AWS costs daily and stores them in DynamoDB.
At first, everything was created manually in the AWS console.

It worked, but I had problems:

hard to reproduce
not clear what’s configured where
risky to change anything

So I moved everything to CDK.

**How I migrated**

I didn’t rebuild everything at once. I moved step by step:

IAM → DynamoDB → Lambda → SNS → EventBridge

Main goal:

don’t break a working system

**Biggest learning — drift**

I changed things manually in AWS to test behavior.

What I learned:

cdk diff doesn’t detect everything
some changes (like env vars) are invisible
IAM changes can silently increase permissions

Example:

COST_THRESHOLD = 5 → 999

Everything still worked, but alerts stopped. No errors.

**If I scale this**

I’d add:

monitoring (CloudWatch alarms)
better error handling
tighter IAM
multiple environments

**Final thought**

Building the system was easy.
Understanding how it can break was the real lesson.
