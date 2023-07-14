# auto_scaling_groups.py
"""This module provides ASG Tree main module."""

import boto3
from .prefix import get_prefix
from . import tree


class AutoScalingGroups(tree.Tree):
    """AWS Auto Scaling Groups.

    Subclass of tree.Tree with the functionality to get details of auto
        scaling groups from boto3 and display them as a text based tree.

    Attributes:
        subnet_ids: A list of strings containing the ids of the subnets in a
            virtual private cloud.
    """

    def __init__(self, subnet_ids):
        """Initializes instance.

        Args:
            subnet_ids: A list of strings containing the ids of the subnets in
                a virtual private cloud.
        """
        self.subnet_ids = subnet_ids

    def generate(self):
        """Generate a text based tree describing all the auto scaling groups
        linked to subnets in subnet_ids.

        Returns:
            A list of strings containing the text based tree.
        """
        asgs = self._get_asgs()
        asgs = self._filter_by_subnets(asgs, self.subnet_ids)
        return tree.Tree._tree_text(
            self, [], "Auto Scaling Groups:", asgs, self._asg_text
        )

    def _get_asgs(self):
        """Get all ASGs using boto3."""
        asgs = []

        client = boto3.client("autoscaling")
        paginator = client.get_paginator("describe_auto_scaling_groups")
        page_iterator = paginator.paginate()

        for page in page_iterator:
            asgs += page["AutoScalingGroups"]

        return asgs

    def _filter_by_subnets(self, asgs, vpc_subnet_ids):
        """Filter all ASGs by subnets in the virtual private cloud."""
        filtered_asgs = []
        for asg in asgs:
            asg_subnet_ids = asg["VPCZoneIdentifier"].split(",")
            if any(id in vpc_subnet_ids for id in asg_subnet_ids):
                filtered_asgs.append(asg)

        return filtered_asgs

    def _asg_text(self, prefix, asg):
        """Describe an ASG as a list of strings."""
        text_tree = []

        asg_arn = asg["AutoScalingGroupARN"]
        asg_name = asg["AutoScalingGroupName"]
        text_tree.append(f"{get_prefix(prefix)} {asg_arn} : {asg_name}")

        subnet_tree = tree.Tree._tree_text(
            self,
            prefix + [False],
            "Subnets:",
            asg["VPCZoneIdentifier"].split(","),
            self._subnet_text,
        )
        text_tree += subnet_tree

        instance_tree = tree.Tree._tree_text(
            self,
            prefix + [True],
            "Instances:",
            asg["Instances"],
            self._instance_text,
        )
        text_tree += instance_tree

        return text_tree

    def _subnet_text(self, prefix, subnet_id):
        """Describe a subnet linked to an ASG as a list of strings."""
        return [f"{get_prefix(prefix)} {subnet_id}"]

    def _instance_text(self, prefix, instance):
        """Describe an instance linked to an ASG as a list of strings."""
        return [f"{get_prefix(prefix)} {instance['InstanceId']}"]
