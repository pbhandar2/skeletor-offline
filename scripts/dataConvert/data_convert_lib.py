import gzip, math
from collections import Counter
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd


def convert_msr_to_blocks(file_location, output_file_name, page_size):

    with gzip.open(file_location) as f:
        with open(output_file_name, 'w+') as g:
            line = f.readline().decode("utf-8")

            while len(line) > 0:

                line_split = line.split(",")

                label = int(line_split[4])
                size = int(line_split[5])

                page_start = int(label)
                page_end = int(math.floor(label + size))

                while page_start <= page_end:
                    string_write = "{}\n".format(page_start)
                    g.write(string_write)
                    page_start += page_size

                line = f.readline().decode("utf-8")


def get_reuse_distance_pymimir(file_location, output=None):
    from PyMimircache import Cachecow
    c = Cachecow()

    params = {
        "init_params": {
            "label": 1,
            "fmt": "{}\n"
        }
    }

    r = c.open(file_location, "c", "c", **params)
    profiler = c.profiler(algorithm="LRU")
    reuse_dist_array = profiler.get_reuse_distance()

    if output is not None:
        f = open(output, 'w+')

        for r in reuse_dist_array:
            f.write("{}\n".format(r))

        f.close()

    return reuse_dist_array

def read_reuse_distance(file_location):
    df = pd.read_csv(file_location, header=None)
    arr = df.values.reshape(-1, len(df))[0]
    return arr


def plot_reuse_hist(reuse_distance_array, limit=-1, width=1, figname="plot_reuse_hist.png"):
    reuse_distance_counter = Counter(reuse_distance_array)
    max_reuse_dist = max(reuse_distance_array)
    if limit == -1:
        limit = max_reuse_dist
    else:
        if limit > max_reuse_dist:
            limit = max_reuse_dist

    labels=[]
    values=[]
    for i in range(limit):
        labels.append(i)
        values.append(reuse_distance_counter[i])

    indexes = np.arange(len(labels))
    plt.bar(indexes, values, width=3)
    # print(max(values))
    # import pdb
    # pdb.set_trace()
    # plt.axvline(x=100, color='g')
    # plt.axvline(x=181, color='g', linestyle='--')
    # plt.axvline(x=1080, color='r')
    # plt.axvline(x=1080-480, color='r', linestyle='--')
    plt.ylabel("Count")
    plt.xlabel("Reuse Distance")
    plt.tight_layout()
    plt.savefig(figname)
    plt.close()

def plot_reuse_cum_hist(reuse_distance_array, limit=-1, width=1, figname="plot_reuse_cum_hist.png"):
    reuse_distance_counter = Counter(reuse_distance_array)

    if limit == -1:
        limit = max(reuse_distance_array)

    labels=[]
    values=[]
    cur_value = 0
    for i in range(limit):
        labels.append(i)
        cur_value = cur_value + reuse_distance_counter[i]
        values.append(cur_value)

    indexes = np.arange(len(labels))
    plt.plot(values)
    #print(max(values))
    # import pdb
    # pdb.set_trace()
    # plt.axvline(x=100, color='g')
    # plt.axvline(x=181, color='g', linestyle='--')
    # plt.axvline(x=1080, color='r')
    # plt.axvline(x=1080-480, color='r', linestyle='--')
    plt.ylabel("Cumulative Count")
    plt.xlabel("Reuse Distance")
    plt.tight_layout()
    plt.savefig(figname)
    plt.close()


    return values



