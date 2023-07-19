# test_prefix.py

from vpc_tree.prefix import (
    ELBOW,
    PIPE,
    SPACE,
    TEE,
    elbow_or_tee,
    get_prefix,
    space_or_pipe,
)


class TestElbowOrTee:
    def test_last_node(self):
        assert elbow_or_tee(True) == ELBOW

    def test_more_nodes(self):
        assert elbow_or_tee(False) == TEE


class TestSpaceOrPipe:
    def test_last_subtree(self):
        assert space_or_pipe(True) == SPACE

    def test_more_subtrees(self):
        assert space_or_pipe(False) == PIPE


class TestGetPrefix:
    def test_empty(self):
        assert get_prefix([]) == ""

    def test_last_node(self):
        assert get_prefix([True]) == ELBOW

    def test_more_nodes(self):
        assert get_prefix([False]) == TEE

    def test_last_subtree_last_node(self):
        assert get_prefix([True, True]) == SPACE + ELBOW

    def test_last_subtree_more_nodes(self):
        assert get_prefix([True, False]) == SPACE + TEE

    def test_more_subtrees_last_node(self):
        assert get_prefix([False, True]) == PIPE + ELBOW

    def test_more_subtrees_more_nodes(self):
        assert get_prefix([False, False]) == PIPE + TEE
