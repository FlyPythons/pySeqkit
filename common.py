
from __future__ import absolute_import

import logging
import os


LOG = logging.getLogger(__name__)


def check_paths(*paths):
    """
    check the existence of paths
    :param paths:
    :return: abs paths
    """
    r = []
    for path in paths:
        path = os.path.abspath(path)
        if not os.path.exists(path):
            msg = "File not found '{path}'".format(**locals())
            LOG.error(msg)
            raise Exception(msg)
        r.append(path)
    if len(r) == 1:
        return r[0]
    return r


def fofn2list(filename):
    """
    read file and return a file list
    :param filename:
    :return:
    """
    r = []

    with open(filename) as fh:
        for line in fh.readlines():
            line = line.strip()
            if line:
                r.append(line)

    return r


def mkdir(d):
    """
    from FALCON_KIT
    :param d:
    :return:
    """
    d = os.path.abspath(d)
    if not os.path.isdir(d):
        LOG.debug('mkdir {!r}'.format(d))
        os.makedirs(d)
    else:
        LOG.debug('mkdir {!r}, {!r} exist'.format(d, d))

    return d


def touch(*paths):
    """
    touch a file.
    from FALCON_KIT
    """

    for path in paths:
        if os.path.exists(path):
            os.utime(path, None)
        else:
            open(path, 'a').close()
            LOG.debug('touch {!r}'.format(path))
