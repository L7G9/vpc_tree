# test_sg_tree.py

import pytest
from vpc_tree.sg_tree import SGTree


@pytest.fixture(scope="class")
def security_groups():
    return [
        {
            "GroupId": "sg-01",
            "GroupName": "security-group-1",
            "IpPermissions": [
                {
                    "FromPort": 80,
                    "IpProtocol": "tcp",
                    "IpRanges": [],
                    "ToPort": 80,
                    "UserIdGroupPairs": [{"GroupId": "sg-02", }],
                }
            ],
            "IpPermissionsEgress": [
                {
                    "IpProtocol": "-1",
                    "IpRanges": [{"CidrIp": "0.0.0.0/0", }],
                    "UserIdGroupPairs": [],
                }
            ],
        },
        {
            "GroupId": "sg-02",
            "GroupName": "security-group-2",
            "IpPermissions": [
                {
                    "FromPort": 80,
                    "IpProtocol": "tcp",
                    "IpRanges": [{"CidrIp": "0.0.0.0/0", }],
                    "ToPort": 80,
                    "UserIdGroupPairs": [],
                },
            ],
            "IpPermissionsEgress": [
                {
                    "IpProtocol": "-1",
                    "IpRanges": [{"CidrIp": "0.0.0.0/0", }],
                    "UserIdGroupPairs": [],
                }
            ],
        },
    ]


@pytest.mark.usefixtures("security_groups")
class TestSGTree:
    def test_generate(self, security_groups):
        sg_tree_generator = SGTree(security_groups)
        text_tree = []
        sg_tree_generator.generate(text_tree, [])

        expected = [
            "Security Groups:",
            "├──sg-01 : security-group-1",
            "│  ├──Ingress Permissions:",
            "│  │  └──tcp : 80 : 80",
            "│  │     └──Security Groups:",
            "│  │        └──sg-02",
            "│  └──Egress Permissions:",
            "│     └──All",
            "│        └──IP Ranges:",
            "│           └──0.0.0.0/0",
            "└──sg-02 : security-group-2",
            "   ├──Ingress Permissions:",
            "   │  └──tcp : 80 : 80",
            "   │     └──IP Ranges:",
            "   │        └──0.0.0.0/0",
            "   └──Egress Permissions:",
            "      └──All",
            "         └──IP Ranges:",
            "            └──0.0.0.0/0",
        ]

        assert len(text_tree) == len(expected)
        for i in range(len(expected)):
            assert text_tree[i] == expected[i]
