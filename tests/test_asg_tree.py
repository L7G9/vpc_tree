# test_asg_tree.py

import pytest
from vpc_tree.asg_tree import ASGTree


@pytest.fixture(scope="class")
def auto_scaling_groups():
    return [
        {
            'AutoScalingGroupARN': 'arn:aws:asg-01...',
            'AutoScalingGroupName': 'auto-scaling-group-01',
            'Instances': [{'InstanceId': 'i-01'}],
            'LaunchConfigurationName': 'launch-configuration-01',
            'LoadBalancerNames': ['load-balancer-01'],
            'MaxSize': 3,
            'MinSize': 1,
            'TargetGroupARNs': ['arn:aws:tg-01...'],
            'VPCZoneIdentifier': 'subnet-01,subnet-02,subnet-03',
        }
    ]


@pytest.mark.usefixtures("auto_scaling_groups")
class TestASGTree:
    def test_generate(self, auto_scaling_groups):
        asg_tree_generator = ASGTree(auto_scaling_groups)
        text_tree = []
        asg_tree_generator.generate(text_tree, [])

        expected = [
            "Auto Scaling Groups:",
            "└──arn:aws:asg-01... : auto-scaling-group-01",
            "   ├──MinSize = 1 : MaxSize = 3",
            "   ├──Launch Configuration",
            "   │  └──launch-configuration-01",
            "   ├──Subnets:",
            "   │  ├──subnet-01",
            "   │  ├──subnet-02",
            "   │  └──subnet-03",
            "   ├──Instances:",
            "   │  └──i-01",
            "   ├──Load Balancers:",
            "   │  └──load-balancer-01",
            "   └──Target Groups:",
            "      └──arn:aws:tg-01...",
        ]

        assert len(text_tree) == len(expected)
        for i in range(len(expected)):
            assert text_tree[i] == expected[i]
