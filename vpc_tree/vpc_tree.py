# vpc_tree.py
"""VPC Tree main module."""

import boto3
from . import (
    asg_tree,
    aws_resources,
    lb_tree,
    sg_tree,
    subnet_tree,
    tags,
    tg_tree,
)


class VPCTree:
    """Provide output for VPCTree command line app."""

    def display_vpc_list(self):
        """Print a list of all Virtual Private Clouds."""
        vpcs = self._generate_vpc_list(aws_resources.get_vpcs())
        for entry in vpcs:
            print(entry)

    def display_vpc_tree(self, vpc_id):
        """Print a tree displaying the resources in a Virtual Private Cloud.

        Args:
            vpc_id: A string containing the Id of the Virtual Private Cloud to
            display.
        """
        text_tree = self._vpc_text(aws_resources.get_vpc(vpc_id))
        for entry in text_tree:
            print(entry)

    def _generate_vpc_list(self, vpcs):
        """Return a list of Virtual Private Clouds in AWS account."""
        text = []

        for vpc in vpcs:
            vpc_id = vpc["VpcId"]
            name = tags.get_tag_value(vpc, "Name")

            if name is None:
                text.append(f"{vpc_id}")
            else:
                text.append(f"{name} : {vpc_id}")

        return text

    def _vpc_text(self, vpc):
        """Describe Virtual Private Cloud as a list of strings."""
        text_tree = []

        text_tree.append(self._get_vpc_description(vpc))

        vpc_id = vpc["VpcId"]

        security_groups = aws_resources.get_security_groups(vpc_id)
        sg_tree_generator = sg_tree.SGTree(security_groups)
        sg_tree_generator.generate(text_tree, [False])

        subnets = aws_resources.get_subnets(vpc_id)
        instances = aws_resources.get_instances(vpc_id)
        subnet_tree_generator = subnet_tree.SubnetTree(subnets, instances)
        subnet_tree_generator.generate(text_tree, [False])

        load_balancers = aws_resources.get_load_balancers()
        load_balancers = aws_resources.filter_load_balancers_by_vpc(
            load_balancers, vpc_id
        )
        lb_tree_generator = lb_tree.LBTree(load_balancers)
        lb_tree_generator.generate(text_tree, [False])

        auto_scaling_groups = aws_resources.get_auto_scaling_groups()
        subnet_ids = aws_resources.get_subnet_ids(subnets)
        auto_scaling_groups = (
            aws_resources.filter_auto_scaling_groups_by_subnets(
                auto_scaling_groups, subnet_ids
            )
        )
        asg_tree_generator = asg_tree.ASGTree(auto_scaling_groups)
        asg_tree_generator.generate(text_tree, [False])

        load_balancer_arns = aws_resources.get_load_balancer_arns(
            load_balancers
        )
        target_groups = aws_resources.get_target_groups(load_balancer_arns)
        tg_tree_generator = tg_tree.TGTree(target_groups)
        tg_tree_generator.generate(text_tree, [True])

        return text_tree

    def _get_vpc(self, vpc_id):
        """Get Virtual Private Cloud linked to vpc_id."""
        client = boto3.client("ec2")
        response = client.describe_vpcs(
            VpcIds=[vpc_id],
        )
        return response["Vpcs"][0]

    def _get_vpc_description(self, vpc):
        """Get description of Virtual Private Cloud in vpc."""
        vpc_id = vpc["VpcId"]
        name = tags.get_tag_value(vpc["Tags"], "Name")
        cidr_block = vpc["CidrBlock"]
        if name is None:
            return f"{vpc_id} : {cidr_block}"
        else:
            return f"{vpc_id} : {name} : {cidr_block}"
