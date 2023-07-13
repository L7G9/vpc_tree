"""This module provides the VPC Tree CLI."""
# cli.py

import argparse
from . import __version__
#from .vpc_tree import


def main():
    args = parse_cmd_line_arguments()
    print(args)
    print(f"list-vpcs {args.list_vpcs}")
    print(f"vpc {args.vpc_id}")

def parse_cmd_line_arguments():
    parser = argparse.ArgumentParser(
        prog="vpc_tree",
        description="VPC Tree, an AWS resource tree generator",
        epilog="Thanks for using VPV Tree.",
    )
    parser.version = f"VPC Tree V{__version__}"
    parser.add_argument("-v", "--version", action="version")
    parser.add_argument(
        "-l",
        "--list-vpcs",
        action="store_true",
        help="Generate a list of VPCs"
    )
    parser.add_argument(
        "vpc_id",
        metavar="VPC_ID",
        nargs="?",
        help="Generate a tree describing the structure of the virtual Private Cloud with VPD_ID"
    )

    return parser.parse_args()
