# lb_tree.py

import boto3
from prefix import get_prefix
import tree


class LBTree(tree.Tree):
    def __init__(self, vpc_id):
        self.vpc_id = vpc_id

    def generate(self):
        self.load_balancers = self._get_lbs()
        self.load_balancers = self._filter_by_vpc(self.load_balancers, self.vpc_id)

        return tree.Tree._tree_text(
            self,
            [],
            'Load Balancers:',
            self.load_balancers,
            self._lb_text
        )

    def _get_lbs(self):
        lbs = []

        client = boto3.client('elbv2')
        paginator = client.get_paginator('describe_load_balancers')
        page_iterator = paginator.paginate()

        for page in page_iterator:
            lbs += page['LoadBalancers']

        return lbs

    def _filter_by_vpc(self, lbs, vpc_id):
        return list(
            filter(lambda d: d['VpcId'] == vpc_id, lbs)
        )

    def _lb_text(self, prefix, lb):
        text_tree = []
        arn = lb['LoadBalancerArn']
        name = lb['LoadBalancerName']
        text_tree.append(f"{get_prefix(prefix)} {arn} : {name}")

        az_tree = tree.Tree._tree_text(
            self,
            prefix + [False],
            'Availability Zones:',
            lb['AvailabilityZones'],
            self._az_text
        )
        text_tree += az_tree

        sg_tree = tree.Tree._tree_text(
            self,
            prefix + [True],
            'Security Groups:',
            lb['SecurityGroups'],
            self._sg_text
        )
        text_tree += sg_tree

        return text_tree

    def _az_text(self, prefix, az):
        zone = az['ZoneName']
        subnet_id = az['SubnetId']
        return [f"{get_prefix(prefix)}{zone} : {subnet_id}"]

    def _sg_text(self, prefix, sg):
        return [f"{get_prefix(prefix)}{sg}"]
