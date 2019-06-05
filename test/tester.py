import sys, json

sys.path.append('../')

from skeletor import Skeletor

#@profile
def my_func():
	processor = Skeletor()
	processor.open_file("web_1.csv.gz", "../trace_config.json", "MSR-Cambridge")
	profiler = processor.get_metric_extractor()
	profiler.extract_metric()

	# print(len(profiler.reader.data["io_type"]))
	# print(len(profiler.reader.data["time"]))
	# print(profiler.reader.data["io_type"][1:10])
	# print(profiler.reader.clock.time_elasped)

	print("Here are the metrics!")
	print(json.dumps(profiler.metrics, indent=4, sort_keys=True))


	print(len(profiler.window_metrics_array))


if __name__ == '__main__':
    my_func()