# coding=utf-8

"""
Presenting the upper level API to the user

Currently supports:
- loading the trace file and getting the lines one by one

Author: Pranav Bhandari <bhandaripranav94@gmail.com> 2018/11
"""

import gzip
import json

from traceReader.gzReader import gzReader
from traceReader.timeReader import TimeReader
from traceReader.txtReader import txtReader
from profiler.ioProfiler import IOProfiler

class skeletor:

    def __init__(self):
        self.profiler = None
        self.config = None

    def open_file(self, file_loc, config_file, **kwargs):
        """
        Load a file.
        Param:
            file_loc -- The location of the file.
            fields -- The dictionary represents the name of the fields, the position in the line array, type and processing.
        Keyword arguments:
            trace_type -- The type of trace which dictates how it is loaded.
            file_format -- The format of the file.
            config -- The location of the config file. 
        """

        # Get the type of the trace if specified
        trace_type = None
        if "trace_type" in kwargs:
            trace_type = kwargs["trace_type"]

        # Setup the config file
        try:
            with open(config_file, 'r') as f:
                config_list = json.loads(f.read())

                # Get the first configuration if trace type is not specified 
                # Otherwise, look for a matching name for the trace type
                if not trace_type:
                    self.config = config_list[0]
                else:
                    for config in config_list:
                        if (config["name"] == trace_type):
                            self.config = config

            # If no configuration was found and a trace type was provided
            if not self.config:
                print("No configuration found relating to the given trace type")
                exit()

        except IOError:
            print ("Could not read file: {}. Make sure the config file exists.".format(config_file))
            exit()

        # Block size to check for serial access as it determines if an access is serial or not
        # E.g: 10 was accesssed then 18 it is serial if block size 8 not if block size is 4
        block_size = -1
        if "block_size" in self.config:
            block_size = self.config["block_size"]


        # The config file can contain multiple configuration the trace type variable denotes which
        # json entry to look at for the configuration
        if "trace_type" in kwargs:
            trace_type = kwargs["trace_type"]
            if (trace_type == "MSR-Cambridge"):
                self.reader = gzReader(file_loc, self.config["delimiter"], self.config["fields"], trace_type, block_size=block_size)
            elif (trace_type == "FIU"):
                clock = TimeReader(self.config["time_unit"], self.config["time_type"], self.config["time_format"])
                self.reader = txtReader(file_loc, self.config["delimiter"], self.config["fields"], trace_type, clock)
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
        
        #print("THIS IS THE I/O PROFILER.")

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
