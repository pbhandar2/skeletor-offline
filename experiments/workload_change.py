
import sys
import json
from skeletor import Skeletor
sys.path.append(".")
import os

import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

def default(o):
    return int(o)


def main(data_dir, data_type, file_name_filer=None):
    print("Called main")
    file_list = os.walk(data_dir).__next__()[2]
    for file_name in file_list:
        if file_name_filer(file_name):
            file_name = file_name.split("/")[-1].replace("\\", "")
            print("Processing {}".format(file_name))
            processor = Skeletor()
            processor.open_file(os.path.join(data_dir, file_name), "../trace_config.json", data_type)
            processor.workload_change()
        # profiler = processor.get_metric_extractor(window_size=86400)
        # profiler.extract_metric()
        # reuse_distance_array = profiler.reuse_distance_array
        #
        # plt.figure()
        # plt.title("Hit Rate Curve for each day of FIU trace \n : {}".format(file_name))
        # plt.xlabel("Cache Size")
        # plt.ylabel("Hit Rate")
        #
        # window_count = 0
        # for start, end in profiler.window_index:
        #     rd_stats, hit_rate_array = shared.get_reuse_distance_features(reuse_distance_array[start:end])
        #     hit_rate_list = [0.7, 0.8, 0.9]
        #     cur_hr = 0
        #     for i, hr in enumerate(hit_rate_array):
        #         if hr > hit_rate_list[cur_hr]:
        #             rd_stats["hr_{}".format(hit_rate_list[cur_hr])] = i
        #             cur_hr += 1
        #             if cur_hr == len(hit_rate_list):
        #                 break
        #
        #     data_name = "{}_{}".format(file_name, window_count)
        #     rd_stats["name"] = data_name
        #     plt.plot(hit_rate_array, label="{}".format(window_count))
        #     window_count += 1
        #     print(rd_stats)
        #     with open("{}_{}.json".format(file_name, window_count), 'w+') as outfile:
        #         json.dump(rd_stats, outfile)
        #
        # plt.legend()
        # plt.savefig("{}_{}.png".format(file_name, window_count))
        # plt.close()


if __name__ == "__main__":

    if len(sys.argv) == 3:
        type = sys.argv[2]
    else:
        type = "FIU"

    main(sys.argv[1], type, file_name_filer=lambda k: k if ".gz" in k else False)