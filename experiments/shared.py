import os
from collections import Counter
from scipy.stats import describe


def get_file_list(data_dir, file_name_filter=None):
    file_list = os.walk(data_dir).__next__()[2]
    for file_name in file_list:
        if filter is not None:
            yield os.path.join(data_dir, file_name)
        else:
            assert type(file_name_filter) == function
            if filter(file_name):
                yield os.path.join(data_dir, file_name)


def get_reuse_distance_features(reuse_distance_array, plot_flag=False, plot_count=100000):
    rd_stats = dict(describe(reuse_distance_array)._asdict())
    rd_counter = Counter(reuse_distance_array)
    rd_stats["num_unique"] = rd_counter[-1]
    hit_rate_array = get_hit_rate(reuse_distance_array, rd_stats)
    return rd_stats, hit_rate_array


def get_hit_rate(rd_counter, rd_stats):
    cur_hit_count = 0
    hit_rate_array = []
    for i in range(rd_stats['minmax'][1]):
        cur_hit_count += rd_counter[i]
        hit_rate_array.append(cur_hit_count/rd_stats['nobs'])

    return hit_rate_array




