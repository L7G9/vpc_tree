# prefix.py
"""Constants and functions to provide the prefix string need to connect the
different elements of a text based tree structure together.

Uses a list of booleans to describe the structure of this prefix string.

The last boolean is used to indicate if the last part of the prefix is
an ELBOW or a TEE. True is used for ELBOW, when it is the last sibling
node in the subtree. False is used for TEE, when there are preceding
sibling nodes in a subtree.

The proceeding booleans are indicate when to use a PIPE or a SPACE in
the proceeding part the prefix. True is used for SPACE, when there are no
more sibling nodes in the same subtree. False is used for PIPE, when there
are more sibling nodes in the same subtree.

Examples.
- [False]            = "├──"
- [False, True]      = "│  └──"
- [True]             = "└──"
- [True, False]      = "   ├──"
- [True, True]       = "   └──"
- [True, True, True] = "      └──"
"""

ELBOW = "└──"
TEE = "├──"
PIPE = "│  "
SPACE = "   "


def elbow_or_tee(last_leaf_node):
    """Selects ELBOW or TEE.

    Args:
       last_leaf_node: A boolean set to True when adding the last sibling node
       in the subtree.

    Returns:
        A string which is either an ELBOW or TEE.
    """
    return ELBOW if last_leaf_node else TEE


def space_or_pipe(last_sub_tree):
    """Selects PIPE or SPACE.

    Args:
       last_sub_tree: A boolean set to True when there are no more sibling
       nodes in the same subtree.

    Returns:
        A string which is either an PIPE or SPACE.
    """
    return SPACE if last_sub_tree else PIPE


def get_prefix(prefix_description):
    """Selects PIPE or SPACE.

    Args:
        prefix_description: A list booleans describing the structure of a
        prefix string

    Returns:
        A string representing the prefix described by prefix_description.
    """
    prefix = ""

    for i in range(len(prefix_description)):
        leaf_node = i == len(prefix_description) - 1
        if leaf_node:
            prefix += elbow_or_tee(prefix_description[i])
        else:
            prefix += space_or_pipe(prefix_description[i])

    return prefix
