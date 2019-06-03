# coding=utf-8

"""
Presenting the upper level API to the user

Currently supports:
- loading the trace file and getting the lines one by one

Author: Pranav Bhandari <bhandaripranav94@gmail.com> 2018/11
"""

import gzip
import json
import logging

from traceReader.gzReader import gzReader
from traceReader.timeReader import TimeReader
from traceReader.txtReader import txtReader
from traceReader.clock import clock
from profiler.ioProfiler import IOProfiler
from lib.general import check_config

DEFAULT_BLOCK_SIZE = 512

class Skeletor:

    def __init__(self):
        self.profiler = None
        self.config = None

    def open_file(self, file_loc, config_file_location, trace_type):
        """
        Load a file.
        Param:
            file_loc -- The location of the file.
            config_file_location -- The location of the configuration file. 
            trace_type -- The type of trace used to identify the correct configuration from the configuration file 
        """

        self.config = check_config(config_file_location, trace_type)

        block_size = None
        if "block_size" in self.config:
            block_size = self.config["block_size"]
        else:
            self.config["block_size"] = DEFAULT_BLOCK_SIZE
            logging.warning("Block Size not included in the config file using the default block size of 512")

        clock_obj = None
        if "clock_config" in self.config:
            clock_type = self.config["clock_config"]["type"]

            if clock_type == "windows":
                self.config["clock"] = clock(clock_type)

        else:
            unit = "nano"
            _type = "relative"



        if (trace_type == "MSR-Cambridge"):
            self.reader = gzReader(file_loc, self.config, trace_type)




        # The config file can contain multiple configuration the trace type variable denotes which
        # json entry to look at for  the configuration
        # if "trace_type" in kwargs:
        #     trace_type = kwargs["trace_type"]
        #     if (trace_type == "MSR-Cambridge"):
        #         self.reader = gzReader(file_loc, self.config["delimiter"], self.config["fields"], trace_type, block_size=block_size)
        #     elif (trace_type == "FIU"):
        #         clock = TimeReader(self.config["time_unit"], self.config["time_type"], self.config["time_format"])
        #         self.reader = txtReader(file_loc, self.config["delimiter"], self.config["fields"], trace_type, clock)
        #     elif (trace_type == "custom" or trace_type == None):
        #         # if file type is not speicified expecting the file format at least
        #         if (kwargs["file_format"] == None):
        #             raise ValueError('For file_type="custom" or None, you need to pass a file format. Refer to README for the supported file formats.')
        #         else:
        #             self.format = kwargs["file_format"]
        # elif "file_format" in kwargs:
        #     self.format = kwargs["file_format"]
        # else:
        #     raise ValueError('You have to specify the file_format or use on the of predefine file_type. Refer to README for the supported file formats and file types.')

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
        
        # print("THIS IS THE I/O PROFILER.")

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
