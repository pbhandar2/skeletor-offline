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
        	"read_count": None,
        	"write_count": None,
        	"read_write_ratio": None,
        	"read_rate": None,
        	"write_rate": None,
        	"io_rate": None,
        	"total_io_size": None,
        	"total_read_size": None,
        	"total_write_size": None,
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



    	




    	






    	



