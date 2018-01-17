#!/usr/bin/env python
"""
Split fasta files by accumulated sequence length or number
Copyright@fanjunpeng (jpfan@whu.edu.cn)

2018/1/12: init by fanjunpeng
2018/1/13: add support for more fasta files
2018/1/13: add support for more multiprocess
"""

from __future__ import absolute_import

import logging
import os
import argparse
from multiprocessing import Pool


from common import fofn2list, mkdir, touch
from FastaReader import open_fasta


LOG = logging.getLogger(__name__)


def write_record(records, out_filename):
    """
    write fasta records to file
    """

    # write seq records
    fasta_out = open(out_filename, "w")
    bed_out = open("%s.bed" % out_filename, 'w')

    for record in records:
        fasta_out.write("%s\n" % str(record))
        bed_out.write("%s\t1\t%s\n" % (record.id, record.length))

    fasta_out.close()
    bed_out.close()

    return out_filename


def split_by_number(filename, number, output_dir="split", max_split=1000):
    """
    split Fasta file by {number} records per file
    :param filename: Fasta filename
    :param number: records per file
    :param output_dir: the output directory of sub fasta files
    :param max_split: the max number of sub files, avoid too much sub files
    :return: list of sub file names
    """

    r = []

    head = os.path.splitext(os.path.basename(filename.rstrip(".gz")))[0]
    prefix = os.path.join(output_dir, head)

    sub_num = 0
    fasta_records = []
    n = 0

    for record in open_fasta(filename):

        if n == number:

            if sub_num > max_split:
                msg = "file %r cuts more than %s, break" % (filename, max_split)
                raise Exception(msg)

            out_filename = "%s.%s.fasta" % (prefix, sub_num)
            write_record(fasta_records, out_filename)
            r.append(out_filename)
            sub_num += 1

            fasta_records = []
            n = 0

        fasta_records.append(record)
        n += 1

    # add the last part if has
    if fasta_records:
        out_filename = "%s.%s.fasta" % (prefix, sub_num)
        write_record(fasta_records, out_filename)
        r.append(out_filename)

    return r


def split_by_length(filename, number, output_dir="split", max_split=1000):
    """
    split Fasta file by {number} length per file
    :param filename: Fasta filename
    :param number: record length per file
    :param output_dir: the output directory of sub fasta files
    :param max_split: the max number of sub files, avoid too much sub files
    :return: list of sub file names
    """
    r = []

    head = os.path.splitext(os.path.basename(filename.rstrip(".gz")))[0]
    prefix = os.path.join(output_dir, head)

    sub_num = 0
    fasta_records = []
    n = 0

    for record in open_fasta(filename):

        if n > number:

            if sub_num > max_split:
                msg = "file %r cuts more than %s, break" % (filename, max_split)
                raise Exception(msg)

            out_filename = "%s.%s.fasta" % (prefix, sub_num)
            write_record(fasta_records, out_filename)
            r.append(out_filename)
            sub_num += 1

            fasta_records = []
            n = 0

        fasta_records.append(record)
        n += record.length

    # add the last part if has
    if fasta_records:
        out_filename = "%s.%s.fasta" % (prefix, sub_num)
        write_record(fasta_records, out_filename)
        r.append(out_filename)

    return r


def fastaSplit(filenames, mode, num, output_dir, concurrent=1, max_split=1000):
    """
    split fasta files
    :param filenames: a list of fasta files
    :param mode: length or number
    :param num: 
    :param output_dir: output directory
    :param concurrent: see -h
    :param max_split: see -h
    :return: 
    """
    assert mode in ["number", "length"]

    output_dir = mkdir(output_dir)
    split_list = os.path.join(output_dir, "split_list")
    done = os.path.join(output_dir, "split_done")

    # avoid rerun
    if os.path.exists(done):
        print("%r exists, pass this step; if you want to rerun, delete the file" % done)
        return fofn2list(split_list)

    # for multiprocessing
    pool = Pool(processes=concurrent)
    results = []
    print("Split '{filenames}' by sequence {mode} =~ {num} per file".format(**locals()))
    if mode == "number":
        for f in filenames:
            results.append(pool.apply_async(split_by_number, (f, num, output_dir, max_split)))
    if mode == "length":
        for f in filenames:
            results.append(pool.apply_async(split_by_length, (f, num, output_dir, max_split)))

    pool.close()
    pool.join()

    file_list = []
    for r in results:
        file_list += r.get()

    with open(split_list, "w") as fh:
        fh.write("\n".join(file_list))

    touch(done)
    return file_list


def set_args():
    args = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description="""
description:
    Split fasta files into sub files by accumulated sequence length or number

author:  fanjunpeng (jpfan@whu.edu.cn)
    """)

    args.add_argument("input", metavar="FASTAs", nargs="+", help="fasta files")
    args.add_argument("-m", "--mode", choices=["number", "length"], default="length", help="split by number or length")
    args.add_argument("-n", "--number", type=int, metavar="INT", help="the value of mode")
    args.add_argument("-o", "--output_dir", default="split", metavar="DIR", help="output directory")
    args.add_argument("-ms", "--max_split", type=int, default=1000, metavar="INT", help="the max number of sub files")
    args.add_argument("-c", "--concurrent", type=int, default=1, metavar="INT", help="number of concurrent process")
    return args.parse_args()


def main():
    args = set_args()
    filenames = args.input
    mode = args.mode
    number = args.number
    output_dir = args.output_dir
    concurrent = args.concurrent
    max_split = args.max_split

    fastaSplit(filenames, mode, number, output_dir, concurrent, max_split)


if __name__ == "__main__":
    main()
