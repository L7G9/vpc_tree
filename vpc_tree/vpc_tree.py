# vpc_tree.py

"""This module provides VPC Tree main module."""

import boto3
import pprint
import prefix
import tags
from sg_tree import SGTree
from subnet_tree import SubnetTree
from lb_tree import LBTree
from asg_tree import ASGTree
from target_group_tree import TargetGroupTree

class VPCTree:
    def __init__(self, vpc_id):
        self._generator = _TreeGenerator(vpc_id)

    def generate(self):
        tree = self._generator.build_tree()
        for entry in tree:
            print(entry)


class _TreeGenerator:
    def __init__(self, vpc_id):
        self._tree = []
        self._vpc_id = vpc_id
        self._client = boto3.client('ec2')

    def build_tree(self):
        self._vpcs()
        self._vpc()
        return self._tree

    def _vpcs(self):
        vpc_response = self._client.describe_vpcs()
        for vpc in vpc_response['Vpcs']:
            vpc_id = vpc['VpcId']
            name = tags.get_tag_value(vpc['Tags'], 'Name')
            print(f"VPC : {name} : {vpc_id}")

    def _get_vpc(self, vpc_id):
        response = self._client.describe_vpcs(
            VpcIds=[
                self._vpc_id,
            ],
        )

        # TODO: error check
        return response['Vpcs'][0]

    def _get_vpc_description(self, vpc):
        vpc_id = vpc['VpcId']
        name = tags.get_tag_value(vpc['Tags'], 'Name')
        cidr_block = vpc['CidrBlock']
        return f"{vpc_id} : {name} : {cidr_block}"


    def _vpc(self):
        vpc = self._get_vpc(self._vpc_id)
        self._tree.append(self._get_vpc_description(vpc))

        sg_tree = SGTree(self._vpc_id)
        sg_text_tree = sg_tree.generate()
        prefix.add_subtree_prefix(sg_text_tree, prefix.TEE, prefix.PIPE_PREFIX)
        self._tree += sg_text_tree

        subnet_tree = SubnetTree(self._vpc_id)
        subnet_text_tree = subnet_tree.generate()
        prefix.add_subtree_prefix(subnet_text_tree, prefix.TEE, prefix.PIPE_PREFIX)
        self._tree += subnet_text_tree

        lb_tree = LBTree(self._vpc_id)
        load_balancer_text_tree = lb_tree.generate()
        prefix.add_subtree_prefix(load_balancer_text_tree, prefix.TEE, prefix.PIPE_PREFIX)
        self._tree += load_balancer_text_tree

        subnet_ids = []
        for subnet in subnet_tree.subnets:
            subnet_ids.append(subnet['SubnetId'])

        asg_tree = ASGTree(subnet_ids)
        auto_scaling_group_text_tree = asg_tree.generate()
        prefix.add_subtree_prefix(auto_scaling_group_text_tree, prefix.TEE, prefix.PIPE_PREFIX)
        self._tree += auto_scaling_group_text_tree

        load_balancer_arns = []
        for load_balancer in lb_tree.load_balancers:
            load_balancer_arns.append(load_balancer['LoadBalancerArn'])

        target_group_tree = TargetGroupTree(load_balancer_arns)
        target_group_text_tree = target_group_tree.generate()
        prefix.add_subtree_prefix(target_group_text_tree, prefix.ELBOW, prefix.SPACE_PREFIX)
        self._tree += target_group_text_tree


if __name__ == "__main__":
    vpc_tree = VPCTree("vpc-0135e5d4f0ba2e477")
    vpc_tree.generate()
