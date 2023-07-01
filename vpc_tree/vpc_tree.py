# vpc_tree.py

"""This module provides VPC Tree main module."""

import boto3


PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class VPCTree:
  def __init__(self, vpc_arn):
    self._generator = _TreeGenerator(vpc_arn)

  def generate(self):
    tree = self._generator.build_tree()
    for entry in tree:
      print(entry)

class _TreeGenerator:
  def __init__(self, vpc_arn):
    self._tree[]

  def build_tree(self):
    self._vpc()

  def _vpc(self):
    # add details of vpc to tree
    # for each subnet in vpc
    #   _subnet()
    pass

  def _subnet(self):
    # add details of subnet to tree
    # for each EC2 instance in subnet
    #   _instance()
    pass

  def _instance(self):
    # add details of instance to tree
    pass
