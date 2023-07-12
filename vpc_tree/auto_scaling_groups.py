# auto_scaling_groups.py

"""This module provides ASG Tree main module."""

import boto3
from prefix import get_prefix
import tree


class AutoScalingGroups(tree.Tree):
    def __init__(self, subnet_ids):
        self.subnet_ids = subnet_ids

    def generate(self):
        asgs = self._get_asgs()
        asgs = self._filter_by_subnets(asgs, self.subnet_ids)
        return tree.Tree._tree_text(
            self, [], "Auto Scaling Groups:", asgs, self._asg_text
        )

    def _get_asgs(self):
        asgs = []

        client = boto3.client("autoscaling")
        paginator = client.get_paginator("describe_auto_scaling_groups")
        page_iterator = paginator.paginate()

        for page in page_iterator:
            asgs += page["AutoScalingGroups"]

        return asgs

    def _filter_by_subnets(self, asgs, vpc_subnet_ids):
        filtered_asgs = []
        for asg in asgs:
            asg_subnet_ids = asg["VPCZoneIdentifier"].split(",")
            if any(id in vpc_subnet_ids for id in asg_subnet_ids):
                filtered_asgs.append(asg)

        return filtered_asgs

    def _asg_text(self, prefix, asg):
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
        return [f"{get_prefix(prefix)} {subnet_id}"]

    def _instance_text(self, prefix, instance):
        return [f"{get_prefix(prefix)} {instance['InstanceId']}"]
