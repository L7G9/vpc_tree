---
# VPC Tree

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Github Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white) ![AWS](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
[![CI pipeline](https://github.com/L7G9/vpc_tree/actions/workflows/main.yaml/badge.svg)](https://github.com/L7G9/vpc_tree/actions/workflows/main.yaml) [![](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

Command line app to display a VPC (Virtual Private Cloud) from AWS as a text tree on the console.

---

This project has been created with Boto3, the AWS SDK for Python.  It shows how different resources in a VPC are related by displaying their IPv4 addresses, Availability Zones, Ids and ARNs.

The current version VPC Tree displays following resources in this order...
- VPC
  - Security Groups
    - Ingress Permissions
    - Egress Permissions
  - Subnets
    - EC2 Instances
      - Security Group Ids
  - Load Balancers
    - Availability Zones / Subnets
    - Security Group Ids
  - Auto Scaling Groups
    - Launch Configuration / Launch Template / Mixed Instances Policy
    - Subnet Ids
    - Instance Ids
    - Load Balancer Names?
    - Target Group ARNs
  - Target Groups
    - Load Balancer ARNs

---

## Getting Started

### Requirements
- [Python3](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)

Clone Github repository and move into project directory.
```bash
git clone https://github.com/L7G9/vpc_tree.git
cd vpc_tree
```
Create a virtual environment (optional).
```bash
python3 -m venv venv
source venv/bin/activate
```
Install packages.
```bash
pip install -r requirements.txt
```
List VPCs.
```bash
./vpc_tree.py -l
```
Example output.
```
Default VPC : vpc-014d48c2988fe0a36
swa-03-main : vpc-05b4c8dc7474706fa
```
Display a VPC.
```bash
./vpc_tree.py vpc-05b4c8dc7474706fa
```
Example output.
```
vpc-05b4c8dc7474706fa : 10.0.0.0/16
├──Security Groups:
│  ├──sg-01bbd93a8c417af90 : terraform-20230720144206890700000003
│  │  ├──Ingress Permissions:
│  │  │  └──tcp : 80 : 80
│  │  │     └──Security Groups:
│  │  │        └──sg-0796944ff18bd994c
│  │  └──Egress Permissions:
│  │     └──All
│  │        └──IP Ranges:
│  │           └──0.0.0.0/0
│  ├──sg-0796944ff18bd994c : terraform-20230720144206876600000002
│  │  ├──Ingress Permissions:
│  │  │  ├──tcp : 80 : 80
│  │  │  │  └──IP Ranges:
│  │  │  │     └──0.0.0.0/0
│  │  │  └──tcp : 443 : 443
│  │  │     └──IP Ranges:
│  │  │        └──0.0.0.0/0
│  │  └──Egress Permissions:
│  │     └──All
│  │        └──IP Ranges:
│  │           └──0.0.0.0/0
│  └──sg-0a4c885185c206dab : default
│     ├──Ingress Permissions:
│     │  └──All
│     │     └──Security Groups:
│     │        └──sg-0a4c885185c206dab
│     └──Egress Permissions:
│        └──All
│           └──IP Ranges:
│              └──0.0.0.0/0
├──Subnets:
│  ├──subnet-069b049e409b57faf : swa-03-public-1 : eu-west-2a : 10.0.1.0/24
│  ├──subnet-0d71df24781ad2725 : swa-03-public-2 : eu-west-2b : 10.0.2.0/24
│  ├──subnet-083796c2b11c588b3 : swa-03-public-3 : eu-west-2c : 10.0.3.0/24
│  ├──subnet-00996db233970059c : swa-03-private-1 : eu-west-2a : 10.0.4.0/24
│  ├──subnet-0d920f96945daaa51 : swa-03-private-2 : eu-west-2b : 10.0.5.0/24
│  │  └──Instances:
│  │     └──i-015f0c983887e4536 : swa-03-main : ami-0c5539781ec0e23ab : t2.micro : running : 10.0.5.201
│  │        └──SecurityGroups:
│  │           └──sg-01bbd93a8c417af90
│  └──subnet-01c15dee0f01f50e1 : swa-03-private-3 : eu-west-2c : 10.0.6.0/24
├──Load Balancers:
│  └──arn:aws:elasticloadbalancing:eu-west-2:382801774683:loadbalancer/app/swa-03-main/d842f7734bfbc58c : swa-03-main
│     ├──Availability Zones:
│     │  ├──eu-west-2a : subnet-069b049e409b57faf
│     │  ├──eu-west-2c : subnet-083796c2b11c588b3
│     │  └──eu-west-2b : subnet-0d71df24781ad2725
│     └──Security Groups:
│        └──sg-0796944ff18bd994c
├──Auto Scaling Groups:
│  └──arn:aws:autoscaling:eu-west-2:382801774683:autoScalingGroup:9e01e56e-be0f-4f59-a9ca-9015935e1184:autoScalingGroupName/swa-03-main : swa-03-main
│     ├──MinSize = 1 : MaxSize = 3
│     ├──Launch Configuration
│     │  └──swa-03-asg-instance-20230720144208229200000006
│     ├──Subnets:
│     │  ├──subnet-01c15dee0f01f50e1
│     │  ├──subnet-00996db233970059c
│     │  └──subnet-0d920f96945daaa51
│     ├──Instances:
│     │  └──i-015f0c983887e4536
│     ├──Load Balancers:
│     └──Target Groups:
│        └──arn:aws:elasticloadbalancing:eu-west-2:382801774683:targetgroup/tf-20230720144207317600000004/6678606d2f35b195
└──Target Groups:
   └──arn:aws:elasticloadbalancing:eu-west-2:382801774683:targetgroup/tf-20230720144207317600000004/6678606d2f35b195 : tf-20230720144207317600000004
      └──Load Balancers:
         └──arn:aws:elasticloadbalancing:eu-west-2:382801774683:loadbalancer/app/swa-03-main/d842f7734bfbc58c
```

## Author
[@L7G9](https://www.github.com/L7G9)

---

## Acknowledgements
All these resources were used to create this project.  Thank you to all those who took the time and effort to share.
- [Directory Tree Tutorial](https://realpython.com/directory-tree-generator-python/)
- [VPC](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_vpcs.html)
- [Security Groups](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_security_groups.html)
- [Subnets](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_subnets.html)
- [Instances](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2/client/describe_instances.html)
- [Load Balancers](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_load_balancers.html)
- [Auto Scaling Groups](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling/client/describe_auto_scaling_groups.html)
- [Target Groups](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/elbv2/client/describe_target_groups.html)
- [Flake8](https://flake8.pycqa.org/en/latest/)
- [Black](https://pypi.org/project/black/)
- [Docformatter](https://github.com/PyCQA/docformatter)
---
