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
        assert len(text_tree) == 19
        assert text_tree[0] == "Security Groups:"
        assert text_tree[1] == "├──sg-01 : security-group-1"
        assert text_tree[2] == "│  ├──Ingress Permissions:"
        assert text_tree[3] == "│  │  └──tcp : 80 : 80"
        assert text_tree[4] == "│  │     └──Security Groups:"
        assert text_tree[5] == "│  │        └──sg-02"
        assert text_tree[6] == "│  └──Egress Permissions:"
        assert text_tree[7] == "│     └──All"
        assert text_tree[8] == "│        └──IP Ranges:"
        assert text_tree[9] == "│           └──0.0.0.0/0"
        assert text_tree[10] == "└──sg-02 : security-group-2"
        assert text_tree[11] == "   ├──Ingress Permissions:"
        assert text_tree[12] == "   │  └──tcp : 80 : 80"
        assert text_tree[13] == "   │     └──IP Ranges:"
        assert text_tree[14] == "   │        └──0.0.0.0/0"
        assert text_tree[15] == "   └──Egress Permissions:"
        assert text_tree[16] == "      └──All"
        assert text_tree[17] == "         └──IP Ranges:"
        assert text_tree[18] == "            └──0.0.0.0/0"
