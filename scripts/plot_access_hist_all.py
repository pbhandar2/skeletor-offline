'''
	The script takes the location of a folder as an input and creates access histogram for all files in the folder. 
'''

import sys, os

sys.path.append('../')

from skeletor import Skeletor

folder_location = sys.argv[1]

file_list = os.walk(folder_location).__next__()[2]

for file_name in file_list:

	file_location = os.path.join(folder_location, file_name)

	processor = Skeletor()
	processor.open_file(file_location, "../trace_config.json", "MSR-Cambridge")

	profiler = processor.get_metric_extractor()
	profiler.extract_metric()

	profiler.get_access_distribution()
	profiler.plot_access_distribution()

