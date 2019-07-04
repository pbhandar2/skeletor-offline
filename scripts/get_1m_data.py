import sys, os, json
import numpy as np
import pandas as pd
import math
from scipy.stats import describe
from collections import Counter


def default(o):
    return int(o)


def process_reuse_array(reuse_dist_array):
    filtered_reuse_dist_array = np.extract(reuse_dist_array != -1, reuse_dist_array)

    if len(filtered_reuse_dist_array) == 0:
        return

    num_unique_objects = len(reuse_dist_array) - len(filtered_reuse_dist_array)
    stats = describe(filtered_reuse_dist_array)

    total_obs = int(math.ceil(stats[0]))
    average_reuse = int(math.ceil(stats[2]))

    stats_ord_dict = stats._asdict()
    stats_ord_dict["num_unique_obj"] = num_unique_objects
    stats_ord_dict["unique_obj_ratio"] = num_unique_objects / len(reuse_dist_array)
    stats_ord_dict["opt"] = 1 - stats_ord_dict["unique_obj_ratio"]

    reuse_counter = Counter(filtered_reuse_dist_array )
    average_hit_rate = None
    size_70 = None
    size_80 = None
    size_90 = None

    total_count = 0

    for d, count in sorted(reuse_counter.items()):
        dist = int(d)
        total_count += count
        if not average_hit_rate and dist > average_reuse:
            average_hit_rate = total_count / total_obs
            stats_ord_dict["avg_hit_rate"] = average_hit_rate

        if not size_70 and total_count > 0.7 * total_obs:
            size_70 = True
            stats_ord_dict["min_cache_size_70"] = dist

        if not size_80 and total_count > 0.8 * total_obs:
            size_80 = True
            stats_ord_dict["min_cache_size_80"] = dist

        if not size_90 and total_count > 0.9 * total_obs:
            size_90 = True
            stats_ord_dict["min_cache_size_90"] = dist



    stats_ord_dict["min_cache_size_100"] = dist

    return stats_ord_dict


def process_input_file(input_file_name, input_dir, output_dir, chunk_size):
    full_input_file_path = os.path.join(input_dir, input_file_name)
    print("Processing file {}".format(full_input_file_path))
    df = pd.read_csv(full_input_file_path)
    num_chunks = math.ceil(len(df) / chunk_size)
    cur_chunk = 0

    for split_array in np.array_split(df, num_chunks):
        stats_dict = process_reuse_array(split_array)

        if stats_dict:
            print(stats_dict)
            output_file_name = "{}_{}.json".format(input_file_name, cur_chunk)
            full_output_file_path = os.path.join(output_dir, output_file_name)
            stats_ord_dict_json = json.dumps(stats_dict, default=default)
            with open(full_output_file_path, 'w+') as g:
                json.dump(stats_ord_dict_json, g)

        cur_chunk += 1


def main(input_dir, output_dir, chunk_size):
    input_file_list = os.walk(input_dir).__next__()[2]

    for input_file_name in input_file_list:
        process_input_file(input_file_name, input_dir, output_dir, chunk_size)


if __name__ == "__main__":
    input_folder_dir = sys.argv[1]
    output_folder_dir = sys.argv[2]
    chunk_size = int(sys.argv[3])
    main(input_folder_dir, output_folder_dir, chunk_size)
