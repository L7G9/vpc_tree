# target_group_tree.py

import boto3
from prefix import get_prefix
import tree

class TargetGroupTree(tree.Tree):
    def __init__(self, load_balancer_arns):
        self.load_balancer_arns = load_balancer_arns

    def generate(self):
        target_groups = self._get_target_groups(self.load_balancer_arns)

        return tree.Tree._tree_text(
            self,
            [],
            'Target Groups:',
            target_groups,
            self._target_group_text
        )

    def _get_target_groups(self, load_balancer_arns):
        target_groups = []

        client = boto3.client('elbv2')
        paginator = client.get_paginator('describe_target_groups')

        for arn in load_balancer_arns:
            page_iterator = paginator.paginate(LoadBalancerArn=arn)
            for page in page_iterator:
                target_groups += page['TargetGroups']

        return target_groups

    def _target_group_text(self, prefix_list, target_group):
        text_tree = []

        arn = target_group['TargetGroupArn']
        name = target_group['TargetGroupName']
        prefix = get_prefix(prefix_list)
        text_tree.append(f"{prefix}{arn} : {name}")

        load_balancer_arns = target_group['LoadBalancerArns']
        if len(load_balancer_arns) > 0:
            text_tree += tree.Tree._tree_text(
                self,
                prefix_list + [True],
                'Load Balanacers:',
                load_balancer_arns,
                self._load_balancer_text
            )

        return text_tree

    def _load_balancer_text(self, prefix_list, load_balancer_arn):
        return [f"{get_prefix(prefix_list)}{load_balancer_arn}"]
