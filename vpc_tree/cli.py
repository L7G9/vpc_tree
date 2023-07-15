# cli.py
"""VPC Tree application's Command Line Interface."""

import argparse

from . import __version__, vpc_tree


def main():
    """"""
    args = parse_cmd_line_arguments()
    tree = vpc_tree.VPCTree()
    if args.list_vpcs:
        tree.display_vpc_list()
    else:
        tree.display_vpc_tree(args.vpc_id)


def parse_cmd_line_arguments():
    """"""
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
        help="Generate a list of VPCs",
    )
    parser.add_argument(
        "vpc_id",
        metavar="VPC_ID",
        nargs="?",
        help="Generate a tree of the Virtual Private Cloud's structure",
    )

    return parser.parse_args()
