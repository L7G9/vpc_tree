# subnets.ph

import boto3
from .prefix import get_prefix
from .tags import get_tag_value
from . import tree


class Subnets(tree.Tree):
    """AWS Subnets.

    Subclass of tree.Tree with the functionality to get details of subnets
       from boto3 and display them as a text based tree.

    Attributes:
        vpc_id: A string containing the id of a virtual private cloud.
        subnets: A list of dictionaries containing the subnets found when generate is called.
    """
    def __init__(self, vpc_id):
        """Initializes instance.

        Args:
            vpc_id: A string containing the id virtual private cloud which all
                the subnets should be linked to.
        """
        self.vpc_id = vpc_id
        self.subnets = []

    def generate(self):
        """Generate a text based tree describing all subnets linked to vpc_id.

        Returns:
            A list of strings containing the text based tree.
        """
        self.subnets = self._get_subnets()
        self.subnets = sorted(self.subnets, key=lambda x: x["CidrBlock"])

        return tree.Tree._tree_text(
            self, [], "Subnets:", self.subnets, self._subnet_text
        )

    def _get_subnets(self):
        """Get all subnets linked to vpc_id using boto3."""
        subnets = []

        client = boto3.client("ec2")
        paginator = client.get_paginator("describe_subnets")
        parameters = {
            "Filters": [
                {"Name": "vpc-id", "Values": [self.vpc_id]},
            ]
        }
        page_iterator = paginator.paginate(**parameters)
        for page in page_iterator:
            subnets += page["Subnets"]

        return subnets

    def _get_instances(self, subnet_id):
        """Get all instances linked to subnet_id using boto3."""
        instances = []

        client = boto3.client("ec2")
        paginator = client.get_paginator("describe_instances")
        parameters = {
            "Filters": [
                {"Name": "subnet-id", "Values": [subnet_id]},
            ]
        }
        page_iterator = paginator.paginate(**parameters)
        for page in page_iterator:
            for reservations in page["Reservations"]:
                instances += reservations["Instances"]

        return instances

    def _subnet_text(self, prefix_list, subnet):
        """Describe subnet as a list of strings."""
        text_tree = []

        prefix = get_prefix(prefix_list)
        id = subnet["SubnetId"]
        name = get_tag_value(subnet, "Name")
        az = subnet["AvailabilityZone"]
        cidr = subnet["CidrBlock"]

        if name is None:
            text_tree.append(f"{prefix} {id} : {az} : {cidr} ")
        else:
            text_tree.append(f"{prefix} {id} : {name} : {az} : {cidr} ")

        instances = self._get_instances(id)
        if len(instances) > 0:
            instances = sorted(instances, key=lambda x: x["PrivateIpAddress"])
            instance_tree = tree.Tree._tree_text(
                self,
                prefix_list + [True],
                "Instances:",
                instances,
                self._instance_text,
            )
            text_tree += instance_tree

        return text_tree

    def _instance_text(self, prefix_list, instance):
        """Describe instance in subnet as a list of strings."""
        text_tree = []

        prefix = get_prefix(prefix_list)
        id = instance["InstanceId"]
        name = None
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

        security_group_tree = tree.Tree._tree_text(
            self,
            prefix_list + [True],
            "SecurityGroups:",
            instance["SecurityGroups"],
            self._security_group_text,
        )
        text_tree += security_group_tree

        return text_tree

    def _security_group_text(self, prefix_list, security_group):
        """Describe security group linked to instance as a list of strings."""
        return [f"{get_prefix(prefix_list)}{security_group['GroupId']}"]
