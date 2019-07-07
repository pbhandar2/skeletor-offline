from skeletor import Skeletor
import os, sys


def generate_reuse_data(file_loc, type):
    processor = Skeletor()
    processor.open_file(file_loc, "../trace_config.json", type)
    profiler = processor.get_metric_extractor()
    profiler.extract_metric()


if __name__ == "__main__":

    file_list = os.walk(sys.argv[1]).__next__()[2]

    for file_name in file_list:
        generate_reuse_data(os.path.join(sys.argv[1], file_name), sys.argv[2])
