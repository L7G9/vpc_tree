# load_balancers.py

import boto3
from .prefix import get_prefix
from . import tree


class LoadBalancers(tree.Tree):
    """AWS Load Balancers.

    Subclass of tree.Tree with the functionality to get details of auto
        scaling groups from boto3 and display them as a text based tree.

    Attributes:
        vpc_id: A string containing the id of a virtual private cloud.
        load_balancers: A list of dictionaries containing details of all the
            load balancers linked to vpc_id.
    """
    def __init__(self, vpc_id):
        """Initializes instance.

        Args:
            vpc_id: A strings containing the id virtual private cloud which
                all the load balancers should be linked to.
        """
        self.vpc_id = vpc_id
        self.load_balancers = []

    def generate(self):
        """Generate a text based tree describing all load balancers linked to
        vpc_id.

        Returns:
            A list of strings containing the text based tree.
        """
        self.load_balancers = self._filter_by_vpc(self._get_lbs(), self.vpc_id)

        return tree.Tree._tree_text(
            self, [], "Load Balancers:", self.load_balancers, self._lb_text
        )

    def _get_lbs(self):
        """Get all load balancers using boto3."""
        lbs = []

        client = boto3.client("elbv2")
        paginator = client.get_paginator("describe_load_balancers")
        page_iterator = paginator.paginate()

        for page in page_iterator:
            lbs += page["LoadBalancers"]

        return lbs

    def _filter_by_vpc(self, lbs, vpc_id):
        """Filter load balancers by virtual private cloud id."""
        return list(filter(lambda d: d["VpcId"] == vpc_id, lbs))

    def _lb_text(self, prefix, lb):
        """Describe a load balancer as a list of strings."""
        text_tree = []
        arn = lb["LoadBalancerArn"]
        name = lb["LoadBalancerName"]
        text_tree.append(f"{get_prefix(prefix)} {arn} : {name}")

        az_tree = tree.Tree._tree_text(
            self,
            prefix + [False],
            "Availability Zones:",
            lb["AvailabilityZones"],
            self._az_text,
        )
        text_tree += az_tree

        sg_tree = tree.Tree._tree_text(
            self,
            prefix + [True],
            "Security Groups:",
            lb["SecurityGroups"],
            self._sg_text,
        )
        text_tree += sg_tree

        return text_tree

    def _az_text(self, prefix, az):
        """Describe an availability zone linked to a load balancer as a list of
        strings."""
        zone = az["ZoneName"]
        subnet_id = az["SubnetId"]
        return [f"{get_prefix(prefix)}{zone} : {subnet_id}"]

    def _sg_text(self, prefix, sg):
        """Describe a security group linked to a load balancer as a list of
        strings."""
        return [f"{get_prefix(prefix)}{sg}"]
