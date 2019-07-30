
from scripts.dataConvert.data_convert_lib import read_reuse_distance, plot_reuse_hist, plot_reuse_cum_hist
import sys

reuse_distance = read_reuse_distance("../../data/msr/block_512/reuse.csv")
plot_reuse_hist(reuse_distance, limit=5000)
values = plot_reuse_cum_hist(reuse_distance, limit=5000)

c = 100
c1 = 0
c2 = 100

lat_1 = 0.1
lat_2 = 120
lat_3 = 100000

lat_array = []
max = 1200
lat_array.append(lat_2*values[max-1]+ lat_3*(values[-1] - values[max]))
config_array = [(0,1200)]

for i in range(1, 201):
    j = 1200 - i*6

    total_lat = lat_1*values[i-1] + lat_2*(values[j-1] - values[i]) + lat_3*(values[-1] - values[j])
    lat_array.append(total_lat)
    config_array.append((i, j))

lat_array.append(lat_1*values[int(max/6)-1]+ lat_3*(values[-1] - values[int(max/6)]))

print(lat_array)

# import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt


plt.figure()
plt.plot(lat_array)
plt.savefig("test_latency.png")

print(min(lat_array))

min_index = lat_array.index(min(lat_array))
print(min_index)
print(config_array[min_index])