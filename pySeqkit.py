#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import logging

from seqkit.stat import stat, stat_args
from seqkit.split import split, split_args
from seqkit import __author__, __version__, __email__


LOG = logging.getLogger(__name__)
__all__ = []


def set_args():

    args = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description="""
Toolkit for processing sequences in FASTA/Q formats

version: %s
contact:  %s <%s>\
    """ % (__version__, " ".join(__author__), __email__))

    subparsers = args.add_subparsers(
        title='commands',
        dest='command')
    subparsers.required = True

    parser_stat = subparsers.add_parser('stat', help="Statistics on sequences")
    parser_stat = stat_args(parser_stat)
    parser_stat.set_defaults(func=stat)

    parser_split = subparsers.add_parser('split', help="Split sequences")
    parser_split = split_args(parser_split)
    parser_split.set_defaults(func=split)

    return args.parse_args()


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )

    args = set_args()
    args.func(args)


if __name__ == "__main__":
    main()

