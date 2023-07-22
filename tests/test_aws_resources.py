# test_aws_resources.py


import pytest
from vpc_tree.aws_resources import (
    get_load_balancer_arns,
    get_subnet_ids,
    filter_auto_scaling_groups_by_subnets,
    filter_instances_by_subnet,
    filter_load_balancers_by_vpc,
)


@pytest.fixture(scope="function")
def subnets():
    return [
        {"SubnetId": "Subnet-01"},
        {"SubnetId": "Subnet-02"},
        {"SubnetId": "Subnet-03"},
    ]


@pytest.fixture(scope="function")
def instances():
    return [
        {"InstanceId": "I-01", "SubnetId": "Subnet-01"},
        {"InstanceId": "I-02", "SubnetId": "Subnet-02"},
        {"InstanceId": "I-03", "SubnetId": "Subnet-03"},
        {"InstanceId": "I-04", "SubnetId": "Subnet-01"},
        {"InstanceId": "I-05", "SubnetId": "Subnet-02"},
        {"InstanceId": "I-06", "SubnetId": "Subnet-03"},
    ]


@pytest.fixture(scope="function")
def load_balancers():
    return [
        {"LoadBalancerArn": "arn:aws:LB-01...", "VpcId": "VPC-01"},
        {"LoadBalancerArn": "arn:aws:LB-02...", "VpcId": "VPC-02"},
        {"LoadBalancerArn": "arn:aws:LB-03...", "VpcId": "VPC-01"},
        {"LoadBalancerArn": "arn:aws:LB-04...", "VpcId": "VPC-01"},
        {"LoadBalancerArn": "arn:aws:LB-05...", "VpcId": "VPC-02"},
    ]


@pytest.fixture(scope="function")
def auto_scaling_groups():
    return [
        {
            "AutoScalingGroupARN": "arn:aws:ASG-01...",
            "VPCZoneIdentifier": "Subnet-01, Subnet-99",
        },
        {
            "AutoScalingGroupARN": "arn:aws:ASG-02...",
            "VPCZoneIdentifier": "Subnet-02, Subnet-99",
        },
        {
            "AutoScalingGroupARN": "arn:aws:ASG-03...",
            "VPCZoneIdentifier": "Subnet-99",
        },
    ]


class TestGetSubnetIds:
    def test_function(self, subnets):
        results = get_subnet_ids(subnets)
        expected = ["Subnet-01", "Subnet-02", "Subnet-03"]
        assert results == expected


class TestFilterInstancesBySubnet:
    def test_function(self, instances):
        results = filter_instances_by_subnet(instances, "Subnet-01")
        expected = [
            {"InstanceId": "I-01", "SubnetId": "Subnet-01"},
            {"InstanceId": "I-04", "SubnetId": "Subnet-01"},
        ]
        assert results == expected


class TestFilterLoadBalancersByVPC:
    def test_function(self, load_balancers):
        results = filter_load_balancers_by_vpc(load_balancers, "VPC-01")
        expected = [
            {"LoadBalancerArn": "arn:aws:LB-01...", "VpcId": "VPC-01"},
            {"LoadBalancerArn": "arn:aws:LB-03...", "VpcId": "VPC-01"},
            {"LoadBalancerArn": "arn:aws:LB-04...", "VpcId": "VPC-01"},
        ]
        assert results == expected


class TestGetLoadBalancerARNs:
    def test_function(self, load_balancers):
        results = get_load_balancer_arns(load_balancers)
        expected = [
            "arn:aws:LB-01...",
            "arn:aws:LB-02...",
            "arn:aws:LB-03...",
            "arn:aws:LB-04...",
            "arn:aws:LB-05...",
        ]
        assert results == expected


class TestFilterAutoScalingGroupsBySubnets:
    def test_function(self, auto_scaling_groups, subnets):
        results = filter_auto_scaling_groups_by_subnets(
            auto_scaling_groups, get_subnet_ids(subnets)
        )
        expected = [
            {
                "AutoScalingGroupARN": "arn:aws:ASG-01...",
                "VPCZoneIdentifier": "Subnet-01, Subnet-99",
            },
            {
                "AutoScalingGroupARN": "arn:aws:ASG-02...",
                "VPCZoneIdentifier": "Subnet-02, Subnet-99",
            },
        ]
        assert results == expected
