# text_tree.py
"""Helper functions to create a generic text based tree."""

from .prefix import get_prefix


def add_tree(text_tree, prefix_description, heading, items, item_function):
    """Add tree description to a list of strings.

    Args:
        text_tree: A list of strings to add this tree to.
        prefix_description: A list of booleans describing a common prefix to
        be added to all strings is this text tree.
        heading: A string containing a heading to give this tree.
        items: A list of dictionaries containing AWS resources.
        item_function: a function that takes a dictionary from items and
        describes it as a list of strings.
    """
    text_tree.append(f"{get_prefix(prefix_description)}{heading}")
    item_count = len(items)
    for i in range(item_count):
        last_item = i == item_count - 1
        item_function(text_tree, prefix_description + [last_item], items[i])


def add_node(text_tree, prefix_description, string):
    """Add node description to a list of strings.

    Args:
        text_tree: A list of strings to add this string to.
        prefix_description: A list of booleans describing the prefix to be
        added to this node.
        string: A string describing the node.
    """
    text_tree.append(f"{get_prefix(prefix_description)}{string}")
