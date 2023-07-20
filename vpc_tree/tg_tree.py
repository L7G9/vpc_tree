# tg_tree.py
"""VPC Tree application's Target Group functionality."""

from .prefix import get_prefix
from .text_tree import add_node, add_tree


class TGTree:
    """Generates a text tree representation of AWS Target Groups.

    Attributes:
        target_groups: A list of dictionaries containing Target Groups from
        Boto3.
    """

    def __init__(self, target_groups):
        """Initializes instance.

        Args:
            target_groups: A list of dictionaries containing Target Groups from
            Boto3.
        """
        self.target_groups = target_groups

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
            self.target_groups,
            self._add_tg_tree,
        )

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
