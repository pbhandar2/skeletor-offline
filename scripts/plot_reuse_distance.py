

import sys, os, json, numpy, math

#sys.path.append("../../PyMimircache")

from PyMimircache import Cachecow
from scipy.stats import describe 

def default(o):
	return int(o)

file_name = "web_1.csv.gz_4096.csv"

if len(sys.argv) > 1:
	file_name = sys.argv[1]

c = Cachecow();

params = {
	"init_params": {
		"label": 1,
		"fmt": "{}\n"
	}
}

r = c.open(file_name,"c","c", **params)

profiler = c.profiler(algorithm="LRU")

reuse_dist_array = profiler.get_reuse_distance()


figname = "{}_{}.png".format(file_name, "reuse_distance")

import matplotlib
matplotlib.use('Agg')

from collections import Counter

limit = 1000
import numpy as np
width = 1

import matplotlib.pyplot as plt
plt.figure(figsize=(100,30))

'''
	labels2, values2 = zip(*self.reuse_distance_counter.most_common(limit))
	Cannot do the concise version above because we need to add 0 values to different 
	reuse distance that do not appear in between so need to iterate over the whole 
	thing and fill up the reuse distances in between. Eg: if we do the above style 
	and we have reuse distance at 200, nothing at 201 and then at 202 we will not 
	be able to insert reuse distance count at 201 to be zero 
'''

reuse_distance_counter = Counter(reuse_dist_array)

labels = []
values = []
for i in range(limit):
	labels.append(i)
	values.append(reuse_distance_counter[i])
indexes = np.arange(len(labels))

plt.subplot(211)
plt.bar(indexes, values, width)
plt.yticks(fontsize=50)
plt.xticks(fontsize=50)
plt.title("Reuse Distance Distribution upto {} for file {} with blocksize {}"
		.format(limit,file_name, 4096), 
		fontsize=80)
plt.ylabel("Count", fontsize=80)
plt.xlabel("Reuse Distance", fontsize=80)


plt.subplot(212)
plt.bar(indexes, values, width)
plt.yticks(fontsize=50)
plt.xticks(fontsize=50)
plt.yscale("log")
plt.title("Log of Reuse Distance Distribution upto {} for file {} with blocksize {}"
	.format(limit, file_name, 4096), fontsize=80)
plt.ylabel("log(Count)", fontsize=80)
plt.xlabel("Reuse Distance", fontsize=80)

plt.subplots_adjust(hspace=1)

plt.savefig(figname)
plt.close()
























