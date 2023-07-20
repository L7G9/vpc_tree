# asg_tree.py
"""VPC Tree application's Auto Scale Group functionality."""

from .prefix import get_prefix
from .text_tree import add_node, add_tree


class ASGTree:
    """Generates a text tree representation of AWS Auto Scaling Groups.

    Attributes:
        auto_scaling_groups: A list of dictionaries containing Auto Scaling
        Groups from Boto3.
    """

    def __init__(self, auto_scaling_groups):
        """Initializes instance.

        Args:
            auto_scaling_groups: A list of dictionaries containing Auto
            Scaling Groups from Boto3.
        """
        self.auto_scaling_groups = auto_scaling_groups

    def generate(self, text_tree, prefix_description):
        """Generate a text based tree describing the Auto Scaling Groups.

        Args:
            text_tree: A list of strings to add this subtree to.
            prefix_description: A list of booleans describing a common prefix
            to be added to all strings is this text tree.
        """
        add_tree(
            text_tree,
            prefix_description,
            "Auto Scaling Groups:",
            self.auto_scaling_groups,
            self._add_asg_tree,
        )

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
