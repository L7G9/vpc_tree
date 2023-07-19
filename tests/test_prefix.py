# test_prefix.py

from vpc_tree.prefix import (ELBOW, PIPE, SPACE, TEE, elbow_or_tree,
                             get_prefix, space_or_pipe)


class TestPrefixFunctions:
    def test_elbow_or_tree_last_node(self):
        assert elbow_or_tree(True) == ELBOW

    def test_elbow_or_tree_more_nodes(self):
        assert elbow_or_tree(False) == TEE

    def test_space_or_pipe_last_subtree(self):
        assert space_or_pipe(True) == SPACE

    def test_space_or_pipe_more_subtrees(self):
        assert space_or_pipe(False) == PIPE

    def test_get_prefix_empty(self):
        assert get_prefix([]) == ""

    def test_get_prefix_last_node(self):
        assert get_prefix([True]) == ELBOW

    def test_get_prefix_more_nodes(self):
        assert get_prefix([False]) == TEE

    def test_get_prefix_last_subtree_last_node(self):
        assert get_prefix([True, True]) == SPACE + ELBOW

    def test_get_prefix_last_subtree_more_nodes(self):
        assert get_prefix([True, False]) == SPACE + TEE

    def test_get_prefix_more_subtrees_last_node(self):
        assert get_prefix([False, True]) == PIPE + ELBOW

    def test_get_prefix_more_subtrees_more_nodes(self):
        assert get_prefix([False, False]) == PIPE + TEE
