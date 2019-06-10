import sys, json

import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

import numpy as np


sys.path.append('../')

from skeletor import Skeletor

#@profile
def my_func():
	processor = Skeletor()
	processor.open_file("web_1.csv.gz", "../trace_config.json", "MSR-Cambridge")
	profiler = processor.get_metric_extractor()

	profiler.extract_metric()
	# print("Here are the metrics!")
	# print(json.dumps(profiler.metrics, indent=4, sort_keys=True))
	# print(len(profiler.window_metrics_array))

	profiler.get_access_distribution()
	profiler.plot_access_distribution()
	


if __name__ == '__main__':
    my_func()