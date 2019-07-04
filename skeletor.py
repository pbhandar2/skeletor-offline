# coding=utf-8

"""
Presenting the upper level API to the user

Currently supports:
- get the reuse distance of each request

Author: Pranav Bhandari <bhandaripranav94@gmail.com> 2018/11
"""

from traceReader.gzReader import GZReader
from traceReader.tarReader import TARReader
from profiler.ioProfiler import IOProfiler
from profiler.metricExtractor import MetricExtractor
from lib.general import check_config


class Skeletor:

    def __init__(self):
        self.profiler = None
        self.config = None
        self.file_loc = None
        self.reader = None

    def open_file(self, file_loc, config_file_location, trace_type):
        """
        Load a file.
        Param:
            file_loc -- The location of the file.
            config_file_location -- The location of the configuration file. 
            trace_type -- The type of trace used to identify the correct configuration from the configuration file 
        """

        self.file_loc = file_loc
        self.config = check_config(config_file_location, trace_type)

        if trace_type == "MSR-Cambridge":
            self.reader = GZReader(file_loc, self.config, trace_type)
        elif trace_type == "FIU":
            self.reader = TARReader(file_loc, self.config, trace_type)
        else:
            raise ValueError("""The trace_type is not included in the config file. Please
                make sure that you have the config file set up correctly with the correct
                trace_type name.""")


    def get_metric_extractor(self):
        """
        Returns the next line of the trace file.
        """

        if self.reader:
            if self.profiler is None:
                self.profiler = MetricExtractor(self.reader)
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
        if self.reader is None:
            if self.profiler is None:
                self.profiler = IOProfiler(self.reader)

        else:
            raise Exception("You need to open a file using open_file in order to get data to plot.")

    def __del__(self):
        print("Destroyed skeletor object!")
