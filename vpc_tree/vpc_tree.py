# vpc_tree.py

"""This module provides VPC Tree main module."""

import boto3
import pprint

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


def _elbow_or_tree(last_node):
    return ELBOW if last_node else TEE


def _space_or_pipe(last_node):
    return SPACE_PREFIX if last_node else PIPE_PREFIX


def _prefix(last_nodes):
    prefix = ''

    for i in range(len(last_nodes)):
        leaf_node = i == len(last_nodes)-1
        if leaf_node:
            prefix += _elbow_or_tree(last_nodes[i])
        else:
            prefix += _space_or_pipe(last_nodes[i])

    return prefix


def _get_tag(tags, key):
    return next(filter(lambda d: d.get("Key") == key, tags), None)


def _get_tag_value(tags, key):
    tag = _get_tag(tags, key)
    if tag is not None:
        return tag['Value']
    return None


class VPCTree:
    def __init__(self, vpc_id):
        self._generator = _TreeGenerator(vpc_id)

    def generate(self):
        tree = self._generator.build_tree()
        for entry in tree:
            print(entry)


class _TreeGenerator:
    def __init__(self, vpc_id):
        self._tree = []
        self._vpc_id = vpc_id
        self._client = boto3.client('ec2')

    def build_tree(self):
        self._vpc()
        return self._tree

    def _vpcs(self):
        vpc_response = self._client.describe_vpcs()
        for vpc in vpc_response['Vpcs']:
            vpc_id = vpc['VpcId']
            name = _get_tag_value(vpc['Tags'], 'Name')
            print(f"VPC : {name} : {vpc_id}")

    def _get_vpc(self, vpc_id):
        response = self._client.describe_vpcs(
            VpcIds=[
                self._vpc_id,
            ],
        )

        # TODO: error check
        return response['Vpcs'][0]

    def _get_vpc_description(self, vpc):
        vpc_id = vpc['VpcId']
        name = _get_tag_value(vpc['Tags'], 'Name')
        cidr_block = vpc['CidrBlock']
        return f"{vpc_id} : {name} : {cidr_block}"

    def _get_vpc_security_groups(self, vpc_id):
        response = self._client.describe_security_groups(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc_id
                    ]
                },
            ]
        )
        return response['SecurityGroups']

    def _get_security_group_description(self, security_group, last_nodes):
        security_group_id = security_group['GroupId']
        name = security_group['GroupName']
        return f"{_prefix(last_nodes)} {security_group_id} : {name}"

    def _get_vpc_subnets(self, vpc_id):
        response = self._client.describe_subnets(
            Filters=[
                {
                    'Name': 'vpc-id',
                    'Values': [
                        vpc_id,
                    ]
                },
            ]
        )
        return response['Subnets']

    def _get_subnet_description(self, subnet, last_nodes):
        id = subnet['SubnetId']
        name = _get_tag_value(subnet['Tags'], 'Name')
        az = subnet['AvailabilityZone']
        cidr = subnet['CidrBlock']
        return f"{_prefix(last_nodes)} {id} : {name} : {az} : {cidr} "

    def _get_subnet_instances(self, subnet_id):
        response = self._client.describe_instances(
            Filters=[
                {
                    'Name': 'subnet-id',
                    'Values': [
                        subnet_id,
                    ]
                },
            ]
        )
        instances = []
        for reservation in response['Reservations']:
            instances += reservation['Instances']

        return instances

    def _get_instance_description(self, instance, last_nodes):
        id = instance['InstanceId']
        name = _get_tag_value(instance['Tags'], 'Name')
        image_id = instance['ImageId']
        instance_type = instance['InstanceType']
        state = instance['State']['Name']
        ip_address = instance['PrivateIpAddress']
        return f"{_prefix(last_nodes)} {id} : {name} : {image_id} : {instance_type} : {state} : {ip_address}"

    def _get_vpc_load_balancers(self, vpc_id):
        client = boto3.client('elbv2')
        response = client.describe_load_balancers()
        load_balancers = response['LoadBalancers']
        filtered_load_balancers = list(
            filter(lambda d: d['VpcId'] == vpc_id, load_balancers)
        )
        return filtered_load_balancers

    def _get_load_balancer_description(self, load_balancer, last_nodes):
        arn = load_balancer['LoadBalancerArn']
        name = load_balancer['LoadBalancerName']
        return f"{_prefix(last_nodes)} {arn} : {name}"

    def _vpc(self):
        vpc = self._get_vpc(self._vpc_id)
        self._tree.append(self._get_vpc_description(vpc))

        self._tree.append(f"{TEE} Security Groups:")

        security_groups = self._get_vpc_security_groups(self._vpc_id)
        security_group_count = len(security_groups)
        for i in range(security_group_count):
            last_subnet = i == security_group_count-1
            self._tree.append(
                self._get_security_group_description(
                    security_groups[i],
                    [False, last_subnet]
                )
            )

        self._tree.append(f"{TEE} Subnets:")
        subnets = self._get_vpc_subnets(self._vpc_id)
        subnets = sorted(subnets, key=lambda x: x['CidrBlock'])
        subnet_count = len(subnets)
        for i in range(subnet_count):
            last_subnet = i == subnet_count-1
            self._tree.append(
                self._get_subnet_description(
                    subnets[i],
                    [False, last_subnet]
                )
            )

            instances = self._get_subnet_instances(subnets[i]['SubnetId'])
            instances = sorted(instances, key=lambda x: x['PrivateIpAddress'])
            instance_count = len(instances)
            if instance_count != 0:
                self._tree.append(
                    f"{_prefix([False, last_subnet, True])} Instances:"
                )
                for j in range(instance_count):
                    last_instance = j == instance_count-1
                    self._tree.append(
                        self._get_instance_description(
                            instances[j],
                            [False, True, last_subnet, last_instance]
                        )
                    )
                    self._tree.append(
                        f"{_prefix([False, True, last_subnet, last_instance, True])} Security Groups:"
                    )
                    security_group_count = len(instances[j]['SecurityGroups'])
                    for k in range(security_group_count):
                        last_security_group = k == security_group_count-1
                        prefix = [
                            False,
                            True,
                            True,
                            last_subnet,
                            last_instance,
                            last_security_group
                        ]
                        id = instances[j]['SecurityGroups'][k]['GroupId']
                        self._tree.append(
                            f"{_prefix(prefix)} {id}"
                        )

        self._tree.append(f"{TEE} Load Balancers:")
        load_balancers = self._get_vpc_load_balancers(self._vpc_id)
        load_balancer_count = len(load_balancers)
        for i in range(load_balancer_count):
            last_load_balancer = i == load_balancer_count-1
            self._tree.append(
                self._get_load_balancer_description(
                    load_balancers[i],
                    [False, last_load_balancer]
                )
            )


if __name__ == "__main__":
    vpc_tree = VPCTree("vpc-0493abc0802f1f4f9")
    vpc_tree.generate()
