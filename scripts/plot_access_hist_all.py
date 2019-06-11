'''
	The script takes the location of a folder as an input and creates access histogram for all files in the folder. 
'''

import sys, os

sys.path.append('../')

from skeletor import Skeletor

folder_location = sys.argv[1]

file_list = os.walk(folder_location).__next__()[2]

for file_name in file_list:

	try:

		file_location = os.path.join(folder_location, file_name)

		print("processing file {}".format(file_location))

		processor = Skeletor()
		processor.open_file(file_location, "../trace_config.json", "MSR-Cambridge")

		profiler = processor.get_metric_extractor()
		profiler.extract_metric()

		profiler.plot_access_distribution()
		profiler.plot_reuse_distance_distribution()

		json_file_name = "metric_{}.json".format(file_name)

		with open(json_file_name, 'w+') as json_file:  
		    json.dump(profiler.metrics, json_file, indent=4)
		    json_file.close()

		del processor

		print("done processing file {}".format(file_location))

	except Exception as inst:

		print(type(inst))
		print(inst.args)
		print(inst)
		print("error processing file {}".format(file_location))

