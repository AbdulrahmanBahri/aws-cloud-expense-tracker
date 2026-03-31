Day 2 focused on setting up the CDK environment rather than defining infrastructure. The goal was to establish a controlled deployment mechanism before introducing any changes to the existing system. Bootstrapping prepared the AWS account for asset-based deployments, and running synth/diff ensured visibility into what CDK would generate. No resources were created yet, as the priority was ensuring that the infrastructure definition process itself was reliable.



\## Day 3 — IAM Modeling Notes



Today I defined the Lambda execution role in CDK before modeling the rest of the infrastructure. IAM was a good first migration target because it exposed the exact boundary of what the system is allowed to do without risking stateful data.



The role currently includes:

\- AWSLambdaBasicExecutionRole for CloudWatch logging

\- Cost Explorer read access

\- DynamoDB access limited to the current table

\- SNS publish access limited to the current topic



Main checks performed:

\- confirmed permissions are explicit instead of hidden in console state

\- reviewed whether any existing permissions in the console role are broader than needed

\- treated this step as a boundary-definition exercise rather than a deployment exercise



\## Day 4 — DynamoDB modeled in CDK



Decisions:

\- Modeled the CloudDailyCosts table as infrastructure in CDK

\- Used partition key `date` (string) because current access pattern is one record per day

\- Chose PAY\_PER\_REQUEST to avoid premature capacity planning

\- Enabled point-in-time recovery for recoverability

\- Kept removal policy as DESTROY for development speed; would switch to RETAIN in a production environment

\- Left encryption at DynamoDB-managed default to keep security baseline without adding KMS complexity yet



Engineering reasoning:

\- Optimized for simple, stable access pattern

\- Avoided speculative indexes and schema complexity

\- Treated recoverability and lifecycle policy as first-class infrastructure concerns

