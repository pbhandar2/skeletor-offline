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
from lib.general import check_config, get_file_list, get_reuse_distance_features, get_hit_rate
from const import *
import json

import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt
from pathlib import Path


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

    def get_metric_extractor(self, window_size=DEF_WINDOW_SIZE):
        """
        Returns the next line of the trace file.
        """

        if self.reader:
            if self.profiler is None:
                self.profiler = MetricExtractor(self.reader, window_size)
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

    def workload_change(self):
        self.profiler = self.get_metric_extractor(window_size=86400)
        self.profiler.extract_metric()
        file_name = Path(self.file_loc).name

        reuse_distance_array = self.profiler.reuse_distance_array

        plt.figure()
        plt.title("Hit Rate Curve for each day of FIU trace \n : {}".format(file_name))
        plt.xlabel("Cache Size")
        plt.ylabel("Hit Rate")

        window_count = 0
        for start, end in self.profiler.window_index:
            rd_stats, hit_rate_array = get_reuse_distance_features(reuse_distance_array[start:end])
            hit_rate_list = [0.7, 0.8, 0.9]
            cur_hr = 0
            for i, hr in enumerate(hit_rate_array):
                if hr > hit_rate_list[cur_hr]:
                    rd_stats["hr_{}".format(hit_rate_list[cur_hr])] = i
                    cur_hr += 1
                    if cur_hr == len(hit_rate_list):
                        break

            data_name = "{}_{}".format(file_name, window_count)
            rd_stats["name"] = data_name
            plt.plot(hit_rate_array, label="{}".format(window_count))
            window_count += 1
            print(rd_stats)
            with open("{}_{}.json".format(file_name, window_count), 'w+') as outfile:
                try:
                    json.dump(json.dumps(rd_stats), outfile)
                except TypeError:
                    print("Error in file: {}, start: {} and end: {}".format(file_name, start, end))

        plt.legend()
        plt.savefig("{}_{}.png".format(file_name, window_count))
        plt.close()

    def __del__(self):
        print("Destroyed skeletor object!")
