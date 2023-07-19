# test_text_tree.py

import pytest
from vpc_tree.text_tree import add_node, add_tree


@pytest.fixture(scope="class")
def heading():
    return "Tree Heading"


@pytest.fixture(scope="class")
def nodes():
    return ["Node 1", "Node 2", "Node 3", "Node 4"]


@pytest.fixture(scope="class")
def prefix_definition():
    return [False, True]


@pytest.mark.usefixtures("prefix_definition", "nodes")
class TestAddNode:
    def test_add_node(self, prefix_definition, nodes):
        text_tree = []
        add_node(text_tree, prefix_definition, nodes[0])
        assert len(text_tree) == 1
        assert text_tree[0] == "│  └──Node 1"


@pytest.mark.usefixtures("prefix_definition", "heading", "nodes")
class TestAddTree:
    def test_add_tree(self, prefix_definition, heading, nodes):
        text_tree = []
        add_tree(text_tree, prefix_definition, heading, nodes, add_node)
        assert len(text_tree) == 5
        assert text_tree[0] == "│  └──Tree Heading"
        assert text_tree[1] == "│     ├──Node 1"
        assert text_tree[2] == "│     ├──Node 2"
        assert text_tree[3] == "│     ├──Node 3"
        assert text_tree[4] == "│     └──Node 4"
