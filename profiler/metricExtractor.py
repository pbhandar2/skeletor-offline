# coding=utf-8

"""
Extracting metrics from the trace

Author: Pranav Bhandari <bhandaripranav94@gmail.com> 2018/11
"""

from traceReader.abstractReader import AbstractReader

# it wouldn't work without this in mjolnir
import matplotlib
matplotlib.use("agg")

import matplotlib.pyplot as plt
import numpy as np 
from statsmodels.tsa.stattools import acf
from scipy.stats import describe

DEF_WINDOW_SIZE=300


'''
	Fix the following parameters:
		1. 
'''

class MetricExtractor():

	def __init__(self, reader, window_size=DEF_WINDOW_SIZE):

		assert isinstance(reader, AbstractReader), \
			"This is not a valid reader: {}".format(reader)

		self.reader = reader
		self.metrics = None
		self.window = window_size
		self.window_metrics_array = []

	def extract_metric(self, start=-1, end=-1, window_size=DEF_WINDOW_SIZE):

		print("Metric Extraction initiated ...")

		window_metrics_array = []
		window_start_time = None

		metrics = {
			"read_count": 0,
			"write_count": 0,
			"total_io": 0,
			"read_write_ratio": None,
			"read_rate": None,
			"write_rate": None,
			"io_rate": None,
			"total_io_size": 0,
			"total_read_size": 0,
			"total_write_size": 0,
			"average_read_size": None,
			"average_write_size": None,
			"average_io_size": None,
			"min_read_size": None,
			"min_write_size": None,
			"max_read_size": None,
			"max_write_size": None,
			"fano": {},
			"autocorrelation": {},
			"moments": {}
		}

		cur_window_metrics = {
			"read_count": 0,
			"write_count": 0,
			"total_io": 0,
			"read_write_ratio": None,
			"read_rate": None,
			"write_rate": None,
			"io_rate": None,
			"total_io_size": 0,
			"total_read_size": 0,
			"total_write_size": 0,
			"average_read_size": None,
			"average_write_size": None,
			"average_io_size": None,
			"min_read_size": None,
			"min_write_size": None,
			"max_read_size": None,
			"max_write_size": None,
			"fano": {}
		} 

		cur_data = self.reader.get_next_line_data()

		while cur_data:

			if window_start_time == None:
				window_start_time = self.reader.clock.cur_time
			elif (self.reader.clock.cur_time - window_start_time).total_seconds() >= self.window:
				#print("Start time {} and end time {}".format(window_start_time, self.reader.clock.cur_time))
				window_metrics_array.append(cur_window_metrics)
				cur_window_metrics = {
					"read_count": 0,
					"write_count": 0,
					"total_io": 0,
					"read_write_ratio": None,
					"read_rate": None,
					"write_rate": None,
					"io_rate": None,
					"total_io_size": 0,
					"total_read_size": 0,
					"total_write_size": 0,
					"average_read_size": None,
					"average_write_size": None,
					"average_io_size": None,
					"min_read_size": None,
					"min_write_size": None,
					"max_read_size": None,
					"max_write_size": None,
					"fano": None
				} 
				window_start_time = self.reader.clock.cur_time

			if cur_data["io_type"] == 'r':
				metrics["read_count"] += 1
				metrics["total_read_size"] += cur_data["size"]
				cur_window_metrics["read_count"] += 1
				cur_window_metrics["total_read_size"] += cur_data["size"]

				if metrics["min_read_size"] == None:
					metrics["min_read_size"] = cur_data["size"]
				elif metrics["min_read_size"] > cur_data["size"]:
					metrics["min_read_size"] = cur_data["size"]

				if cur_window_metrics["min_read_size"] == None:
					cur_window_metrics["min_read_size"] = cur_data["size"]
				elif cur_window_metrics["min_read_size"] > cur_data["size"]:
					cur_window_metrics["min_read_size"] = cur_data["size"]

				if metrics["max_read_size"] == None:
					metrics["max_read_size"] = cur_data["size"]
				elif metrics["max_read_size"] < cur_data["size"]:
					metrics["max_read_size"] = cur_data["size"]

				if cur_window_metrics["max_read_size"] == None:
					cur_window_metrics["max_read_size"] = cur_data["size"]
				elif cur_window_metrics["max_read_size"] < cur_data["size"]:
					cur_window_metrics["max_read_size"] = cur_data["size"]

			else:
				metrics["write_count"] += 1
				metrics["total_write_size"] += cur_data["size"]
				cur_window_metrics["write_count"] += 1
				cur_window_metrics["total_write_size"] += cur_data["size"]

				if metrics["min_write_size"] == None:
					metrics["min_write_size"] = cur_data["size"]
				elif metrics["min_write_size"] > cur_data["size"]:
					metrics["min_write_size"] = cur_data["size"]

				if cur_window_metrics["min_write_size"] == None:
					cur_window_metrics["min_write_size"] = cur_data["size"]
				elif cur_window_metrics["min_write_size"] > cur_data["size"]:
					cur_window_metrics["min_write_size"] = cur_data["size"]

				if metrics["max_write_size"] == None:
					metrics["max_write_size"] = cur_data["size"]
				elif metrics["max_write_size"] < cur_data["size"]:
					metrics["max_write_size"] = cur_data["size"]

				if cur_window_metrics["max_write_size"] == None:
					cur_window_metrics["max_write_size"] = cur_data["size"]
				elif cur_window_metrics["max_write_size"] < cur_data["size"]:
					cur_window_metrics["max_write_size"] = cur_data["size"]

			metrics["total_io"] += 1
			metrics["total_io_size"] += cur_data["size"]
			cur_window_metrics["total_io"] += 1
			cur_window_metrics["total_io_size"] += cur_data["size"]
			cur_data = self.reader.get_next_line_data()


		if metrics["write_count"] > 0:
			metrics["read_write_ratio"] = metrics["read_count"]/metrics["write_count"]
			metrics["write_rate"] = metrics["write_count"]/self.reader.clock.time_elasped.total_seconds()
			metrics["average_write_size"] = metrics["total_write_size"]/metrics["write_count"]

		if metrics["read_count"] > 0:
			metrics["read_rate"] = metrics["read_count"]/self.reader.clock.time_elasped.total_seconds()
			metrics["average_read_size"] = metrics["total_read_size"]/metrics["read_count"]
		

		if metrics["read_count"] > 0 and metrics["write_count"] > 0:
			metrics["io_rate"] = metrics["total_io"]/self.reader.clock.time_elasped.total_seconds()
			metrics["average_io_size"] = metrics["total_io_size"]/metrics["total_io"]

			for window_metrics in window_metrics_array:

				if window_metrics["write_count"] > 0:
					window_metrics["read_write_ratio"] = window_metrics["read_count"]/metrics["write_count"]
					window_metrics["write_rate"] = window_metrics["write_count"]/window_size
					window_metrics["average_write_size"] = window_metrics["total_write_size"]/window_metrics["write_count"]

				if window_metrics["read_count"] > 0:
					window_metrics["read_rate"] = window_metrics["read_count"]/window_size
					window_metrics["average_read_size"] = window_metrics["total_read_size"]/window_metrics["read_count"]

				if window_metrics["read_count"] > 0 and window_metrics["write_count"] > 0:
					window_metrics["io_rate"] = window_metrics["total_io"]/window_size
					window_metrics["average_io_size"] = window_metrics["total_io_size"]/window_metrics["total_io"]

		self.metrics = metrics
		self.window_metrics_array = window_metrics_array

		self.get_fano_factor("read_count")
		self.get_fano_factor("write_count")
		self.get_fano_factor("total_io")
		self.get_fano_factor("total_io_size")
		self.get_fano_factor("total_read_size")
		self.get_fano_factor("total_write_size")

		self.get_autocorrelation("read_count")
		self.get_autocorrelation("write_count")
		self.get_autocorrelation("total_io")
		self.get_autocorrelation("total_io_size")
		self.get_autocorrelation("total_read_size")
		self.get_autocorrelation("total_write_size")

		self.get_moments("read_count")
		self.get_moments("write_count")
		self.get_moments("total_io")
		self.get_moments("total_io_size")
		self.get_moments("total_read_size")
		self.get_moments("total_write_size")


	def get_fano_factor(self, attribute):

		# print("Fano factor of {}".format(attribute))

		attribute_array = np.zeros(len(self.window_metrics_array))
		for i, window_metric in enumerate(self.window_metrics_array):
			attribute_array[i] = window_metric[attribute]
			
		variance = np.var(attribute_array)
		mean = np.mean(attribute_array)

		fano = variance/mean
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








		




		






		



