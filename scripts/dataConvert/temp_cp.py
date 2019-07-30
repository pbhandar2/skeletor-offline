import os
from scripts.dataConvert.data_convert_lib import read_reuse_distance, plot_reuse_hist, plot_reuse_cum_hist


def get_config(values, file_name):
    c = 100
    c1 = 0
    c2 = 100

    lat_1 = 0.1
    lat_2 = 1000
    lat_3 = 60000

    lat_array = []
    max = 32000
    cost_ratio = 16
    lat_array.append(lat_2 * values[max - 1] + lat_3 * (values[-1] - values[max]))
    config_array = [(0, max)]

    for i in range(1, int(max/cost_ratio)):
        j = max - i * cost_ratio

        total_lat = lat_1 * values[i - 1] + lat_2 * (values[j - 1] - values[i]) + lat_3 * (values[-1] - values[j])
        lat_array.append(total_lat)
        config_array.append((i, j))

    lat_array.append(lat_1 * values[int(max / cost_ratio) - 1] + lat_3 * (values[-1] - values[int(max / cost_ratio)]))


    # import matplotlib
    # matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    plt.figure()
    plt.plot(lat_array)
    plt.savefig("{}_latency.png".format(file_name))


    min_index = lat_array.index(min(lat_array))



    write_str = "{},{}\n".format(file_name, config_array[min_index][0])
    print(write_str)

    import pdb
    #pdb.set_trace()

def process_file(file_loc, file_name):
    reuse_distance = read_reuse_distance(file_loc)
    #plot_reuse_hist(reuse_distance, limit=100000, figname="{}_reuse_hist.png".format(file_name))
    # values = plot_reuse_cum_hist(reuse_distance, limit=100000, figname="{}_reuse_hist_cum.png".format(file_name))
    from collections import Counter
    reuse_distance_counter = Counter(reuse_distance)

    limit = max(reuse_distance)
    print(limit)
    labels=[]
    values=[]
    cur_value = 0
    for i in range(limit):
        labels.append(i)
        cur_value = cur_value + reuse_distance_counter[i]
        values.append(cur_value)

    get_config(values, file_name)

if __name__ == "__main__":
    #reuse_dir = "../../data/cachePhysics/reuse_distance"
    reuse_dir = "../../data/msr/block_512"
    filename_list = os.walk(reuse_dir).__next__()[2]

    for filename in filename_list:
        # if '08' in filename:
        #     file_dir = os.path.join(reuse_dir, filename)
        #     process_file(file_dir, filename)

        file_dir = os.path.join(reuse_dir, filename)
        process_file(file_dir, filename)
