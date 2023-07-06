# sg_tree.py

import boto3
from prefix import get_prefix
import tree


class SGTree(tree.Tree):
    def __init__(self, vpc_id):
        self.vpc_id = vpc_id

    def generate(self):
        sgs = self._get_sgs()
        return tree.Tree._tree_text(
            self,
            [],
            'Security Groups:',
            sgs,
            self._sg_text
        )

    def _get_sgs(self):
        sgs = []

        client = boto3.client('ec2')
        paginator = client.get_paginator('describe_security_groups')
        parameters = {
            'Filters': [
                {
                    'Name': 'vpc-id',
                    'Values': [self.vpc_id]
                },
            ]
        }
        page_iterator = paginator.paginate(**parameters)
        for page in page_iterator:
            sgs += page['SecurityGroups']

        return sgs

    def _sg_text(self, prefix, sg):
        id = sg['GroupId']
        name = sg['GroupName']
        return [f"{get_prefix(prefix)}{id} : {name}"]
