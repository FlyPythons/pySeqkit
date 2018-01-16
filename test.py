#!/usr/bin/env python
from FastaReader import open_fasta, FastaRecord

from fastaSplit import fastaSplit


def test_fasta():
    name = "test this is a test"
    seq = "aaggccttss"

    seqobj = FastaRecord(name, seq)

    print("id: %s\ndesc: %s" % (seqobj.id, seqobj.description))

    text = str(seqobj)

    with open("test.fasta", "w") as fh:
        fh.write("%s\n%s\n%s\n" % (text,text,text))

    seqio = open_fasta("test.fasta")

    for s in seqio:
        print(s.id)

    fastaSplit(["test.fasta"], "length", 1, "split")


def main():
    test_fasta()

if __name__ == "__main__":
    main()

