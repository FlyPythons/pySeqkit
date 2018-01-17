#!/usr/bin/env python
import os


def test_fasta():
    fasta_record = """\
>test1 this is a test1
aaggcctt
aaggcctt
>test2 this is a test2
aaggcctt
>test3 this is a test3
aaggcctt
"""

    with open("test.fasta", "w") as out:
        out.write(fasta_record)

    os.system("python ../fastaStat.py test.fasta")
    os.system("python ../fastaSplit.py -m length -n 1 -o fasta test.fasta")


def test_fastq():

    fastq_record = """\
    @test1 this is a test1
    aaggccttss
    +
    >>>>>>>>>>
    @test2 this is a test2
    aaggccttss
    +
    >>>>>>>>>>
    @test3 this is a test3
    aaggccttss
    +
    >>>>>>>>>>
    """

    with open("test.fastq", "w") as out:
        out.write(fastq_record)

    os.system("python ../fastqStat.py test.fastq")
    os.system("python ../fastqSplit.py -m length -n 1 -o fastq test.fastq")


def main():
    test_fasta()
    test_fastq()

if __name__ == "__main__":
    main()

