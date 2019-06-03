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

class MetricExtractor():

	def __init__(self, reader):

		assert isinstance(reader, AbstractReader), \
			"This is not a valid reader: {}".format(reader)

		self.reader = reader
		self.metrics = {
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
			"max_write_size": None
		}

	def extract_metric(self):

		print("Metric Extraction initiated ...")

		cur_data = self.reader.get_next_line_data()

		while cur_data:

			if cur_data["io_type"] == 'r':
				self.metrics["read_count"] += 1
				self.metrics["total_read_size"] += cur_data["size"]

				if self.metrics["min_read_size"] == None:
					self.metrics["min_read_size"] = cur_data["size"]
				elif self.metrics["min_read_size"] > cur_data["size"]:
					self.metrics["min_read_size"] = cur_data["size"]

				if self.metrics["max_read_size"] == None:
					self.metrics["max_read_size"] = cur_data["size"]
				elif self.metrics["max_read_size"] < cur_data["size"]:
					self.metrics["max_read_size"] = cur_data["size"]

			else:
				self.metrics["write_count"] += 1
				self.metrics["total_write_size"] += cur_data["size"]

				if self.metrics["min_write_size"] == None:
					self.metrics["min_write_size"] = cur_data["size"]
				elif self.metrics["min_write_size"] > cur_data["size"]:
					self.metrics["min_write_size"] = cur_data["size"]

				if self.metrics["max_write_size"] == None:
					self.metrics["max_write_size"] = cur_data["size"]
				elif self.metrics["max_write_size"] < cur_data["size"]:
					self.metrics["max_write_size"] = cur_data["size"]

			self.metrics["total_io"] += 1
			self.metrics["total_io_size"] += cur_data["size"]
			cur_data = self.reader.get_next_line_data()

		self.metrics["read_write_ratio"] = self.metrics["read_count"]/self.metrics["write_count"]
		self.metrics["read_rate"] = self.metrics["read_count"]/self.reader.clock.time_elasped.total_seconds()
		self.metrics["write_rate"] = self.metrics["write_count"]/self.reader.clock.time_elasped.total_seconds()
		self.metrics["io_rate"] = self.metrics["total_io"]/self.reader.clock.time_elasped.total_seconds()
		self.metrics["average_read_size"] = self.metrics["total_read_size"]/self.metrics["read_count"]
		self.metrics["average_write_size"] = self.metrics["total_write_size"]/self.metrics["write_count"]
		self.metrics["average_io_size"] = self.metrics["total_io_size"]/self.metrics["total_io"]

		





		




		






		



