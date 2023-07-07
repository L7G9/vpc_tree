# prefix.py

"""This module provides VPC Tree main module."""

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


def elbow_or_tree(last_node):
    return ELBOW if last_node else TEE


def space_or_pipe(last_node):
    return SPACE_PREFIX if last_node else PIPE_PREFIX


def get_prefix(last_nodes):
    prefix = ''

    for i in range(len(last_nodes)):
        leaf_node = i == len(last_nodes)-1
        if leaf_node:
            prefix += elbow_or_tree(last_nodes[i])
        else:
            prefix += space_or_pipe(last_nodes[i])

    return prefix

def prefix_list(prefix, list):
    for item in list:
        item = prefix + item

def add_subtree_prefix(text_tree, root_prefix, branch_prefix):
    text_tree[0] = root_prefix + text_tree[0]
    for i in range(1, len(text_tree)):
        text_tree[i] = branch_prefix + text_tree[i]
