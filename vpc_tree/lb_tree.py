# lb_tree.py
"""VPC Tree application's Load Balancer functionality."""

import boto3

from .prefix import get_prefix
from .text_tree import generate_tree


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

    def generate(self):
        """Generate a text based tree describing all Load Balancers linked to
        vpc_id.

        Returns:
            A list of strings containing the text based tree.
        """
        self.load_balancers = self._filter_by_vpc(self._get_lbs(), self.vpc_id)

        return generate_tree(
            [], "Load Balancers:", self.load_balancers, self._lb_text
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

    def _lb_text(self, prefix_description, lb):
        """Describe a load balancer as a list of strings."""
        text_tree = []
        arn = lb["LoadBalancerArn"]
        name = lb["LoadBalancerName"]
        text_tree.append(f"{get_prefix(prefix_description)} {arn} : {name}")

        az_tree = generate_tree(
            prefix_description + [False],
            "Availability Zones:",
            lb["AvailabilityZones"],
            self._az_text,
        )
        text_tree += az_tree

        sg_tree = generate_tree(
            prefix_description + [True],
            "Security Groups:",
            lb["SecurityGroups"],
            self._sg_text,
        )
        text_tree += sg_tree

        return text_tree

    def _az_text(self, prefix_description, az):
        """Describe an Availability Zone linked to a Load Balancer as a list of
        strings."""
        zone = az["ZoneName"]
        subnet_id = az["SubnetId"]
        return [f"{get_prefix(prefix_description)}{zone} : {subnet_id}"]

    def _sg_text(self, prefix_description, sg):
        """Describe a Security Group linked to a Load Balancer as a list of
        strings."""
        return [f"{get_prefix(prefix_description)}{sg}"]
