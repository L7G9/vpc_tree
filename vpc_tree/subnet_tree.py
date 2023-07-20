# subnet_tree.ph
"""VPC Tree application's Subnet functionality."""

from .prefix import get_prefix
from .tags import get_tag_value
from .text_tree import add_tree
from .aws_resources import get_instances


class SubnetTree:
    """Get details of AWS Subnets and represent them in a tree structure.

    Attributes:
        vpc_id: A string containing the Id of a Virtual Private Cloud.
        subnets: A list of dictionaries containing the Subnets found when
        generate is called.
    """

    def __init__(self, subnets):
        """Initializes instance.

        Args:
            subnets: A list of dictionaries containing Subnets from Boto3.
        """
        self.subnets = subnets

    def generate(self, text_tree, prefix_description):
        """Generate a text based tree describing all Subnets linked to vpc_id.

        Args:
            text_tree: A list of strings to add this subtree to.
            prefix_description: A list of booleans describing a common prefix
            to be added to all strings is this text tree.
        """
        self.subnets = sorted(
            self.subnets, key=lambda x: x["CidrBlock"]
        )

        add_tree(
            text_tree,
            prefix_description,
            "Subnets:",
            self.subnets,
            self._add_subnet_tree,
        )

    def _add_subnet_tree(self, text_tree, prefix_description, subnet):
        """Adds tree describing Subnet to text_tree."""
        prefix = get_prefix(prefix_description)
        id = subnet["SubnetId"]
        name = get_tag_value(subnet, "Name")
        az = subnet["AvailabilityZone"]
        cidr = subnet["CidrBlock"]

        if name is None:
            text_tree.append(f"{prefix}{id} : {az} : {cidr}")
        else:
            text_tree.append(f"{prefix}{id} : {name} : {az} : {cidr}")

        instances = get_instances(id)
        if len(instances) > 0:
            instances = sorted(instances, key=lambda x: x["PrivateIpAddress"])
            add_tree(
                text_tree,
                prefix_description + [True],
                "Instances:",
                instances,
                self._add_instance_tree,
            )

    def _add_instance_tree(self, text_tree, prefix_description, instance):
        """Adds tree describing Instance in Subnet to text_tree."""
        prefix = get_prefix(prefix_description)
        id = instance["InstanceId"]
        name = get_tag_value(instance, "Name")
        image = instance["ImageId"]
        type = instance["InstanceType"]
        state = instance["State"]["Name"]
        ip = instance["PrivateIpAddress"]

        if name is None:
            text_tree.append(
                f"{prefix}{id} : {image} : {type} : {state} : {ip}"
            )
        else:
            text_tree.append(
                f"{prefix}{id} : {name} : {image} : {type} : {state} : {ip}"
            )

        add_tree(
            text_tree,
            prefix_description + [True],
            "SecurityGroups:",
            instance["SecurityGroups"],
            self._add_sg_node,
        )

    def _add_sg_node(self, text_tree, prefix_description, security_group):
        """Adds Id of Security Group linked to Instance to text_tree."""
        text_tree.append(
            f"{get_prefix(prefix_description)}{security_group['GroupId']}"
        )
