
import gzip
import logging
import os.path

LOG = logging.getLogger(__name__)
ALLOWED_FASTQ = [".fq", ".fastq", ".fq.gz", ".fastq.gz"]


class FastqRecord(object):
    """
    Object to process a fastq record
    """
    def __init__(self, description, seq, desc2, quality):
        self._description = description[1:]
        self._seq = seq
        self._desc2 = desc2
        self._quality = quality

    @property
    def identifier(self):
        """
        The 1st line of FASTQ file, @ is not included
        :return:
        """
        return self._description

    @property
    def id(self):
        """
        The name of the FASTQ record, equal to the identifier
        up to the first whitespace.
        :return:
        """
        return self._description.split()[0]

    @property
    def seq(self):
        """
        The sequence of the FASTQ record, the 2nd line
        :return:
        """
        return self._seq

    @property
    def quality(self):
        """
        The quality of the sequence, the 4th line
        :return:
        """
        return self._quality

    def trim(self, left, right):
        """
        return a trimmed fastq record
        :param left: the number of bases to be trimmed on left
        :param right: the number of bases to be trimmed on ringht
        :return:
        """
        return FastqRecord(self._description, self.seq[left:-right], self._desc2, self.quality[left:-right])

    @classmethod
    def from_string(cls, string):
        string = string.strip()
        lines = string.splitlines()

        assert len(lines) == 4
        assert lines[0].startswith("@")
        assert lines[2].startswith("+")

        return FastqRecord(*lines)

    def __str__(self):
        return "@{}\n{}\n{}\n{}".format(self.identifier, self._seq, self._desc2, self.quality)

    def __len__(self):
        return len(self._seq)


def check_format(filename):
    """
    check the format of file
    :param filename:
    :return:
    """

    if any([f for f in ALLOWED_FASTQ if filename.endswith(f)]):
        return 0
    else:
        msg = "file format is not in %s" % ALLOWED_FASTQ
        raise Exception(msg)


def yield_fastq_records(stream):
    """
    yield fastq records from stream
    :param stream: a stream object
    :return:
    """

    n = 0
    string = ""

    for line in stream:
        line = line.strip()

        if not line:
            continue

        n += 1
        string += "%s\n" % line

        if n == 4:
            yield FastqRecord.from_string(string)
            n = 0
            string = ""


def open_fastq(filename):
    """
    read fastq file and return fastq records
    :param filename:
    :return:
    """
    check_format(filename)

    filename = os.path.abspath(filename)
    mode = 'r'

    LOG.info("Parse fastq sequences from %r" % filename)
    if filename.endswith(".gz"):
        stream = gzip.open(filename, mode)
    else:
        stream = open(filename, mode)

    return yield_fastq_records(stream)

