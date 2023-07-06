# asg_tree.py

"""This module provides VPC Tree main module."""

import boto3
from prefix import get_prefix


class ASGTree:
    def __init__(self, subnet_ids):
        self.subnet_ids = subnet_ids

    def get_asgs(self):
        asgs = []

        client = boto3.client('autoscaling')
        paginator = client.get_paginator('describe_auto_scaling_groups')
        page_iterator = paginator.paginate()

        for page in page_iterator:
            asgs += page['AutoScalingGroups']

        return asgs

    def filter_by_subnets(self, asgs, vpc_subnet_ids):
        filtered_asgs = []
        for asg in asgs:
            asg_subnet_ids = asg['VPCZoneIdentifier'].split(',')
            if any(id in vpc_subnet_ids for id in asg_subnet_ids):
                filtered_asgs.append(asg)

        return filtered_asgs

    def _make_tree(self, prefix_start, heading, items, item_function):
        tree = []
        tree.append(f"{get_prefix(prefix_start)}{heading}")
        item_count = len(items)
        for i in range(item_count):
            last_item = i == item_count-1
            tree += item_function(prefix_start + [last_item], items[i])

        return tree

    def _get_asg(self, prefix, asg):
        tree = []

        asg_arn = asg['AutoScalingGroupARN']
        asg_name = asg['AutoScalingGroupName']
        tree.append(f"{get_prefix(prefix)} {asg_arn} : {asg_name}")

        subnet_tree = self._make_tree(
            prefix + [False],
            'Subnets:',
            asg['VPCZoneIdentifier'].split(','),
            self._get_subnet
        )
        tree += subnet_tree

        instance_tree = self._make_tree(
            prefix + [True],
            'Instances:',
            asg['Instances'],
            self._get_instance
        )
        tree += instance_tree

        return tree

    def _get_subnet(self, prefix, subnet_id):
        return [f"{get_prefix(prefix)} {subnet_id}"]

    def _get_instance(self, prefix, instance):
        return [f"{get_prefix(prefix)} {instance['InstanceId']}"]

    def asg_tree(self, asgs):
        return self._make_tree(
            [],
            'Auto Scaling Groups:',
            asgs,
            self._get_asg
        )
