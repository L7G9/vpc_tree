# sg_tree.py
"""VPC Tree application's Security Group functionality."""

import boto3

from .prefix import get_prefix
from .text_tree import generate_tree


class SGTree:
    """Gets details of AWS Security Groups and represents them in a tree
    structure.

    Attributes:
        vpc_id: A string containing the Id of a Virtual Private Cloud.
    """

    def __init__(self, vpc_id):
        """Initializes instance.

        Args:
            vpc_id: A string containing the Id Virtual Private Cloud which all
            the Security Groups should be linked to.
        """
        self.vpc_id = vpc_id

    def generate(self):
        """Generate a text based tree describing all Security Groups linked to
        vpc_id.

        Returns:
            A list of strings containing the text based tree.
        """
        sgs = self._get_sgs()
        return generate_tree([], "Security Groups:", sgs, self._sg_text)

    def _get_sgs(self):
        """Get all Security Groups linked to vpc_id using Boto3."""
        sgs = []

        client = boto3.client("ec2")
        paginator = client.get_paginator("describe_security_groups")
        parameters = {
            "Filters": [
                {"Name": "vpc-id", "Values": [self.vpc_id]},
            ]
        }
        page_iterator = paginator.paginate(**parameters)
        for page in page_iterator:
            sgs += page["SecurityGroups"]

        return sgs

    def _sg_text(self, prefix_description, sg):
        """Describe a Security Group as a list of strings."""
        text_tree = []
        id = sg["GroupId"]
        name = sg["GroupName"]
        text_tree.append(f"{get_prefix(prefix_description)}{id} : {name}")

        ingress_tree = generate_tree(
            prefix_description + [False],
            "Ingress Permissions:",
            sg["IpPermissions"],
            self._permission_text)
        text_tree += ingress_tree

        egress_tree = generate_tree(
            prefix_description + [True],
            "Egress Permissions:",
            sg["IpPermissionsEgress"],
            self._permission_text)
        text_tree += egress_tree

        return text_tree

    def _permission_text(self, prefix_description, permission):
        """Describe a Security Group Permission as a list of strings"""
        text_tree = []
        prefix = get_prefix(prefix_description)
        protocol = permission["IpProtocol"]
        if protocol != "-1":
            from_port = permission["FromPort"]
            to_port = permission["ToPort"]
            text_tree.append(f"{prefix}{protocol} : {from_port} : {to_port}")
        else:
            text_tree.append(f"{prefix}All")

        ip_tree = generate_tree(
            prefix_description + [False],
            "IP Ranges:",
            permission["IpRanges"],
            self._permission_ip_range_text
        )
        text_tree += ip_tree

        sg_tree = generate_tree(
            prefix_description + [True],
            "Security Groups:",
            permission["UserIdGroupPairs"],
            self._permission_sg_text
        )
        text_tree += sg_tree

        return text_tree

    def _permission_ip_range_text(self, prefix_description, ip_range):
        """Describe an IP Range as a list of strings."""
        return [f"{get_prefix(prefix_description)}{ip_range['CidrIp']}"]

    def _permission_sg_text(self, prefix_description, group_pair):
        """Describe a Security Group linked to a Permission as a list of
        strings."""
        return [f"{get_prefix(prefix_description)}{group_pair['GroupId']}"]
