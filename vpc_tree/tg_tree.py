# tg_tree.py
"""VPC Tree application's Target Group functionality."""

import boto3

from .prefix import get_prefix
from .text_tree import add_node, add_tree


class TGTree:
    """Gets details of AWS Target Groups and represents them in a tree
    structure.

    Attributes:
        load_balancer_arns: A list of strings containing the arns of the Load
        Balancers in a Virtual Private Cloud.
    """

    def __init__(self, load_balancer_arns):
        """Initializes instance.

        Args:
            load_balancer_arns: A list of strings containing the arns of the
            Load Balancers in a Virtual Private Cloud.
        """
        self.load_balancer_arns = load_balancer_arns

    def generate(self, text_tree, prefix_description):
        """Generate a text based tree describing all the Target Groups linked
        to the Load Balancers in a Virtual Private Cloud.

        Args:
            text_tree: A list of strings to add this subtree to.
            prefix_description: A list of booleans describing a common prefix
            to be added to all strings is this text tree.
        """

        add_tree(
            text_tree,
            prefix_description,
            "Target Groups:",
            self._get_target_groups(self.load_balancer_arns),
            self._add_tg_tree,
        )

    def _get_target_groups(self, load_balancer_arns):
        """Get all target groups linked to load balancer arns using Boto3."""
        target_groups = []

        client = boto3.client("elbv2")
        paginator = client.get_paginator("describe_target_groups")

        for arn in load_balancer_arns:
            page_iterator = paginator.paginate(LoadBalancerArn=arn)
            for page in page_iterator:
                target_groups += page["TargetGroups"]

        return target_groups

    def _add_tg_tree(self, text_tree, prefix_description, target_group):
        """Adds tree describing Target Group to text_tree."""
        arn = target_group["TargetGroupArn"]
        name = target_group["TargetGroupName"]
        prefix = get_prefix(prefix_description)
        text_tree.append(f"{prefix}{arn} : {name}")

        load_balancer_arns = target_group["LoadBalancerArns"]
        if len(load_balancer_arns) > 0:
            add_tree(
                text_tree,
                prefix_description + [True],
                "Load Balancers:",
                load_balancer_arns,
                add_node,
            )
