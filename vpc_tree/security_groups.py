# security_groups.py

import boto3
from prefix import get_prefix
import tree


class SecurityGroups(tree.Tree):
    """AWS Security Groups.

    Subclass of tree.Tree with the functionality to get details of security
       groups from boto3 and display them as a text based tree.

    Attributes:
        vpc_id: A string containing the id of a virtual private cloud.
    """
    def __init__(self, vpc_id):
        """Initializes instance.

        Args:
            vpc_id: A string containing the id virtual private cloud which all
                the security groups should be linked to.
        """
        self.vpc_id = vpc_id

    def generate(self):
        """Generate a text based tree describing all security groups linked to
            vpc_id.

        Returns:
            A list of strings containing the text based tree.
        """
        sgs = self._get_sgs()
        return tree.Tree._tree_text(
            self, [], "Security Groups:", sgs, self._sg_text
        )

    def _get_sgs(self):
        """Get all security groups linked to vpc_id using boto3."""
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

    def _sg_text(self, prefix, sg):
        """Describe a security group as a list of strings."""
        id = sg["GroupId"]
        name = sg["GroupName"]
        return [f"{get_prefix(prefix)}{id} : {name}"]
