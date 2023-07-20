# __init__.py
"""Top-level package for VPC Tree.

Change Log.
- 0.2.2 Fix error were get_instances would get Instances from all VPCs.
- 0.2.1 Expand information in Auto Scaling Group sub-tree to include...
    - Launch Template
    - Launch Configurations
    - MixedInstancesPolicy
    - Min and Max Size
    - Load Balancers
    - Target Groups
- 0.2.0 Security Group Permissions added.
- 0.1.0 Initial release.
"""

__version__ = "0.2.2"
