# asg_tree.py
"""VPC Tree application's Auto Scale Group functionality."""

import boto3

from .prefix import get_prefix
from .text_tree import add_node, add_tree


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

    def generate(self, text_tree, prefix_description):
        """Generate a text based tree describing all the Auto Scaling Groups
        linked to the Subnets in subnet_ids.

        Args:
            text_tree: A list of strings to add this subtree to.
            prefix_description: A list of booleans describing a common prefix
            to be added to all strings is this text tree.
        """
        add_tree(
            text_tree,
            prefix_description,
            "Auto Scaling Groups:",
            self._filter_by_subnets(self._get_asgs(), self.subnet_ids),
            self._add_asg_tree,
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

    def _add_asg_tree(self, text_tree, prefix_description, asg):
        """Adds tree describing Auto Scaling Group to text_tree."""
        arn = asg["AutoScalingGroupARN"]
        name = asg["AutoScalingGroupName"]
        text_tree.append(f"{get_prefix(prefix_description)}{arn} : {name}")

        sub_prefix_1 = get_prefix(prefix_description + [False])
        sub_prefix_2 = get_prefix(prefix_description + [False] + [True])

        min = asg["MinSize"]
        max = asg["MaxSize"]
        text_tree.append(f"{sub_prefix_1}MinSize = {min} : MaxSize = {max}")

        if "LaunchConfigurationName" in asg:
            text_tree.append(f"{sub_prefix_1}Launch Configuration")
            text_tree.append(f"{sub_prefix_2}{asg['LaunchConfigurationName']}")

        if "LaunchTemplate" in asg:
            text_tree.append(f"{sub_prefix_1}Launch Template")
            id = asg["LaunchTemplate"]["LaunchTemplateId"]
            text_tree.append(f"{sub_prefix_2}{id}")

        if "MixedInstancesPolicy" in asg:
            text_tree.append(f"{sub_prefix_1}Mixed Instances Policy")
            id = asg["MixedInstancesPolicy"]["LaunchTemplate"][
                "LaunchTemplateSpecification"
            ]["LaunchTemplateId"]
            text_tree.append(f"{sub_prefix_2}{id}")

        add_tree(
            text_tree,
            prefix_description + [False],
            "Subnets:",
            asg["VPCZoneIdentifier"].split(","),
            add_node,
        )

        add_tree(
            text_tree,
            prefix_description + [False],
            "Instances:",
            asg["Instances"],
            self._add_instance_node,
        )

        add_tree(
            text_tree,
            prefix_description + [False],
            "Load Balancers:",
            asg["LoadBalancerNames"],
            add_node,
        )

        add_tree(
            text_tree,
            prefix_description + [True],
            "Target Groups:",
            asg["TargetGroupARNs"],
            add_node,
        )

    def _add_instance_node(self, text_tree, prefix_description, instance):
        """Adds Id of Instance linked to Auto Scaling Group to text_tree."""
        text_tree.append(
            f"{get_prefix(prefix_description)}{instance['InstanceId']}"
        )
