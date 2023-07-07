# vpc_tree.py

"""This module provides VPC Tree main module."""

import boto3
import pprint

from sg_tree import SGTree
from subnet_tree import SubnetTree
from lb_tree import LBTree
from asg_tree import ASGTree
from target_group_tree import TargetGroupTree

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


def _elbow_or_tree(last_node):
    return ELBOW if last_node else TEE


def _space_or_pipe(last_node):
    return SPACE_PREFIX if last_node else PIPE_PREFIX


def _prefix(last_nodes):
    prefix = ''

    for i in range(len(last_nodes)):
        leaf_node = i == len(last_nodes)-1
        if leaf_node:
            prefix += _elbow_or_tree(last_nodes[i])
        else:
            prefix += _space_or_pipe(last_nodes[i])

    return prefix


def _get_tag(tags, key):
    return next(filter(lambda d: d.get("Key") == key, tags), None)


def _get_tag_value(tags, key):
    tag = _get_tag(tags, key)
    if tag is not None:
        return tag['Value']
    return None


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
            name = _get_tag_value(vpc['Tags'], 'Name')
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
        name = _get_tag_value(vpc['Tags'], 'Name')
        cidr_block = vpc['CidrBlock']
        return f"{vpc_id} : {name} : {cidr_block}"


    def _vpc(self):
        vpc = self._get_vpc(self._vpc_id)
        self._tree.append(self._get_vpc_description(vpc))

        sg_tree = SGTree(self._vpc_id)
        self._tree += sg_tree.generate()

        subnet_tree = SubnetTree(self._vpc_id)
        self._tree += subnet_tree.generate()

        lb_tree = LBTree(self._vpc_id)
        self._tree += lb_tree.generate()

        subnet_ids = []
        for subnet in subnet_tree.subnets:
            subnet_ids.append(subnet['SubnetId'])
        asg_tree = ASGTree(subnet_ids)
        self._tree += asg_tree.generate()

        load_balancer_arns = []
        for load_balancer in lb_tree.load_balancers:
            load_balancer_arns.append(load_balancer['LoadBalancerArn'])
        target_group_tree = TargetGroupTree(load_balancer_arns)
        self._tree += target_group_tree.generate()


if __name__ == "__main__":
    vpc_tree = VPCTree("vpc-0135e5d4f0ba2e477")
    vpc_tree.generate()
