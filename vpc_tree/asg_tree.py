# asg_tree.py
"""VPC Tree application's Auto Scale Group functionality."""

import boto3

from .prefix import get_prefix
from .text_tree import generate_tree


class ASGTree:
    """Gets details of AWS Auto Scaling Groups and represents them in a tree
    structure.

    Attributes:
        subnet_ids: A list of strings containing the Ids of the Subnets in a
        Virtual Private Cloud.
    """

    def __init__(self, subnet_ids):
        """Initializes instance.

        Args:
            subnet_ids: A list of strings containing the Ids of the Subnets in
            a Virtual Private Cloud.
        """
        self.subnet_ids = subnet_ids

    def generate(self):
        """Generate a text based tree describing all the Auto Scaling Groups
        linked to the Subnets in subnet_ids.

        Returns:
            A list of strings containing the text based tree.
        """
        asgs = self._filter_by_subnets(self._get_asgs(), self.subnet_ids)
        return generate_tree(
            [], "Auto Scaling Groups:", asgs, self._asg_text
        )

    def _get_asgs(self):
        """Get all Auto Scaling Groups using Boto3."""
        asgs = []

        client = boto3.client("autoscaling")
        paginator = client.get_paginator("describe_auto_scaling_groups")
        page_iterator = paginator.paginate()

        for page in page_iterator:
            asgs += page["AutoScalingGroups"]

        return asgs

    def _filter_by_subnets(self, asgs, vpc_subnet_ids):
        """Filter all Auto Scaling Groups by Subnets in the Virtual Private
        Cloud."""
        filtered_asgs = []
        for asg in asgs:
            asg_subnet_ids = asg["VPCZoneIdentifier"].split(",")
            if any(id in vpc_subnet_ids for id in asg_subnet_ids):
                filtered_asgs.append(asg)

        return filtered_asgs

    def _asg_text(self, prefix_description, asg):
        """Describe an Auto Scaling Group as a list of strings."""
        text_tree = []

        arn = asg["AutoScalingGroupARN"]
        name = asg["AutoScalingGroupName"]
        text_tree.append(f"{get_prefix(prefix_description)} {arn} : {name}")

        subnet_tree = generate_tree(
            prefix_description + [False],
            "Subnets:",
            asg["VPCZoneIdentifier"].split(","),
            self._subnet_text,
        )
        text_tree += subnet_tree

        instance_tree = generate_tree(
            prefix_description + [True],
            "Instances:",
            asg["Instances"],
            self._instance_text,
        )
        text_tree += instance_tree

        return text_tree

    def _subnet_text(self, prefix_description, subnet_id):
        """Describe a Subnet linked to an Auto Scaling Group as a list of
        strings."""
        return [f"{get_prefix(prefix_description)} {subnet_id}"]

    def _instance_text(self, prefix_description, instance):
        """Describe an Instance linked to an Auto Scaling Group as a list of
        strings."""
        return [f"{get_prefix(prefix_description)} {instance['InstanceId']}"]
