# test_lb_tree.py

import pytest
from vpc_tree.lb_tree import LBTree


@pytest.fixture(scope="class")
def load_balancers():
    return [
        {
            "AvailabilityZones": [
                {
                    "SubnetId": "subnet-01",
                    "ZoneName": "eu-west-2a",
                },
                {
                    "SubnetId": "subnet-02",
                    "ZoneName": "eu-west-2b",
                },
                {
                    "SubnetId": "subnet-03",
                    "ZoneName": "eu-west-2c",
                },
            ],
            "LoadBalancerArn": "arn:aws:lb-01...",
            'LoadBalancerName': 'load-balancer-01',
            "SecurityGroups": ["sg-01"],
        }
    ]


@pytest.mark.usefixtures("load_balancers")
class TestLBTree:
    def test_generate(self, load_balancers):
        lb_tree_generator = LBTree(load_balancers)
        text_tree = []
        lb_tree_generator.generate(text_tree, [])

        expected = [
            "Load Balancers:",
            "└──arn:aws:lb-01... : load-balancer-01",
            "   ├──Availability Zones:",
            "   │  ├──eu-west-2a : subnet-01",
            "   │  ├──eu-west-2b : subnet-02",
            "   │  └──eu-west-2c : subnet-03",
            "   └──Security Groups:",
            "      └──sg-01",
        ]

        assert len(text_tree) == len(expected)
        for i in range(len(expected)):
            assert text_tree[i] == expected[i]
