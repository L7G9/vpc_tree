# sg_tree.py
"""VPC Tree application's Security Group functionality."""

from .prefix import get_prefix
from .text_tree import add_tree


class SGTree:
    """Generates a text tree representation of AWS Security Groups.

    Attributes:
        security_groups: A list of dictionaries containing Security Groups
        from Boto3.
    """

    def __init__(self, security_groups):
        """Initializes instance.

        Args:
            security_groups: A list of dictionaries containing Security Groups
            from Boto3.
        """
        self.security_groups = security_groups

    def generate(self, text_tree, prefix_description):
        """Generate a text based tree describing the Security Groups.

        Args:
            text_tree: A list of strings to add this subtree to.
            prefix_description: A list of booleans describing a common prefix
            to be added to all strings is this text tree.
        """
        add_tree(
            text_tree,
            prefix_description,
            "Security Groups:",
            self.security_groups,
            self._add_sg_tree,
        )

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
