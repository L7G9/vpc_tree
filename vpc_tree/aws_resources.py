# aws_resources.py

import boto3


def get_vpcs():
    """Return a list of Virtual Private Clouds in AWS account."""
    client = boto3.client("ec2")
    vpc_response = client.describe_vpcs()
    return vpc_response["Vpcs"]


def get_vpc(vpc_id):
    """Get Virtual Private Cloud linked to vpc_id."""
    client = boto3.client("ec2")
    response = client.describe_vpcs(
        VpcIds=[vpc_id],
    )
    return response["Vpcs"][0]


def get_sgs(vpc_id):
    """Get all Security Groups linked to vpc_id."""
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
    """Get all Subnets linked to vpc_id."""
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
    """Get list of subnet ids."""
    subnet_ids = []
    for subnet in subnets:
        subnet_ids.append(subnet["SubnetId"])

    return subnet_ids


def get_instances(subnet_id):
    """Get all Instances linked to subnet_id."""
    instances = []

    client = boto3.client("ec2")
    paginator = client.get_paginator("describe_instances")
    parameters = {
        "Filters": [
            {"Name": "subnet-id", "Values": [subnet_id]},
        ]
    }
    page_iterator = paginator.paginate(**parameters)
    for page in page_iterator:
        for reservations in page["Reservations"]:
            instances += reservations["Instances"]

    return instances


def get_lbs():
    """Get all Load Balancers."""
    lbs = []

    client = boto3.client("elbv2")
    paginator = client.get_paginator("describe_load_balancers")
    page_iterator = paginator.paginate()

    for page in page_iterator:
        lbs += page["LoadBalancers"]

    return lbs


def filter_lbs_by_vpc(lbs, vpc_id):
    """Filter Load Balancers by vpc_id."""
    return list(filter(lambda d: d["VpcId"] == vpc_id, lbs))


def get_lb_arns(lbs):
    """Get list of Load Balancer arns."""
    load_balancer_arns = []
    for load_balancer in lbs:
        load_balancer_arns.append(load_balancer["LoadBalancerArn"])

    return load_balancer_arns


def get_asgs():
    """Get all Auto Scaling Groups."""
    asgs = []

    client = boto3.client("autoscaling")
    paginator = client.get_paginator("describe_auto_scaling_groups")
    page_iterator = paginator.paginate()

    for page in page_iterator:
        asgs += page["AutoScalingGroups"]

    return asgs


def filter_asgs_by_subnets(asgs, vpc_subnet_ids):
    """Filter Auto Scaling Groups by vpc_subnet_ids."""
    filtered_asgs = []
    for asg in asgs:
        asg_subnet_ids = asg["VPCZoneIdentifier"].split(",")
        if any(id in vpc_subnet_ids for id in asg_subnet_ids):
            filtered_asgs.append(asg)

    return filtered_asgs


def _get_target_groups(load_balancer_arns):
    """Get all Target Groups linked to load_balancer_arns."""
    target_groups = []

    client = boto3.client("elbv2")
    paginator = client.get_paginator("describe_target_groups")

    for arn in load_balancer_arns:
        page_iterator = paginator.paginate(LoadBalancerArn=arn)
        for page in page_iterator:
            target_groups += page["TargetGroups"]

    return target_groups
