import json
from const import *
import logging
from traceReader.clock import Clock
import os
from collections import Counter
from scipy.stats import describe

def numpyint_to_int(o):
    return int(o)

def check_config(json_file_location, trace_type):
    try:
        json_file_handle = open(json_file_location, 'r')
    except IOError:
        print("Could not read file: {}. Make sure the config file exists.".format(json_file_location))
        exit()

    config_json_array = json.load(json_file_handle)
    assert type(config_json_array) == list
    trace_type_config = None

    for config_json in config_json_array:
        if config_json["name"] == trace_type:
            trace_type_config = config_json
            break

    if trace_type_config is None:
        raise Exception(
            "The type {} was not found in the json file at {}. "
            "Please check to make sure that the name provided matches the name "
            "field in one of the json entries in the file.".format(
                trace_type, json_file_location))

    if "block_size" not in trace_type_config:
        trace_type_config["block_size"] = DEF_BLOCK_SIZE
        logging.warning("Block Size not included in the config file using the default block size of 512")

    if "page_size" not in trace_type_config:
        trace_type_config["page_size"] = DEF_BLOCK_SIZE
        logging.warning("Block Size not included in the config file using the default page size of 512")

    if "clock_config" in trace_type_config:
        trace_type_config["clock"] = Clock(
            trace_type_config["clock_config"]["type"],
            unit=trace_type_config["clock_config"]["unit"]
        )
    else:
        clock_type = "timestamp"
        clock_unit = "ns"
        trace_type_config["clock"] = Clock(clock_type, unit=clock_unit)
        logging.warning("""Clock not included in config. Using default clock type
            which treats time as timestamps with the unit as nanoseconds""")

    return trace_type_config


def get_file_list(data_dir, file_name_filter=None):
    file_list = os.walk(data_dir).__next__()[2]
    for file_name in file_list:
        if filter is not None:
            yield os.path.join(data_dir, file_name)
        else:
            assert type(file_name_filter) == function
            if filter(file_name):
                yield os.path.join(data_dir, file_name)


def filter_reuse_distance(reuse_distance_array):
    filtered_reuse_distance_array = []
    unique_object_count = 0
    for rd in reuse_distance_array:
        if rd != -1:
            filtered_reuse_distance_array.append(rd)
        else:
            unique_object_count += 1
    return filtered_reuse_distance_array, unique_object_count


def get_reuse_distance_features(raw_reuse_distance_array, plot_flag=False, plot_count=100000):
    reuse_distance_array, unique_object_count = filter_reuse_distance(raw_reuse_distance_array)
    rd_stats = dict(describe(reuse_distance_array)._asdict())
    rd_counter = Counter(reuse_distance_array)
    rd_stats["num_unique"] = unique_object_count
    rd_stats["opt"] = unique_object_count/(unique_object_count+rd_stats["nobs"])
    rd_stats["minmax"] = [rd_stats["minmax"][0], rd_stats["minmax"][1]]
    hit_rate_array = get_hit_rate(rd_counter, rd_stats)
    return rd_stats, hit_rate_array


def get_hit_rate(rd_counter, rd_stats):
    cur_hit_count = 0
    hit_rate_array = []
    for i in range(rd_stats['minmax'][1]):
        cur_hit_count += rd_counter[i]
        hit_rate_array.append(cur_hit_count/rd_stats['nobs'])

    return hit_rate_array