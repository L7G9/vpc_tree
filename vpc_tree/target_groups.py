# target_groups.py

import boto3
from .prefix import get_prefix
from . import tree


class TargetGroups(tree.Tree):
    """AWS Target Groups.

    Subclass of tree.Tree with the functionality to get details of target
        groups from boto3 and display them as a text based tree.

    Attributes:
        load_balancer_arns: A list of strings containing the arns of the load balancers in a
            virtual private cloud.
    """
    def __init__(self, load_balancer_arns):
        """Initializes instance.

        Args:
            load_balancer_arns: A list of strings containing the arns of the load balancers in
                a virtual private cloud.
        """
        self.load_balancer_arns = load_balancer_arns

    def generate(self):
        """Generate a text based tree describing all the target groups linked to the load balancers
               in a virtual private cloud.

        Returns:
            A list of strings containing the text based tree.
        """
        target_groups = self._get_target_groups(self.load_balancer_arns)

        return tree.Tree._tree_text(
            self, [], "Target Groups:", target_groups, self._target_group_text
        )

    def _get_target_groups(self, load_balancer_arns):
        """Get all target groups linked to load balancer arns using boto3."""
        target_groups = []

        client = boto3.client("elbv2")
        paginator = client.get_paginator("describe_target_groups")

        for arn in load_balancer_arns:
            page_iterator = paginator.paginate(LoadBalancerArn=arn)
            for page in page_iterator:
                target_groups += page["TargetGroups"]

        return target_groups

    def _target_group_text(self, prefix_list, target_group):
        """Describe target group as a list os strings."""
        text_tree = []

        arn = target_group["TargetGroupArn"]
        name = target_group["TargetGroupName"]
        prefix = get_prefix(prefix_list)
        text_tree.append(f"{prefix}{arn} : {name}")

        load_balancer_arns = target_group["LoadBalancerArns"]
        if len(load_balancer_arns) > 0:
            text_tree += tree.Tree._tree_text(
                self,
                prefix_list + [True],
                "Load Balanacers:",
                load_balancer_arns,
                self._load_balancer_text,
            )

        return text_tree

    def _load_balancer_text(self, prefix_list, load_balancer_arn):
        """Describe load balancer linked to target group as a list of strings."""
        return [f"{get_prefix(prefix_list)}{load_balancer_arn}"]
