# sg_tree.py
"""VPC Tree application's Security Group functionality."""

import boto3

from .prefix import get_prefix
from .text_tree import add_tree


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

    def generate(self, text_tree, prefix_description):
        """Generate a text based tree describing all Security Groups linked to
        vpc_id.

        Args:
            text_tree: A list of strings to add this subtree to.
            prefix_description: A list of booleans describing a common prefix
            to be added to all strings is this text tree.
        """
        add_tree(
            text_tree,
            prefix_description,
            "Security Groups:",
            self._get_sgs(),
            self._add_sg_tree,
        )

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

    def _add_sg_tree(self, text_tree, prefix_description, sg):
        """Adds tree describing Security Group to text_tree."""
        id = sg["GroupId"]
        name = sg["GroupName"]
        text_tree.append(f"{get_prefix(prefix_description)}{id} : {name}")

        add_tree(
            text_tree,
            prefix_description + [False],
            "Ingress Permissions:",
            sg["IpPermissions"],
            self._add_permission_tree,
        )

        add_tree(
            text_tree,
            prefix_description + [True],
            "Egress Permissions:",
            sg["IpPermissionsEgress"],
            self._add_permission_tree,
        )

    def _add_permission_tree(self, text_tree, prefix_description, permission):
        """Adds tree describing Security Group Permission to text_tree."""
        prefix = get_prefix(prefix_description)
        protocol = permission["IpProtocol"]
        if protocol != "-1":
            from_port = permission["FromPort"]
            to_port = permission["ToPort"]
            text_tree.append(f"{prefix}{protocol} : {from_port} : {to_port}")
        else:
            text_tree.append(f"{prefix}All")

        ip_ranges = permission["IpRanges"]
        user_id_group_pairs = permission["UserIdGroupPairs"]

        if len(ip_ranges) > 0:
            is_last_sub_tree = len(user_id_group_pairs) == 0
            add_tree(
                text_tree,
                prefix_description + [is_last_sub_tree],
                "IP Ranges:",
                ip_ranges,
                self._add_ip_range_node,
            )

        if len(user_id_group_pairs) > 0:
            add_tree(
                text_tree,
                prefix_description + [True],
                "Security Groups:",
                user_id_group_pairs,
                self._add_sg_node,
            )

    def _add_ip_range_node(self, text_tree, prefix_description, ip_range):
        """Adds IP Range of Permission to text_tree."""
        text_tree.append(
            f"{get_prefix(prefix_description)}{ip_range['CidrIp']}"
        )

    def _add_sg_node(self, text_tree, prefix_description, group_pair):
        """Adds Security Group Id of Permission to text_tree."""
        text_tree.append(
            f"{get_prefix(prefix_description)}{group_pair['GroupId']}"
        )
