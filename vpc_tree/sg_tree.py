# sg_tree.py

import boto3
from .prefix import get_prefix
from .text_tree import generate_tree


class SGTree():
    """Get deails of AWS Security Groups and represents them in a tree structure..

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
        return generate_tree(
            self, [], 'Security Groups:', sgs, self._sg_text
        )

    def _get_sgs(self):
        """Get all Security Groups linked to vpc_id using Boto3."""
        sgs = []

        client = boto3.client('ec2')
        paginator = client.get_paginator('describe_security_groups')
        parameters = {
            'Filters': [
                {'Name': 'vpc-id', 'Values': [self.vpc_id]},
            ]
        }
        page_iterator = paginator.paginate(**parameters)
        for page in page_iterator:
            sgs += page['SecurityGroups']

        return sgs

    def _sg_text(self, prefix_description, sg):
        """Describe a Security Group as a list of strings."""
        id = sg['GroupId']
        name = sg['GroupName']
        return [f"{get_prefix(prefix_description)}{id} : {name}"]
