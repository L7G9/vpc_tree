# vpc_tree.py
"""This module provides VPC Tree main module."""

import boto3
from . import prefix
from . import tags
from . import security_groups
from . import subnets
from . import load_balancers
from . import auto_scaling_groups
from . import target_groups


class VPCTree:
    """Provide output for VPCTree comand line app."""
    def display_vpc_list(self):
        """Print a list of all VPCs."""
        vpcs = self._generate_vpc_list()
        for entry in vpcs:
            print(entry)

    def display_vpc_tree(self, vpc_id):
        """Print a tree displaying the resources in a VPC.

        Args:
            vpc_id: A string containing the id of the VPC to display.
        """
        text_tree = self._generate_vpc_tree(vpc_id)
        for entry in text_tree:
            print(entry)

    def _generate_vpc_list(self):
        """Return a list of VPCs in AWS account."""
        vpcs = []

        client = boto3.client("ec2")
        vpc_response = client.describe_vpcs()
        for vpc in vpc_response["Vpcs"]:
            vpc_id = vpc["VpcId"]
            name = tags.get_tag_value(vpc["Tags"], "Name")
            if name is None:
                vpcs.append(f"VPC : {vpc_id}")
            else:
                vpcs.append(f"VPC : {name} : {vpc_id}")

        return vpcs

    def _generate_vpc_tree(self, vpc_id):
        text_tree = []

        vpc = self._get_vpc(vpc_id)
        text_tree.append(self._get_vpc_description(vpc))

        sgs = security_groups.SecurityGroups(vpc_id)
        sg_text_tree = sgs.generate()
        prefix.add_subtree_prefix(sg_text_tree, prefix.TEE, prefix.PIPE)
        text_tree += sg_text_tree

        sns = subnets.Subnets(vpc_id)
        subnet_text_tree = sns.generate()
        prefix.add_subtree_prefix(
            subnet_text_tree, prefix.TEE, prefix.PIPE
        )
        text_tree += subnet_text_tree

        lbs = load_balancers.LoadBalancers(vpc_id)
        load_balancer_text_tree = lbs.generate()
        prefix.add_subtree_prefix(
            load_balancer_text_tree, prefix.TEE, prefix.PIPE
        )
        text_tree += load_balancer_text_tree

        subnet_ids = []
        for subnet in sns.subnets:
            subnet_ids.append(subnet["SubnetId"])

        asgs = auto_scaling_groups.AutoScalingGroups(subnet_ids)
        auto_scaling_group_text_tree = asgs.generate()
        prefix.add_subtree_prefix(
            auto_scaling_group_text_tree, prefix.TEE, prefix.PIPE
        )
        text_tree += auto_scaling_group_text_tree

        load_balancer_arns = []
        for load_balancer in lbs.load_balancers:
            load_balancer_arns.append(load_balancer["LoadBalancerArn"])

        tgs = target_groups.TargetGroups(load_balancer_arns)
        target_group_text_tree = tgs.generate()
        prefix.add_subtree_prefix(
            target_group_text_tree, prefix.ELBOW, prefix.SPACE
        )
        text_tree += target_group_text_tree

        return text_tree

    def _get_vpc(self, vpc_id):
        client = boto3.client("ec2")
        response = client.describe_vpcs(
            VpcIds=[
                vpc_id
            ],
        )
        return response["Vpcs"][0]

    def _get_vpc_description(self, vpc):
        vpc_id = vpc["VpcId"]
        name = tags.get_tag_value(vpc["Tags"], "Name")
        cidr_block = vpc["CidrBlock"]
        if name is None:
            return f"{vpc_id} : {cidr_block}"
        else:
            return f"{vpc_id} : {name} : {cidr_block}"
