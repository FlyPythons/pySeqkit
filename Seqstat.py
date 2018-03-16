#!/usr/bin/env python
"""
This script is used to statistics on a list of fastq files
copyright@fanjunpeng (jpfan@whu.edu.cn)

2018/1/15: init by fanjunpeng

"""
import argparse
from multiprocessing import Pool

from FastqReader import open_fastq
from FastaReader import open_fasta


def get_length(filename, index, min_len):
    """
    get the length of record
    :param filename:
    :return:
    """
    r = []

    print("[%s] process %r" % (index, filename))

    fmt = filename.split(".")[-1]

    if filename.endswith(".gz"):
        fmt = ".".join(filename.split(".")[-2:])

    if fmt.lower() in ["fastq", "fq", "fastq.gz", "fq.gz"]:
        for record in open_fastq(filename):

            if record.length >= min_len:
                r.append(record.length)

    elif fmt.lower() in ["fasta", "fa", "fasta.gz", "fa.gz"]:
        for record in open_fasta(filename):

            if record.length >= min_len:
                r.append(record.length)
    else:
        print("[%s] %r is not a valid seq format!" % (index, filename))

    return r


def N(number, lengths):
    """
    return N{number} information of lengths
    :param number: 0-100
    :param lengths: a list of length
    :return:
    """
    assert lengths

    sum_length = sum(lengths)
    accu_len = 0
    accu_num = 0

    for i in sorted(lengths, reverse=True):
        accu_len += i
        accu_num += 1

        if accu_len >= sum_length*number/100:
            return i, accu_num, accu_len

    return i, accu_num, accu_len


def over(number, lengths):
    """
    return length in lengths over {number}
    :param number:
    :param lengths:
    :return:
    """
    assert lengths
    accu_len = 0
    accu_num = 0

    for i in sorted(lengths, reverse=True):
        if i < number:
            return i, accu_num, accu_len

        accu_len += i
        accu_num += 1

    return i, accu_num, accu_len


def fofn2list(fofn):
    r = []
    with open(fofn) as fh:
        for line in fh.readlines():
            line = line.strip()
            if line == '':
                continue
            if line.startswith("#"):
                continue

            r.append(line)

    return r


def seq_stat(filenames, ngs=False, fofn=False, concurrent=1, min_len=0):
    """
    statistics on fastq files
    :param filenames:
    :param fofn: a file contain fastq file list
    :param concurrent: concurrent process to read fastq files
    :param min_len:
    :return:
    """
    # 1. get the lengths of each fastA/Q file
    if fofn:
        file_list = []
        for f in filenames:
            file_list += fofn2list(f)
    else:
        file_list = filenames

    pool = Pool(processes=concurrent)
    results = []

    for i in range(len(file_list)):
        filename = file_list[i]
        index = "%s/%s" % (i+1, len(file_list))
        results.append(pool.apply_async(get_length, (filename, index, min_len)))

    pool.close()
    pool.join()

    lengths = []

    for i, r in enumerate(results):
        print("[%s/%s] getting results of %r" % (i+1, len(results), file_list[i]))
        lengths += r.get()

    # write lengths out
    lengths = sorted(lengths, reverse=True)

    # 2. get the common statistics
    total_length = sum(lengths)
    reads_number = len(lengths)
    file_num = "{0:,}".format(len(file_list))
    average_length = "{0:,}".format(int(total_length / reads_number))
    longest = "{0:,}".format(lengths[0])
    _total_length = "{0:,}".format(total_length)
    reads_number = "{0:,}".format(reads_number)

    print("""
Statistics for all FastA/Q records

file number:   \t{file_num}
record number: \t{reads_number}
sum of length: \t{_total_length}
average length:\t{average_length}
longest length:\t{longest}
""".format(**locals()))

    # 2. get the N10-N90 statstics
    # length: the N{i} value; number: number of reads which length >= N{i}
    # if the input file is ngs short reads, skip the following steps.
    if ngs:
        return 1

    print("Distribution of record length")
    print("%5s\t%15s\t%15s\t%10s" % ("Type", "Bases", "Count", "%Bases"))
    for i in [10, 20, 30, 40, 50, 60, 70, 80, 90]:
        read_length, read_number, read_length_sum = N(i, lengths)
        print("%5s\t%15s\t%15s\t%10.2f" % ("N%s" % i,
                                           "{0:,}".format(read_length),
                                           "{0:,}".format(read_number),
                                           100.0*read_length_sum/total_length))

    # length: the sum of record length which length >= i; number: the number of record which length >= i
    for i in [1, 5, 10, 20, 30, 40, 50, 60]:
        _, read_number, read_length_sum = over(i*1000, lengths)
        print("%5s\t%15s\t%15s\t%10.2f" % (">%skb" % i,
                                           "{0:,}".format(read_length_sum),
                                           "{0:,}".format(read_number),
                                           100.0*read_length_sum/total_length))

    # write out record length for plot
    with open("record.len", "w") as fh:
        fh.write("\n".join(map(str, lengths)))


def get_args():
    """
    get args
    :return:
    """
    args = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description="""
description:
    Statistics on FastA/Q files

author:  fanjunpeng (jpfan@whu.edu.cn)
        """)

    args.add_argument("input", metavar='FILEs', nargs="+", help="file paths, '*' is accepted")
    args.add_argument("-ngs", action="store_true", help="input fastq reads is short reads from ngs")
    args.add_argument("-f", "--fofn", action="store_true", help="input file contains file paths")
    args.add_argument("--min_len", type=int, metavar="INT", default=0, help="min length to statistics")
    args.add_argument("-c", "--concurrent", metavar='INT', type=int, default=1, help="number of concurrent process")

    return args.parse_args()


def main():
    args = get_args()
    seq_stat(args.input, args.ngs, args.fofn, args.concurrent, args.min_len)


if __name__ == "__main__":
    main()
