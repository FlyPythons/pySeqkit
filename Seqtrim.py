#!/usr/bin/env python

import argparse
from multiprocessing import Pool


from FastqReader import open_fastq
from FastaReader import open_fasta


def get_seq(filename, index, min_len):
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

    records = []

    if fmt.lower() in ["fastq", "fq", "fastq.gz", "fq.gz"]:
        records = open_fastq(filename)
    elif fmt.lower() in ["fasta", "fa", "fasta.gz", "fa.gz"]:
        records = open_fasta(filename)
    else:
        print("[%s] %r is not a valid seq format!" % (index, filename))

    out = open("%s.fasta" % index.split("/")[0], "w")

    for record in records:

        if record.length >= min_len:
            out.write(">%s\n%s\n" % (record.name, record.seq))
            r.append(record.length)

    out.close()

    return r


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


def seq_trim(filenames, fofn=False, concurrent=1, min_len=0):
    """
    trim FastA/Q files
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
        results.append(pool.apply_async(get_seq, (filename, index, min_len)))

    pool.close()
    pool.join()

    lengths = []

    for i, r in enumerate(results):
        print("[%s/%s] getting results of %r" % (i+1, len(results), file_list[i]))
        lengths += r.get()

    lengths = sorted(lengths, reverse=True)

    with open("seq.len", "w") as fh:
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
    args.add_argument("-f", "--fofn", action="store_true", help="input file contains file paths")
    args.add_argument("--min_len", type=int, metavar="INT", default=0, help="min length to statistics")
    args.add_argument("-c", "--concurrent", metavar='INT', type=int, default=1, help="number of concurrent process")

    return args.parse_args()


def main():
    args = get_args()
    seq_trim(args.input, args.fofn, args.concurrent, args.min_len)


if __name__ == "__main__":
    main()
