# coding=utf-8

"""
msrReader reads the MSR traces. 
Author: Pranav Bhandari <bhandaripranav94@gmail.com> 2018/11
"""

import gzip
from traceReader.abstractReader import AbstractReader

class msrReader(AbstractReader):

    def __init__(self, file_loc, delimiter, fields, trace_type, num_skip=0, block_size=-1):
        super(msrReader, self).__init__(file_loc)
        self.file = gzip.open(file_loc, "r") # the file to be read
        self.num_lines = 0 # the number of lines in the trace file
        self.delimiter = delimiter
        self.fields = fields
        self.trace_type = trace_type
        self.block_size = block_size

        if (num_skip > 0):
            self.skip_lines(num_skip)

