# lb_tree.py
"""VPC Tree application's Load Balancer functionality."""

from .prefix import get_prefix
from .text_tree import add_node, add_tree


class LBTree:
    """Generates a text tree representation of AWS Load Balancers.

    Attributes:
        load_balancers: A list of dictionaries containing Load Balancers from
        Boto3.
    """

    def __init__(self, load_balancers):
        """Initializes instance.

        Args:
            load_balancers: A list of dictionaries containing Load Balancers
            from Boto3.
        """
        self.load_balancers = load_balancers

    def generate(self, text_tree, prefix_description):
        """Generate a text based tree describing the Load Balancers.

        Args:
            text_tree: A list of strings to add this subtree to.
            prefix_description: A list of booleans describing a common prefix
            to be added to all strings is this text tree.
        """
        add_tree(
            text_tree,
            prefix_description,
            "Load Balancers:",
            self.load_balancers,
            self._add_lb_tree,
        )

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
