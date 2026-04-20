Day 2 — CDK Foundation \& Environment Setup

Day 2 focused on setting up the CDK environment rather than defining infrastructure. The goal was to establish a controlled deployment mechanism before introducing any changes to the existing system.

Bootstrapping prepared the AWS account for asset-based deployments, and running cdk synth / cdk diff ensured visibility into what CDK would generate before any deployment.

No resources were created at this stage. The priority was ensuring that the infrastructure definition and deployment workflow itself is reliable, observable, and predictable before modifying real systems.

Reliability thinking:

Infrastructure changes should be previewed before execution (diff as a safety gate)
The deployment mechanism must be trusted before the infrastructure it manages
Separating definition from deployment reduces accidental production impact


Day 3 — IAM Modeling Notes

Today I defined the Lambda execution role in CDK before modeling the rest of the infrastructure.

IAM was a good first migration target because it defines what the system is allowed to do without touching stateful resources.

The role currently includes:

AWSLambdaBasicExecutionRole for CloudWatch logging
Cost Explorer read access
DynamoDB access limited to the current table
SNS publish access limited to the current topic

Main checks performed:

Confirmed permissions are explicit instead of hidden in console state
Reviewed whether existing permissions are broader than required
Ensured resources are scoped (table ARN, topic ARN) instead of wildcarded

Reliability thinking:

IAM misconfiguration causes runtime failure, not deployment failure
Overly broad permissions increase blast radius of bugs
Under-scoped permissions create hidden failure paths
IAM should be treated as a contract, not just configuration


Day 4 — DynamoDB modeled in CDK

Decisions:

Modeled the CloudDailyCosts table as infrastructure in CDK
Used partition key date (string) because access pattern is one record per day
Chose PAY\_PER\_REQUEST to avoid premature capacity planning
Enabled point-in-time recovery for recoverability
Used DESTROY removal policy for development (would be RETAIN in production)
Kept default DynamoDB-managed encryption

Engineering reasoning:

Optimized for a simple and stable access pattern
Avoided speculative schema complexity (no sort key, no GSIs yet)
Treated recoverability and lifecycle policies as first-class concerns

Reliability thinking:

Data is the most critical asset; infrastructure must protect it by default
Point-in-time recovery enables rollback from bad writes or deployment errors
Removal policies define what happens during failure or stack deletion
Table schema should match actual access patterns, not anticipated ones


Day 4 — Lambda modeled in CDK (Behavior Lock-In)

After defining IAM and DynamoDB, the Lambda function was modeled in CDK with a focus on preserving existing behavior rather than improving it.

Decisions:

Modeled the existing Lambda in CDK without changing business logic
Preserved handler, runtime, memory, and timeout configuration
Passed infrastructure dependencies (table name, topic ARN, threshold) via environment variables
Used asset packaging (from\_asset) to make the local repository the source of truth
Attached the previously defined IAM role instead of creating a new one inside the construct

Engineering reasoning:

Treated Lambda migration as a behavior lock-in step, not a refactor
Avoided introducing logic changes during infrastructure migration
Ensured infrastructure and application boundaries remain clean
Made runtime configuration explicit rather than hidden in console settings

Reliability thinking:

Lambda behavior can drift through configuration changes even if code remains unchanged
Environment variables are part of runtime behavior and must be treated as critical configuration
Timeout and memory settings directly affect reliability, not just cost
Packaging code from the local repository makes deployments reproducible, but increases the need for disciplined changes
IAM issues surface at runtime, making testing critical after deployment

Migration risk considered:

Creating a new Lambda alongside an existing console Lambda can result in duplicate systems
Function naming must be handled intentionally to avoid deployment conflicts
Migration should be staged (parallel → verify → cutover) rather than destructive


Day 5 — SNS and EventBridge modeled in CDK

Decisions:

Modeled the SNS alert topic in CDK
Modeled the daily EventBridge rule in CDK
Wired EventBridge to the Lambda function through a separate scheduling construct
Replaced hardcoded SNS ARN references with a CDK-managed topic ARN

Engineering reasoning:

Kept scheduling, notifications, runtime behavior, and state management in separate constructs
Reduced hardcoded infrastructure references
Treated automation wiring as an operational concern, not just a syntax task

Key risks considered:

Running both the old console scheduler and the new CDK scheduler would cause duplicate Lambda executions
Duplicate executions could lead to repeated DynamoDB writes, repeated alerts, and misleading logs
EventBridge schedules operate in UTC, requiring explicit time decisions
SNS topic creation does not guarantee alert delivery if subscriptions are not configured or confirmed

Reliability thinking:

Automation layers (schedulers, event triggers) must be treated as critical system components
A system can appear healthy while executing duplicate workloads
Infrastructure migration must consider behavior duplication, not just resource creation
Event-driven systems require careful reasoning about who triggers what, and how often


Day 6 — Drift Detection \& Failure Scenarios



Today focused on understanding how live AWS resources can drift away from CDK-defined infrastructure, and how that drift affects reliability and security.



Two types of drift were intentionally introduced directly in the AWS console:



1\. IAM drift



The Lambda execution role was modified manually by:



attaching the managed policy AmazonS3FullAccess

adding an extra inline policy statement allowing S3 list access

2\. Lambda configuration drift



The Lambda environment variable COST\_THRESHOLD was changed from 5 to 999



Observation



cdk drift detected both changes and reported that the deployed resources had diverged from the expected stack configuration.



Key learnings

IAM drift changes the security boundary of the system and can silently expand permissions

Lambda configuration drift changes runtime behavior even when application code is unchanged

Drift can impact both security and functional correctness

Infrastructure as code only remains trustworthy if manual console changes are minimized or actively reconciled

Reliability thinking

Security drift is especially dangerous because it increases blast radius without changing application logic

Configuration drift can create silent business failures, such as alerts no longer triggering

Production systems need a clear ownership model for change management

CDK should be treated as the source of truth, and manual changes should be temporary or codified back into infrastructure code

Ownership model

Infrastructure changes should ideally flow through CDK

Manual production changes should be rare, intentional, and reviewed

Drift detection should be part of operational hygiene, not only a debugging step

