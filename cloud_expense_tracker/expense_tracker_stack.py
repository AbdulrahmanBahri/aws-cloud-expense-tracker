from constructs import Construct
from aws_cdk import Stack

class ExpenseTrackerStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # Day 2: empty stack skeleton
        pass
