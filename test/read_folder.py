from skeletor import skeletor
import sys 
import os 

trace_folder = sys.argv[1]

trace_file_names = os.walk(trace_folder).__next__()[2]

for file_name in trace_file_names:
	trace_path = '{}{}'.format(trace_folder, file_name)
	print(trace_path)







