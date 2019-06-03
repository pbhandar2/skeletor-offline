# coding=utf-8

"""
gzReader reads the compressed gz trace files.
Author: Pranav Bhandari <bhandaripranav94@gmail.com> 2018/11
"""

import gzip
import numpy as np 

from traceReader.abstractReader import AbstractReader
from traceReader.readerLib import process_line

class gzReader(AbstractReader):

    def __init__(self, file_loc, config, trace_type):
        super(gzReader, self).__init__(file_loc)
        self.file = gzip.open(file_loc, "r") # the file to be read
        self.num_lines = 0 # the number of lines in the trace file
        self.delimiter = config["delimiter"]
        self.fields = config["fields"]
        self.trace_type = trace_type
        self.block_size = config["block_size"]
        self.cur_line = None
        self.cur_fields = None
        self.num_skip = config["num_skip"] if "num_skip" in config else 0
        self.clock = config["clock"]

        self.data = {}
        for key in self.fields:
            self.data[key] = np.array([])

        if (self.num_skip > 0):
            self.skip_lines(self.num_skip)
 
    def get_next_line(self):
        self.num_lines += 1
        self.cur_line = self.file.readline().decode("utf-8").rstrip()

        if len(self.cur_line):
            self.cur_fields = process_line(self.cur_line.split(self.delimiter), self.fields)

        for key in self.cur_fields:
            if key == "time":
                self.data[key] = np.append(self.data[key], self.clock.get_time(self.cur_fields[key]))
            else:
                self.data[key] = np.append(self.data[key], self.cur_fields[key])

        return self.cur_line

    def get_next_line_data(self):
        self.get_next_line()
        return self.cur_fields

    def get_next_line_array(self):
        self.num_lines += 1
        return self.get_next_line().split(self.delimiter)

    def skip_lines(self, num_lines):
        self.num_lines += num_lines
        for i in range(num_lines):
            self.file.readline()

