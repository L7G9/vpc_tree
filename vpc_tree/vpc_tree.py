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
    def display_vpc_list(self):
        list_generator = _VPCListGenerator()
        vpcs: _VPCListGenerator = list_generator.generate()
        for entry in vpcs:
            print(entry)

    def display_vpc_tree(self, vpd_id):
        tree_generator = _VPCTreeGenerator(vpd_id)
        text_tree: _VPCListGenerator = tree_generator.generate()
        for entry in text_tree:
            print(entry)


class _VPCListGenerator:
    def generate(self):
        vpcs = []

        client = boto3.client("ec2")
        vpc_response = client.describe_vpcs()
        for vpc in vpc_response["Vpcs"]:
            vpc_id = vpc["VpcId"]
            name = tags.get_tag_value(vpc["Tags"], "Name")
            vpcs.append(f"VPC : {name} : {vpc_id}")

        return vpcs


class _VPCTreeGenerator:
    def __init__(self, vpc_id):
        self._vpc_id = vpc_id

    def generate(self):
        text_tree = []

        vpc = self._get_vpc(self._vpc_id)
        text_tree.append(self._get_vpc_description(vpc))

        sgs = security_groups.SecurityGroups(self._vpc_id)
        sg_text_tree = sgs.generate()
        prefix.add_subtree_prefix(sg_text_tree, prefix.TEE, prefix.PIPE)
        text_tree += sg_text_tree

        sns = subnets.Subnets(self._vpc_id)
        subnet_text_tree = sns.generate()
        prefix.add_subtree_prefix(
            subnet_text_tree, prefix.TEE, prefix.PIPE
        )
        text_tree += subnet_text_tree

        lbs = load_balancers.LoadBalancers(self._vpc_id)
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

        # TODO: error check
        return response["Vpcs"][0]

    def _get_vpc_description(self, vpc):
        vpc_id = vpc["VpcId"]
        name = tags.get_tag_value(vpc["Tags"], "Name")
        cidr_block = vpc["CidrBlock"]
        return f"{vpc_id} : {name} : {cidr_block}"
