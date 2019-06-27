import os, json, math
from ast import literal_eval

stats_dir = "./page_4096/0/reuse_stats"

file_list = os.walk(stats_dir).__next__()[2]
array_dict = []

with open("summary.csv", "w+") as g: 
	for file_name in file_list:

		with open(os.path.join(stats_dir, file_name)) as json_file: 

				data = literal_eval(json.load(json_file))

				#print(type(data))
				#print(data)


				max_reuse = data["minmax"][1]
				avg = data["mean"]
				var = data["variance"]
				skew = data["skewness"]
				kurt = data["kurtosis"]
				cache_size = data["min_cache_size_70"]
				unique_obj_ratio = data["unique_obj_ratio"]
				net_diff_in_cache_size = cache_size - int(math.ceil(avg))

				error = net_diff_in_cache_size/cache_size

				write_txt = "{},{},{},{},{},{},{},{},{},{}\n".format(
					file_name,
					max_reuse,
					avg, var, skew, kurt,
					cache_size, net_diff_in_cache_size,
					error, unique_obj_ratio)

				array_dict.append([file_name, max_reuse, avg, var, skew, kurt, cache_size, net_diff_in_cache_size, error, unique_obj_ratio])

				
				g.write(write_txt)

labels = ["file_name", "max", "mean", "var", "skew", "kurt", "size", "net_size", "error", "unique_ratio"]

array_dict = sorted(array_dict, key=lambda k: k[3])
from tabulate import tabulate
print(tabulate(array_dict, headers=labels))