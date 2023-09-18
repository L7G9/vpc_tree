# test_subnet_tree.py

import pytest
from vpc_tree.subnet_tree import SubnetTree


@pytest.fixture(scope="class")
def subnets():
    return [
        {
            "AvailabilityZone": "eu-west-2a",
            "CidrBlock": "10.0.1.0/24",
            "SubnetId": "sn-01",
            "Tags": [{"Key": "Name", "Value": "subnet-01"}],
        },
        {
            "AvailabilityZone": "eu-west-2b",
            "CidrBlock": "10.0.2.0/24",
            "SubnetId": "sn-02",
            "Tags": [{"Key": "Name", "Value": "subnet-02"}],
        },
        {
            "AvailabilityZone": "eu-west-2c",
            "CidrBlock": "10.0.3.0/24",
            "SubnetId": "sn-03",
            "Tags": [{"Key": "Name", "Value": "subnet-03"}],
        },
    ]


@pytest.fixture(scope="class")
def instances():
    return [
        {
            "ImageId": "ami-1234",
            "InstanceId": "i-01",
            "InstanceType": "t2.micro",
            "PrivateIpAddress": "10.0.1.5",
            "SecurityGroups": [{"GroupId": "sg-01"}],
            "State": {"Name": "running"},
            "SubnetId": "sn-01",
            "Tags": [{"Key": "Name", "Value": "instance-01"}],
        },
        {
            "ImageId": "ami-1234",
            "InstanceId": "i-02",
            "InstanceType": "t2.micro",
            "PrivateIpAddress": "10.0.1.6",
            "SecurityGroups": [{"GroupId": "sg-01"}],
            "State": {"Name": "running"},
            "SubnetId": "sn-01",
            "Tags": [{"Key": "Name", "Value": "instance-02"}],
        },
        {
            "ImageId": "ami-1234",
            "InstanceId": "i-03",
            "InstanceType": "t2.micro",
            "PrivateIpAddress": "10.0.2.7",
            "SecurityGroups": [{"GroupId": "sg-02"}],
            "State": {"Name": "running"},
            "SubnetId": "sn-02",
            "Tags": [{"Key": "Name", "Value": "instance-03"}],
        },
    ]


@pytest.mark.usefixtures("subnets", "instances")
class TestSubnetTree:
    def test_generate(self, subnets, instances):
        subnet_tree_generator = SubnetTree(subnets, instances)
        text_tree = []
        subnet_tree_generator.generate(text_tree, [])

        expected = [
            "Subnets:",
            "├──sn-01 : subnet-01 : eu-west-2a : 10.0.1.0/24",
            "│  └──Instances:",
            "│     ├──i-01 : instance-01 : ami-1234 : t2.micro : running"
            " : 10.0.1.5",
            "│     │  └──SecurityGroups:",
            "│     │     └──sg-01",
            "│     └──i-02 : instance-02 : ami-1234 : t2.micro : running"
            " : 10.0.1.6",
            "│        └──SecurityGroups:",
            "│           └──sg-01",
            "├──sn-02 : subnet-02 : eu-west-2b : 10.0.2.0/24",
            "│  └──Instances:",
            "│     └──i-03 : instance-03 : ami-1234 : t2.micro : running"
            " : 10.0.2.7",
            "│        └──SecurityGroups:",
            "│           └──sg-02",
            "└──sn-03 : subnet-03 : eu-west-2c : 10.0.3.0/24",
        ]

        assert len(text_tree) == len(expected)
        for i in range(len(expected)):
            assert text_tree[i] == expected[i]
