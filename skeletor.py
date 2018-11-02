# coding=utf-8

"""
Presenting the upper level API to the user

Currently supports:
- loading the trace file and getting the lines one by one

Author: Pranav Bhandari <bhandaripranav94@gmail.com> 2018/11
"""

import gzip

from traceReader.gzReader import gzReader
from profiler.ioProfiler import IOProfiler

MSR_format = {
    "name": "MSR-Cambridge",
    "file_format": "gz",
    "delimiter": ",",
    "format": "gz",
    "block_size": 512,
    "fields": {
      "time": {
        "index": 0,
        "type": "float"
      },
      "hostname": {
        "index": 1,
        "type": "string"
      },
      "disknumber": {
        "index": 2,
        "type": "integer"
      },
      "io_type": {
        "index": 3,
        "type": "string",
        "values": {
          "read": "Read",
          "write": "Write"
        }
      },
      "block": {
        "index": 4,
        "type": "integer"
      },
      "size": {
        "index": 5,
        "type": "integer"
      },
      "response_time": {
        "index": 6,
        "type": "integer"
      }
    }
}

class skeletor:

    def __init__(self):
        self.delimiter = None
        self.fields = None
        self.profiler = None

    def open_file(self, file_loc, **kwargs):
        """
        Load a file.
        Param:
            file_loc -- The location of the file.
            fields -- The dictionary represents the name of the fields, the position in the line array, type and processing.
        Keyword arguments:
            trace_type -- The type of trace which dictates how it is loaded.
            file_format -- The format of the file.
        """

        block_size = -1
        if "block_size" in kwargs:
            block_size = kwargs["block_size"]

        if "trace_type" in kwargs:
            trace_type = kwargs["trace_type"]
            if (trace_type == "MSR_Cambridge"):
                self.reader = gzReader(file_loc, MSR_format["delimiter"], MSR_format["fields"], trace_type, block_size=MSR_format["block_size"])
            elif (trace_type == "custom" or trace_type == None):
                # if file type is not speicified expecting the file format at least
                if (kwargs["file_format"] == None):
                    raise ValueError('For file_type="custom" or None, you need to pass a file format. Refer to README for the supported file formats.')
                else:
                    self.format = kwargs["file_format"]
        elif "file_format" in kwargs:
            self.format = kwargs["file_format"]
        else:
            raise ValueError('You have to specify the file_format or use on the of predefine file_type. Refer to README for the supported file formats and file types.')

    def get_next_line(self):
        """
        Returns the next line of the trace file.
        """

        return self.reader.get_next_line()

    def get_next_line_array(self):
        """
        Returns the next line of the trace file.
        """

        return self.reader.get_next_line_array()

    def get_io_profiler(self):
        """
        Returns the next line of the trace file.
        """
        print("THIS IS THE I/O PROFILER.")

        if (self.reader):
            if (self.profiler == None):
                self.profiler = IOProfiler(self.reader)
        else:
            raise Exception("You need to open a file using open_file in order to get data to plot.")

        return self.profiler

    def plot_access(self):
        """
            The first thing that I need to do is get the data necessary. I need
            to use the profiler to get the x-axis which is time and y-axis which
            is block number and
        """
        print("Get access plot.")

    def plot_size_dist(self):
        """
            I need to get the size distribution for things in the
        """
        if (self.reader == None):
            if (self.profiler == None):
                self.profiler = IOProfiler(self.reader)

        else:
            raise Exception("You need to open a file using open_file in order to get data to plot.")

    def test_print(self):
        print("TESTING THE CLASS")
