# vpc_tree.py
"""VPC Tree main module."""

import boto3

from . import asg_tree, lb_tree, prefix, sg_tree, subnet_tree, tags, tg_tree


class VPCTree:
    """Provide output for VPCTree command line app."""

    def display_vpc_list(self):
        """Print a list of all Virtual Private Clouds."""
        vpcs = self._generate_vpc_list()
        for entry in vpcs:
            print(entry)

    def display_vpc_tree(self, vpc_id):
        """Print a tree displaying the resources in a Virtual Private Cloud.

        Args:
            vpc_id: A string containing the Id of the Virtual Private Cloud to
            display.
        """
        text_tree = self._vpc_text(vpc_id)
        for entry in text_tree:
            print(entry)

    def _generate_vpc_list(self):
        """Return a list of Virtual Private Clouds in AWS account."""
        vpcs = []

        client = boto3.client('ec2')
        vpc_response = client.describe_vpcs()
        for vpc in vpc_response['Vpcs']:
            vpc_id = vpc['VpcId']
            name = tags.get_tag_value(vpc['Tags'], 'Name')
            if name is None:
                vpcs.append(f"VPC : {vpc_id}")
            else:
                vpcs.append(f"VPC : {name} : {vpc_id}")

        return vpcs

    def _vpc_text(self, vpc_id):
        """Describe Virtual Private Cloud as a list of strings."""
        text_tree = []

        vpc = self._get_vpc(vpc_id)
        text_tree.append(self._get_vpc_description(vpc))

        sg_tree_generator = sg_tree.SGTree(vpc_id)
        sg_text_tree = sg_tree_generator.generate()
        prefix.add_subtree_prefix(sg_text_tree, prefix.TEE, prefix.PIPE)
        text_tree += sg_text_tree

        subnet_tree_generator = subnet_tree.SubnetTree(vpc_id)
        subnet_text_tree = subnet_tree_generator.generate()
        prefix.add_subtree_prefix(subnet_text_tree, prefix.TEE, prefix.PIPE)
        text_tree += subnet_text_tree

        lb_tree_generator = lb_tree.LBTree(vpc_id)
        lb_text_tree = lb_tree_generator.generate()
        prefix.add_subtree_prefix(lb_text_tree, prefix.TEE, prefix.PIPE)
        text_tree += lb_text_tree

        subnet_ids = []
        for subnet in subnet_tree_generator.subnets:
            subnet_ids.append(subnet['SubnetId'])

        asg_tree_generator = asg_tree.ASGTree(subnet_ids)
        asg_text_tree = asg_tree_generator.generate()
        prefix.add_subtree_prefix(asg_text_tree, prefix.TEE, prefix.PIPE)
        text_tree += asg_text_tree

        load_balancer_arns = []
        for load_balancer in lb_tree_generator.load_balancers:
            load_balancer_arns.append(load_balancer['LoadBalancerArn'])

        tg_tree_generator = tg_tree.TGTree(load_balancer_arns)
        tg_text_tree = tg_tree_generator.generate()
        prefix.add_subtree_prefix(tg_text_tree, prefix.ELBOW, prefix.SPACE)
        text_tree += tg_text_tree

        return text_tree

    def _get_vpc(self, vpc_id):
        """Get Virtual Private Cloud linked to vpc_id."""
        client = boto3.client('ec2')
        response = client.describe_vpcs(
            VpcIds=[vpc_id],
        )
        return response['Vpcs'][0]

    def _get_vpc_description(self, vpc):
        """Get description of Virtual Private Cloud in vpc."""
        vpc_id = vpc['VpcId']
        name = tags.get_tag_value(vpc['Tags'], 'Name')
        cidr_block = vpc['CidrBlock']
        if name is None:
            return f"{vpc_id} : {cidr_block}"
        else:
            return f"{vpc_id} : {name} : {cidr_block}"
