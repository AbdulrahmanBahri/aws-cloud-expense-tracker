#!/usr/bin/env python3
import aws_cdk as cdk
from cloud_expense_tracker.expense_tracker_stack import ExpenseTrackerStack

app = cdk.App()

ExpenseTrackerStack(
    app,
    "CloudExpenseTrackerStack",
    env=cdk.Environment(
        account="478561403051",
        region="us-east-1"
    ),
)

app.synth()