from skeletor import skeletor
import sys 
import os 

trace_folder = sys.argv[1]
output_path = sys.argv[2]

trace_file_names = os.walk(trace_folder).__next__()[2]

for file_name in trace_file_names:
	trace_path = '{}{}'.format(trace_folder, file_name)
	if (os.path.getsize(trace_path)):
		out_path = '{}{}'.format(output_path, file_name)
		processor = skeletor()
		processor.open_file(trace_path, "../trace_config.json", trace_type="FIU")
		profiler = processor.get_io_profiler()
		profiler.plot_scatter_interval("block", out_path, 1800, binSize=0, markerSize=5)









