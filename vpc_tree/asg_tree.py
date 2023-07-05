# asg_tree.py

"""This module provides VPC Tree main module."""

import boto3
import pprint
from prefix import prefix


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

    def filter_by_subnets(self, asgs, subnet_ids):
        filtered_asgs = []
        for asg in asgs:
            if any(subnet_id in subnet_ids for subnet_id in asg['VPCZoneIdentifier'].split(',')):
                filtered_asgs.append(asg)

        return filtered_asgs

    def asg_tree(self, asgs):
        tree = []

        tree.append(f"Auto Scaling Groups:")
        asg_count = len(asgs)
        for i in range(asg_count):
            asg = asgs[i]
            last_asg = i == asg_count-1
            tree.append(f"{prefix([last_asg])} {asg['AutoScalingGroupARN']} : {asg['AutoScalingGroupName']}")

            tree.append(f"{prefix([last_asg, False])} Subnets:")
            subnet_ids = asg['VPCZoneIdentifier'].split(',')
            subnet_count = len(subnet_ids)
            for j in range(subnet_count):
                last_subnet = j == subnet_count-1
                tree.append(f"{prefix([last_asg, False, last_subnet])} {subnet_ids[j]}")

            tree.append(f"{prefix([last_asg, True])} Instances:")
            instances = asg['Instances']
            instance_count = len(instances)
            for k in range(instance_count):
                last_instance = k == instance_count-1
                tree.append(f"{prefix([last_asg, True, last_instance])} {instances[k]['InstanceId']}")

        return tree
