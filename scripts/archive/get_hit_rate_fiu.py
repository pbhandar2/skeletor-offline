import sys, os, json, numpy, math
from PyMimircache import Cachecow
from scipy.stats import describe 

def default(o):
	return int(o)

CONSIDER_NEG_REUSE = 1

# set the file name 
file_name = "web_1.csv.gz_4096.csv"
if len(sys.argv) > 1:
	file_name = sys.argv[1]
if len(sys.argv) > 2:
	CONSIDER_NEG_REUSE = 0

# setting up cachecow and the profiler 
c = Cachecow();
params = {
	"init_params": {
		"label": 1,
		"fmt": "{}\n"
	}
}

r = c.open(file_name,"c","c", **params)
profiler = c.profiler(algorithm="LRU")

# get reuse distance and the hit rate array 
reuse_dist_array = profiler.get_reuse_distance()
hit_rate_array = profiler.get_hit_rate()

# reuse distance output file 
reuse_output_file_name = "{}_{}.csv".format(file_name, "reuse")

if not CONSIDER_NEG_REUSE:
	new_reuse = []

# counting the number of unique objects and also creating a new array of reuse distance that does not consider -1 value
num_unique_objs = 0
with open(reuse_output_file_name, 'w+') as f:
	for i, reuse_distance in enumerate(reuse_dist_array):

		if reuse_distance == -1:
			num_unique_objs += 1
		else:
			if not CONSIDER_NEG_REUSE:
				new_reuse.append(reuse_distance)

		f.write(str(reuse_distance))
		f.write("\n")

# getting the correct stat based on if we are counting the -1 or not 
if not CONSIDER_NEG_REUSE:
	stats = describe(new_reuse)
else:
	stats = describe(reuse_dist_array)

stats_ord_dict = stats._asdict()

stats_ord_dict["opt"] = hit_rate_array[-3]
stats_ord_dict["num_unique_obj"] = num_unique_objs
stats_ord_dict["unique_obj_ratio"] = num_unique_objs/len(reuse_dist_array)
stats_ord_dict["avg_hit_rate"] = hit_rate_array[int(math.ceil(stats[2]))]

threshold_70 = 0.7 * hit_rate_array[-3]
threshold_80 = 0.8 * hit_rate_array[-3]
threshold_90 = 0.9 * hit_rate_array[-3]
threshold_100 = 1 * hit_rate_array[-3]
min_cache_size_70 = 0
min_cache_size_80 = 0
min_cache_size_90 = 0
min_cache_size_100 = 0

hit_rate_file_name = "{}_{}.csv".format(file_name, "hit_rate")

with open(hit_rate_file_name, 'w+') as g:
	for i, hit_rate in enumerate(hit_rate_array):

		if min_cache_size_70 == 0 and hit_rate > threshold_70:
			stats_ord_dict["min_cache_size_70"] = i
			min_cache_size_70 = i
		if min_cache_size_80 == 0 and hit_rate > threshold_80:
			stats_ord_dict["min_cache_size_80"] = i
			min_cache_size_80 = i
		if min_cache_size_90 == 0 and hit_rate > threshold_90:
			stats_ord_dict["min_cache_size_90"] = i
			min_cache_size_90 = i
		if min_cache_size_100 == 0 and hit_rate > threshold_100:
			stats_ord_dict["min_cache_size_100"] = i
			min_cache_size_100 = i

		g.write(str(hit_rate))
		g.write("\n")



stats_ord_dict_json = json.dumps(stats_ord_dict, default=default)
reuse_output_fstats_file_name = "{}_{}.json".format(file_name, "reuse_stats")
with open(reuse_output_fstats_file_name, 'w+') as g:
	json.dump(stats_ord_dict_json, g)

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

hrc_file_name = "{}_{}.png".format(file_name, "HRC")
plt.title("HRC of file {}".format(file_name))
plt.plot(hit_rate_array[:-3])
plt.axvline(x=stats[2], color='k', linestyle='--')
plt.xlabel("Cache Size")
plt.ylabel("Hit Rate")
plt.savefig(hrc_file_name)

























