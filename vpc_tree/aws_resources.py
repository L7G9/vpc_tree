# aws_resources.py
"""VPC Tree application's functionality to retrieve and filter resources from
Boto3."""

import boto3


def get_vpcs():
    """Get all Virtual Private Clouds in AWS account.

    Returns:
        A list of dictionaries containing the details of the Virtual Private
        Clouds.
    """
    client = boto3.client("ec2")
    vpc_response = client.describe_vpcs()
    return vpc_response["Vpcs"]


def get_vpc(vpc_id):
    """Get a single Virtual Private Cloud.

    Args:
        vpc_id: A string containing the Virtual Private Cloud Id to find.

    Returns:
        A dictionary containing the details of the Virtual Private
        Cloud.
    """
    client = boto3.client("ec2")
    response = client.describe_vpcs(
        VpcIds=[vpc_id],
    )
    return response["Vpcs"][0]


def get_security_groups(vpc_id):
    """Get all Security Groups linked to a Virtual Private Cloud.

    Args:
        vpc_id: A string containing the Virtual Private Cloud Id.

    Returns:
        A list of dictionaries containing the details of the Security Groups.
    """
    sgs = []

    client = boto3.client("ec2")
    paginator = client.get_paginator("describe_security_groups")
    parameters = {
        "Filters": [
            {"Name": "vpc-id", "Values": [vpc_id]},
        ]
    }
    page_iterator = paginator.paginate(**parameters)
    for page in page_iterator:
        sgs += page["SecurityGroups"]

    return sgs


def get_subnets(vpc_id):
    """Get all Subnets linked to a Virtual Private Cloud.

    Args:
        vpc_id: A string containing the Virtual Private Cloud Id.

    Returns:
        A list of dictionaries containing the details of the Subnets.
    """
    subnets = []

    client = boto3.client("ec2")
    paginator = client.get_paginator("describe_subnets")
    parameters = {
        "Filters": [
            {"Name": "vpc-id", "Values": [vpc_id]},
        ]
    }
    page_iterator = paginator.paginate(**parameters)
    for page in page_iterator:
        subnets += page["Subnets"]

    return subnets


def get_subnet_ids(subnets):
    """Get list of Subnet Ids.

    Args:
        subnets: A list of dictionaries containing the details of the
        Subnets.

    Returns:
        A list of strings containing the Subnet Ids."""
    subnet_ids = []
    for subnet in subnets:
        subnet_ids.append(subnet["SubnetId"])

    return subnet_ids


def get_instances(vpc_id):
    """Get all Instances in Virtual Private Cloud.

    Args:
        vpc_id: A string containing Virtual Private Cloud Id.

    Returns:
        A list of dictionaries containing the details of the Instances.
    """
    instances = []

    client = boto3.client("ec2")
    paginator = client.get_paginator("describe_instances")
    parameters = {
            "Filters": [
                {"Name": "vpc-id", "Values": [vpc_id]},
            ]
        }
    page_iterator = paginator.paginate(**parameters)
    for page in page_iterator:
        for reservations in page["Reservations"]:
            instances += reservations["Instances"]

    return instances


def filter_instances_by_subnet(instances, subnet_id):
    """Filter Instances by Subnet.

    Args:
        instances: A list of dictionaries containing the details of the
        Instances to filter.
        subnet_id: A string containing the Subnet Id to filter by.

    Returns:
        A list of dictionaries containing the details of the filtered
        Instances.
    """
    return list(filter(lambda d: d["SubnetId"] == subnet_id, instances))


def get_load_balancers():
    """Get all Load Balancers.

    Returns:
        A list of dictionaries containing the details of the Load Balancers.
    """
    lbs = []

    client = boto3.client("elbv2")
    paginator = client.get_paginator("describe_load_balancers")
    page_iterator = paginator.paginate()

    for page in page_iterator:
        lbs += page["LoadBalancers"]

    return lbs


def filter_load_balancers_by_vpc(load_balancers, vpc_id):
    """Filter Load Balancers by Virtual Private Cloud.

    Args:
        load_balancers: A list of dictionaries containing the details of the
        Load Balancers to filter.
        vpc_id: A string containing the Virtual Private Cloud Id to filter by.

    Returns:
        A list of dictionaries containing the details of the filtered Auto
        Scaling Groups."""
    return list(filter(lambda d: d["VpcId"] == vpc_id, load_balancers))


def get_load_balancer_arns(load_balancers):
    """Get list of Load Balancer ARNs.

    Args:
        load_balancers: A list of dictionaries containing the details of the
        Load Balancers.

    Returns:
        A list of strings containing the Load Balancer ARNs.
    """
    load_balancer_arns = []
    for load_balancer in load_balancers:
        load_balancer_arns.append(load_balancer["LoadBalancerArn"])

    return load_balancer_arns


def get_auto_scaling_groups():
    """Get all Auto Scaling Groups.

    Returns:
        A list of dictionaries containing the details of the Auto Scaling
        Groups.
    """
    asgs = []

    client = boto3.client("autoscaling")
    paginator = client.get_paginator("describe_auto_scaling_groups")
    page_iterator = paginator.paginate()

    for page in page_iterator:
        asgs += page["AutoScalingGroups"]

    return asgs


def filter_auto_scaling_groups_by_subnets(auto_scaling_groups, subnet_ids):
    """Filter Auto Scaling Groups by Subnet

    Args:
        auto_scaling_groups: A list of dictionaries containing the details of
        the Auto Scaling Groups to filter.
        subnet_ids: A list of strings containing the Subnet Ids to filter by.

    Returns:
        A list of dictionaries containing the details of the filtered Auto
        Scaling Groups.
    """
    filtered_asgs = []
    for asg in auto_scaling_groups:
        asg_subnet_ids = asg["VPCZoneIdentifier"].split(",")
        if any(id in subnet_ids for id in asg_subnet_ids):
            filtered_asgs.append(asg)

    return filtered_asgs


def get_target_groups(load_balancer_arns):
    """Get all Target Groups linked to a list of Load Balancers.

    Args:
        load_balancer_arns: A list of strings containing the Load Balancers
        ARNs.

    Returns:
        A list of dictionaries containing the details of the Target Groups.
    """
    target_groups = []

    client = boto3.client("elbv2")
    paginator = client.get_paginator("describe_target_groups")

    for arn in load_balancer_arns:
        page_iterator = paginator.paginate(LoadBalancerArn=arn)
        for page in page_iterator:
            target_groups += page["TargetGroups"]

    return target_groups
