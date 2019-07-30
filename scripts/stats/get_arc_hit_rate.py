from PyMimircache import Cachecow
import sys, os, json, numpy, math
from lib import get_percentiles 


def main(file_name, output_folder):

	# setting up cachecow and the profiler 
	c = Cachecow();
	params = {
		"init_params": {
			"label": 1,
			"fmt": "{}\n"
		}
	}

	r = c.open(file_name,"c","c", **params)
	num_req = c.num_of_req()
	profiler = c.profiler(algorithm="ARC", cache_size=math.floor(num_req*0.8), bin_size=1)
	hit_rate = profiler.get_hit_ratio()
	max_hit_rate = hit_rate[-1]

	hit_rate_string = "\n".join(str(h) for h in hit_rate)

	# write the hit ratio to a file 
	with open("{}/arc_HR_{}.csv".format(output_folder, file_name), 'w+') as f:
		f.write(hit_rate_string)


if __name__ == "__main__":
	folder_dir = sys.argv[1]
	output_folder_dir = sys.argv[2]
	file_list = os.walk(folder_dir).__next__()[2]

	for file_name in file_list:
		if ".csv" in file_name:
			file_dir = os.path.join(folder_dir, file_name)
			main(file_dir, output_folder_dir)

