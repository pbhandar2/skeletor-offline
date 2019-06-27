# coding=utf-8

"""
The module that extracts metrics from a given trace.
Author: Pranav Bhandari <bhandaripranav94@gmail.com> 2018/11
"""

from traceReader.abstractReader import AbstractReader
from profiler.splayTree import SplayTree

# it wouldn't work without this in mjolnir
import matplotlib

matplotlib.use("agg")

import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.stattools import acf
from scipy.stats import describe
from const import *
from copy import copy
from collections import Counter
import math


class MetricExtractor():
    def __init__(self, reader, window_size=DEF_WINDOW_SIZE):

        assert isinstance(reader, AbstractReader), \
            "This is not a valid reader: {}".format(reader)

        self.reader = reader
        self.reuse_distance_array = []
        self.page_accessed = []
        self.metrics = {
            "num_sequential_page_access": 0,
            "sequential_page_access_length": {
                "min": math.inf,
                "max": 0,
                "mean": 0,
                "total": 0
            }
        }

        self.splay_tree = SplayTree()
        self.prev_page = None
        self.prev_block = None

    def process_reuse_distance(self, cur_data):
        cur_page = math.floor(cur_data["block"] / self.reader.block_size)

        if self.reader.trace_type == "FIU":
            end_page = math.floor((cur_data["block"] + cur_data["size"] * 512) / self.reader.block_size)
        else:
            end_page = math.floor((cur_data["block"] + cur_data["size"]) / self.reader.block_size)

        while cur_page <= end_page:
            reuse_distance = self.splay_tree.find(cur_page)
            self.page_accessed.append(cur_page)
            self.reuse_distance_array.append(reuse_distance)
            cur_page += 1

    def check_sequentiality(self, cur_data):
        # CHECK SEQUENTIALITY IN BLOCK GRANULARITY
        # GET INFORMATION ON THE SEQUENTIALITY LEGNTH
        # SHOULD BE A WAY TO DISTINGUISH READ/WRITE SEQUENTIALITY

        start_page = math.floor(cur_data["block"] / self.reader.block_size)

        if start_page == self.prev_page + 1:
            self.metrics.num_sequential_page_access += 1

    def extract_metric(self, window_size=DEF_WINDOW_SIZE):
        print("Metric Extraction initiated ...")

        cur_data = self.reader.get_next_line_data()

        while cur_data:
            self.process_reuse_distance(cur_data)

            # check for sequentiality in block and page granularity
            self.check_sequentiality(cur_data)

            cur_data = self.reader.get_next_line_data()

        # 	if window_start_time == None:
        # 		window_start_time = self.reader.clock.cur_time
        # 	elif (self.reader.clock.cur_time - window_start_time).total_seconds() >= self.window:
        # 		#print("Start time {} and end time {}".format(window_start_time, self.reader.clock.cur_time))
        # 		window_metrics_array.append(cur_window_metrics)
        # 		cur_window_metrics = copy(METRICS)
        # 		window_start_time = self.reader.clock.cur_time
        # 		window_prev_access = 0

        # 	if cur_data["block"] - prev_access == self.reader.block_size:
        # 		metrics["sequential"] += 1
        # 		cur_window_metrics["sequential"] += 1
        # 	else:
        # 		metrics["random"] += 1
        # 		cur_window_metrics["random"] += 1

        # 	metrics["sequential"] += int(cur_data["size"]/self.reader.block_size)
        # 	cur_window_metrics["sequential"] += int(cur_data["size"]/self.reader.block_size)

        # 	for i in range(int(cur_data["size"]/self.reader.block_size)):
        # 		# print("updating {}".format(cur_data["block"] + i*self.reader.block_size))

        # 		block_address = cur_data["block"] + i*self.reader.block_size
        # 		access_number += 1

        # 		self.blocks_accessed.append(block_address)
        # 		access_distribution[block_address] += 1

        # 		if block_address not in reuse_distance_dict:
        # 			reuse_distance_dict[block_address] = [-1]
        # 			reuse_distance_counter[-1] += 1
        # 		else:
        # 			reuse_distance = access_number - prev_access_dict[block_address] - 1
        # 			reuse_distance_dict[block_address].append(reuse_distance)
        # 			reuse_distance_counter[reuse_distance] += 1

        # 		prev_access_dict[block_address] = access_number

        # 	prev_access = cur_data["block"] + cur_data["size"]

        # 	if cur_data["io_type"] == 'r':
        # 		metrics["read_count"] += 1
        # 		metrics["total_read_size"] += cur_data["size"]
        # 		cur_window_metrics["read_count"] += 1
        # 		cur_window_metrics["total_read_size"] += cur_data["size"]

        # 		if metrics["min_read_size"] == None:
        # 			metrics["min_read_size"] = cur_data["size"]
        # 		elif metrics["min_read_size"] > cur_data["size"]:
        # 			metrics["min_read_size"] = cur_data["size"]

        # 		if cur_window_metrics["min_read_size"] == None:
        # 			cur_window_metrics["min_read_size"] = cur_data["size"]
        # 		elif cur_window_metrics["min_read_size"] > cur_data["size"]:
        # 			cur_window_metrics["min_read_size"] = cur_data["size"]

        # 		if metrics["max_read_size"] == None:
        # 			metrics["max_read_size"] = cur_data["size"]
        # 		elif metrics["max_read_size"] < cur_data["size"]:
        # 			metrics["max_read_size"] = cur_data["size"]

        # 		if cur_window_metrics["max_read_size"] == None:
        # 			cur_window_metrics["max_read_size"] = cur_data["size"]
        # 		elif cur_window_metrics["max_read_size"] < cur_data["size"]:
        # 			cur_window_metrics["max_read_size"] = cur_data["size"]

        # 	else:
        # 		metrics["write_count"] += 1
        # 		metrics["total_write_size"] += cur_data["size"]
        # 		cur_window_metrics["write_count"] += 1
        # 		cur_window_metrics["total_write_size"] += cur_data["size"]

        # 		if metrics["min_write_size"] == None:
        # 			metrics["min_write_size"] = cur_data["size"]
        # 		elif metrics["min_write_size"] > cur_data["size"]:
        # 			metrics["min_write_size"] = cur_data["size"]

        # 		if cur_window_metrics["min_write_size"] == None:
        # 			cur_window_metrics["min_write_size"] = cur_data["size"]
        # 		elif cur_window_metrics["min_write_size"] > cur_data["size"]:
        # 			cur_window_metrics["min_write_size"] = cur_data["size"]

        # 		if metrics["max_write_size"] == None:
        # 			metrics["max_write_size"] = cur_data["size"]
        # 		elif metrics["max_write_size"] < cur_data["size"]:
        # 			metrics["max_write_size"] = cur_data["size"]

        # 		if cur_window_metrics["max_write_size"] == None:
        # 			cur_window_metrics["max_write_size"] = cur_data["size"]
        # 		elif cur_window_metrics["max_write_size"] < cur_data["size"]:
        # 			cur_window_metrics["max_write_size"] = cur_data["size"]

        # 	metrics["total_io"] += 1
        # 	metrics["total_io_size"] += cur_data["size"]
        # 	cur_window_metrics["total_io"] += 1
        # 	cur_window_metrics["total_io_size"] += cur_data["size"]
        # 	cur_data = self.reader.get_next_line_data()


        # if metrics["write_count"] > 0:
        # 	metrics["read_write_ratio"] = metrics["read_count"]/metrics["write_count"]
        # 	metrics["write_rate"] = metrics["write_count"]/self.reader.clock.time_elasped.total_seconds()
        # 	metrics["average_write_size"] = metrics["total_write_size"]/metrics["write_count"]

        # if metrics["read_count"] > 0:
        # 	metrics["read_rate"] = metrics["read_count"]/self.reader.clock.time_elasped.total_seconds()
        # 	metrics["average_read_size"] = metrics["total_read_size"]/metrics["read_count"]


        # if metrics["read_count"] > 0 and metrics["write_count"] > 0:
        # 	metrics["io_rate"] = metrics["total_io"]/self.reader.clock.time_elasped.total_seconds()
        # 	metrics["average_io_size"] = metrics["total_io_size"]/metrics["total_io"]

        # 	for window_metrics in window_metrics_array:

        # 		if window_metrics["write_count"] > 0:
        # 			window_metrics["read_write_ratio"] = window_metrics["read_count"]/metrics["write_count"]
        # 			window_metrics["write_rate"] = window_metrics["write_count"]/window_size
        # 			window_metrics["average_write_size"] = window_metrics["total_write_size"]/window_metrics["write_count"]

        # 		if window_metrics["read_count"] > 0:
        # 			window_metrics["read_rate"] = window_metrics["read_count"]/window_size
        # 			window_metrics["average_read_size"] = window_metrics["total_read_size"]/window_metrics["read_count"]

        # 		if window_metrics["read_count"] > 0 and window_metrics["write_count"] > 0:
        # 			window_metrics["io_rate"] = window_metrics["total_io"]/window_size
        # 			window_metrics["average_io_size"] = window_metrics["total_io_size"]/window_metrics["total_io"]

        # self.metrics = metrics
        # self.window_metrics_array = window_metrics_array
        # self.access_distribution = access_distribution
        # self.reuse_distance_counter = reuse_distance_counter
        # self.reuse_distance_distribution = sorted(reuse_distance_counter.items())
        # self.reuse_distance_dict = reuse_distance_dict
        # self.metrics["top_10_reuse_distance"] = reuse_distance_counter.most_common(10)
        # self.metrics["top_10_accessed_block"] = access_distribution.most_common(10)

        # self.get_fano_factor("read_count")
        # self.get_fano_factor("write_count")
        # self.get_fano_factor("total_io")
        # self.get_fano_factor("total_io_size")
        # self.get_fano_factor("total_read_size")
        # self.get_fano_factor("total_write_size")

        # self.get_autocorrelation("read_count")
        # self.get_autocorrelation("write_count")
        # self.get_autocorrelation("total_io")
        # self.get_autocorrelation("total_io_size")
        # self.get_autocorrelation("total_read_size")
        # self.get_autocorrelation("total_write_size")

        # self.get_moments("read_count")
        # self.get_moments("write_count")
        # self.get_moments("total_io")
        # self.get_moments("total_io_size")
        # self.get_moments("total_read_size")
        # self.get_moments("total_write_size")

    def get_fano_factor(self, attribute):

        # print("Fano factor of {}".format(attribute))

        attribute_array = np.zeros(len(self.window_metrics_array))
        for i, window_metric in enumerate(self.window_metrics_array):
            attribute_array[i] = window_metric[attribute]

        variance = np.var(attribute_array)
        mean = np.mean(attribute_array)

        fano = variance / mean
        cur_fano = self.metrics["fano"]
        cur_fano[attribute] = fano
        self.metrics["fano"] = cur_fano

    def get_autocorrelation(self, attribute):

        # print("Autocorrelation of {}".format(attribute))

        attribute_array = np.zeros(len(self.window_metrics_array))
        for i, window_metric in enumerate(self.window_metrics_array):
            attribute_array[i] = window_metric[attribute]

        autocorr = acf(attribute_array)
        cur_autocorr = self.metrics["autocorrelation"]
        cur_autocorr[attribute] = autocorr.tolist()
        self.metrics["autocorrelation"] = cur_autocorr

    def get_moments(self, attribute):

        # print("Moments of {}".format(attribute))
        attribute_array = np.zeros(len(self.window_metrics_array))
        for i, window_metric in enumerate(self.window_metrics_array):
            attribute_array[i] = window_metric[attribute]

        stats = describe(attribute_array)

        moment_obj = {}
        moment_obj["variance"] = stats.variance
        moment_obj["skewness"] = stats.skewness
        moment_obj["kurtosis"] = stats.kurtosis

        self.metrics["moments"][attribute] = moment_obj

    def plot_access_distribution(self, figname=DEF_HISTOGRAM_FIG_NAME, limit=DEF_ACCESS_PLOT_LIMIT,
                                 width=DEF_HISTOGRAM_WIDTH):

        if self.access_distribution == None:
            self.extract_metric()

        count_filtered = self.access_distribution.most_common(limit)
        labels, values = zip(*count_filtered)
        indexes = np.arange(len(labels))
        plt.bar(indexes, values, width)
        # plt.xticks(indexes + width * 0.5, labels, rotation='vertical')
        plt.title("Access Distribution of first {} addresses from file {}".format(limit, self.reader.file_name))
        plt.xticks([], [])

        if figname == DEF_HISTOGRAM_FIG_NAME:
            figname = "{}_{}.png".format(DEF_HISTOGRAM_FIG_NAME, self.reader.file_name)

        plt.savefig(figname)
        plt.close()

    def plot_reuse_distance_distribution(self, figname=DEF_REUSE_HISTOGRAM_FIG_NAME, width=DEF_REUSE_HISTOGRAM_WIDTH,
                                         limit=DEF_REUSE_HISTOGRAM_PLOT_LIMIT):

        plt.figure(figsize=(80, 20))
        plt.yticks(fontsize=80)

        if self.reuse_distance_distribution == None:
            self.extract_metric()

        count_array = self.reuse_distance_distribution

        labels = []
        values = []

        for i in range(limit):
            labels.append(i)
            values.append(self.reuse_distance_counter[i])

        indexes = np.arange(len(labels))
        plt.bar(indexes, values, width)

        # plt.xticks(labels, labels, rotation='vertical')
        plt.title("Reuse Distance Distribution upto {} for file {}".format(limit, self.reader.file_name), fontsize=80)
        plt.xticks([], [])

        if figname == DEF_REUSE_HISTOGRAM_FIG_NAME:
            figname = "{}_{}.png".format(DEF_REUSE_HISTOGRAM_FIG_NAME, self.reader.file_name)

        plt.savefig(figname)
        plt.close()

    def __del__(self):
        print("Destroyed MetricExtractor object!")
