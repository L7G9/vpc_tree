---
# VPC Tree

Command line app to display a VPC (Virtual Private Cloud) from AWS as a text tree on the console.

---

This project has been created with Boto3, the AWS SDK for Python.  It shows how different resources in a VPC are related by displaying thier IPv4 addresses, Availability Zones, Ids and ARNs.

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
- [python3](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html)

### 

Clone Github repositoy and move into project dirctory.
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
VPC : vpc-014d48c2988fe0a36
VPC : vpc-05b4c8dc7474706fa
```
Display a VPC.
```bash
./vpc_tree.py vpc-05b4c8dc7474706fa
```
Example output.
```
vpc-05b4c8dc7474706fa : 10.0.0.0/16
├──Security Groups:
│   ├──sg-079ac493a323d4bb9 : terraform-20230717100001338400000002
│   │   ├──Ingress Permissions:
│   │   │   ├──tcp : 80 : 80
│   │   │   │   ├──IP Ranges:
│   │   │   │   │   └──0.0.0.0/0
│   │   │   │   └──Security Groups:
│   │   │   └──tcp : 443 : 443
│   │   │       ├──IP Ranges:
│   │   │       │   └──0.0.0.0/0
│   │   │       └──Security Groups:
│   │   └──Egress Permissions:
│   │       └──All
│   │           ├──IP Ranges:
│   │           │   └──0.0.0.0/0
│   │           └──Security Groups:
│   ├──sg-011fb638259dccad6 : default
│   │   ├──Ingress Permissions:
│   │   │   └──All
│   │   │       ├──IP Ranges:
│   │   │       └──Security Groups:
│   │   │           └──sg-011fb638259dccad6
│   │   └──Egress Permissions:
│   │       └──All
│   │           ├──IP Ranges:
│   │           │   └──0.0.0.0/0
│   │           └──Security Groups:
│   └──sg-06573b18b3cc1a5c9 : terraform-20230717100001848000000004
│       ├──Ingress Permissions:
│       │   └──tcp : 80 : 80
│       │       ├──IP Ranges:
│       │       └──Security Groups:
│       │           └──sg-079ac493a323d4bb9
│       └──Egress Permissions:
│           └──All
│               ├──IP Ranges:
│               │   └──0.0.0.0/0
│               └──Security Groups:
├──Subnets:
│   ├──subnet-0dc16b4f7ff0813be : swa-03-public-1 : eu-west-2a : 10.0.1.0/24
│   ├──subnet-08b1c8a8689bdeab1 : swa-03-public-2 : eu-west-2b : 10.0.2.0/24
│   ├──subnet-0d58994416f73e388 : swa-03-public-3 : eu-west-2c : 10.0.3.0/24
│   ├──subnet-0b89af84321528afa : swa-03-private-1 : eu-west-2a : 10.0.4.0/24
│   │   └──Instances:
│   │       └──i-0b82a8ce5ac40dc13 : swa-03-main : ami-0c5539781ec0e23ab : t2.micro : running : 10.0.4.147
│   │           └──SecurityGroups:
│   │               └──sg-06573b18b3cc1a5c9
│   ├──subnet-06fe96013b9194760 : swa-03-private-2 : eu-west-2b : 10.0.5.0/24
│   └──subnet-0183f0deed194c5fb : swa-03-private-3 : eu-west-2c : 10.0.6.0/24
├──Load Balancers:
│   └──arn:aws:elasticloadbalancing:eu-west-2:382801774683:loadbalancer/app/swa-03-main/a7520e6004f53e41 : swa-03-main
│       ├──Availability Zones:
│       │   ├──eu-west-2b : subnet-08b1c8a8689bdeab1
│       │   ├──eu-west-2c : subnet-0d58994416f73e388
│       │   └──eu-west-2a : subnet-0dc16b4f7ff0813be
│       └──Security Groups:
│           └──sg-079ac493a323d4bb9
├──Auto Scaling Groups:
│   └──arn:aws:autoscaling:eu-west-2:382801774683:autoScalingGroup:70d2e826-e0e4-47d7-9d95-cabba63d872d:autoScalingGroupName/swa-03-main : swa-03-main
│       ├──MinSize = 1 : MaxSize = 3
│       ├──Launch Configuration
│       │   └──swa-03-asg-instance-20230717100003337900000006
│       ├──Subnets:
│       │   ├──subnet-06fe96013b9194760
│       │   ├──subnet-0183f0deed194c5fb
│       │   └──subnet-0b89af84321528afa
│       ├──Instances:
│       │   └──i-0b82a8ce5ac40dc13
│       ├──Load Balancers:
│       └──Target Groups:
│           └──arn:aws:elasticloadbalancing:eu-west-2:382801774683:targetgroup/tf-20230717100001345800000003/be4f992c74424036
└──Target Groups:
    └──arn:aws:elasticloadbalancing:eu-west-2:382801774683:targetgroup/tf-20230717100001345800000003/be4f992c74424036 : tf-20230717100001345800000003
        └──Load Balancers:
            └──arn:aws:elasticloadbalancing:eu-west-2:382801774683:loadbalancer/app/swa-03-main/a7520e6004f53e41
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

