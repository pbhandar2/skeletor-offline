# coding=utf-8

"""
gzReader reads the compressed gz trace files.
Author: Pranav Bhandari <bhandaripranav94@gmail.com> 2018/11
"""

import gzip
from traceReader.abstractReader import AbstractReader

class txtReader(AbstractReader):

    def __init__(self, file_loc, delimiter, fields, trace_type, clock, num_skip=0, block_size=-1):
        super(txtReader, self).__init__(file_loc)
        self.file = open(file_loc, "r") # the file to be read
        self.num_lines = 0 # the number of lines in the trace file
        self.delimiter = delimiter
        self.fields = fields
        self.trace_type = trace_type
        self.block_size = block_size
        self.clock = clock
        self.file_loc = file_loc
        if (num_skip > 0):
            self.skip_lines(num_skip)

    def get_next_line(self):
        self.num_lines += 1
        line = self.file.readline().rstrip()
        if (line):
            line_split = line.split(self.delimiter)
            self.clock.update_time(int(line_split[0]))
        return line

    def get_next_line_array(self):
        self.num_lines += 1
        return self.get_next_line().split(self.delimiter)

    def skip_lines(self, num_lines):
        self.num_lines += num_lines
        for i in range(num_lines):
            self.file.readline()
