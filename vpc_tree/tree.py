# tree.py

"""This module provides Tree main module."""

from prefix import get_prefix


class Tree:
    def _tree_text(self, prefix_start, heading, items, item_function):
        tree = []
        tree.append(f"{get_prefix(prefix_start)}{heading}")
        item_count = len(items)
        for i in range(item_count):
            last_item = i == item_count - 1
            tree += item_function(prefix_start + [last_item], items[i])

        return tree
