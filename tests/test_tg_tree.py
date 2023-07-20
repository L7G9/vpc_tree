# test_tg_tree.py

import pytest
from vpc_tree.tg_tree import TGTree


@pytest.fixture(scope="class")
def target_groups():
    return [
        {
            'LoadBalancerArns': ['arn:aws:lb-01...'],
            'TargetGroupArn': 'arn:aws:tg-01...',
            'TargetGroupName': 'target-group-01',
        }
    ]


@pytest.mark.usefixtures("target_groups")
class TestTGTree:
    def test_generate(self, target_groups):
        tg_tree_generator = TGTree(target_groups)
        text_tree = []
        tg_tree_generator.generate(text_tree, [])

        expected = [
            "Target Groups:",
            "└──arn:aws:tg-01... : target-group-01",
            "   └──Load Balancers:",
            "      └──arn:aws:lb-01...",
        ]

        assert len(text_tree) == len(expected)
        for i in range(len(expected)):
            assert text_tree[i] == expected[i]
