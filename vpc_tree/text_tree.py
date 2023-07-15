# text_tree.py
"""Help function to create a generic text based tree."""

from .prefix import get_prefix


def generate_tree(prefix_description, heading, items, item_function):
    """Create a text based tree.
    Args:
        prefix_description: A list of booleans describing a common prefix to
        be added to all strings is this text tree.
        heading: A string containing a heading to give this tree.
        items: A list of dictionaries containing AWS resources.
        item_function: a function that takes a dictionary from items and
        describes it as a list of strings.

     Returns:
        A list of strings containing the text based tree.
    """
    tree = []
    tree.append(f"{get_prefix(prefix_description)}{heading}")
    item_count = len(items)
    for i in range(item_count):
        last_item = i == item_count - 1
        tree += item_function(prefix_description + [last_item], items[i])

    return tree
