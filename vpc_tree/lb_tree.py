# lb_tree.py
"""VPC Tree application's Load Balancer functionality."""

import boto3

from .prefix import get_prefix
from .text_tree import add_node, add_tree


class LBTree:
    """Gets details of AWS Load Balancers and represents them in a tree
    structure.

    Attributes:
        vpc_id: A string containing the id of a Virtual Private Cloud.
        load_balancers: A list of dictionaries containing details of all the
        Load Balancers linked to vpc_id.
    """

    def __init__(self, vpc_id):
        """Initializes instance.

        Args:
            vpc_id: A strings containing the id Virtual Private Cloud which
            all the Load Balancers should be linked to.
        """
        self.vpc_id = vpc_id
        self.load_balancers = []

    def generate(self, text_tree, prefix_description):
        """Generate a text based tree describing all Load Balancers linked to
        vpc_id.

        Args:
            text_tree: A list of strings to add this subtree to.
            prefix_description: A list of booleans describing a common prefix
            to be added to all strings is this text tree.
        """
        self.load_balancers = self._filter_by_vpc(self._get_lbs(), self.vpc_id)

        add_tree(
            text_tree,
            prefix_description,
            "Load Balancers:",
            self.load_balancers,
            self._add_lb_tree,
        )

    def _get_lbs(self):
        """Get all Load Balancers using boto3."""
        lbs = []

        client = boto3.client("elbv2")
        paginator = client.get_paginator("describe_load_balancers")
        page_iterator = paginator.paginate()

        for page in page_iterator:
            lbs += page["LoadBalancers"]

        return lbs

    def _filter_by_vpc(self, lbs, vpc_id):
        """Filter Load Balancers by Virtual Private Cloud Id."""
        return list(filter(lambda d: d["VpcId"] == vpc_id, lbs))

    def _add_lb_tree(self, text_tree, prefix_description, lb):
        """Adds tree describing Load Balancer to text_tree."""
        arn = lb["LoadBalancerArn"]
        name = lb["LoadBalancerName"]
        text_tree.append(f"{get_prefix(prefix_description)}{arn} : {name}")

        add_tree(
            text_tree,
            prefix_description + [False],
            "Availability Zones:",
            lb["AvailabilityZones"],
            self._add_az_node,
        )

        add_tree(
            text_tree,
            prefix_description + [True],
            "Security Groups:",
            lb["SecurityGroups"],
            add_node,
        )

    def _add_az_node(self, text_tree, prefix_description, az):
        """Adds details of Availability Zone linked to a Load Balancer to
        text_tree."""
        zone = az["ZoneName"]
        subnet_id = az["SubnetId"]
        text_tree.append(
            f"{get_prefix(prefix_description)}{zone} : {subnet_id}"
        )
