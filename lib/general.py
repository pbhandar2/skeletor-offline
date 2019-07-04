import json
from const import *
import logging
from traceReader.clock import Clock


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
