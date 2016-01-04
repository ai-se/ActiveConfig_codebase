from __future__ import with_statement
from mmap import mmap


def count_number_of_lines(filename):
    """
    Source: http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
    :param filename: Name of the files
    :return: Number of lines in the files
    """
    f = open(filename, "r+")
    buf = mmap(f.fileno(), 0)
    lines = 0
    readline = buf.readline
    while readline(): lines += 1
    return lines