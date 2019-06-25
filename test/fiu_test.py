import sys, os, matplotlib, time, pdb
from skeletor import Skeletor

matplotlib.use("agg")
import matplotlib.pyplot as plt

sys.path.append('../')


def my_func():

    if len(sys.argv) > 1:
        file_location = sys.argv[1]
    else:
        file_location = os.path.join("../data/mail-02.tar.gz")

    processor = Skeletor()
    processor.open_file(file_location, "../trace_config.json", "FIU")
    profiler = processor.get_metric_extractor()
    profiler.extract_metric()

    pdb.set_trace()


if __name__ == '__main__':
    start = time.time()
    my_func()
    end = time.time()
    print("Time taken by the script: {}".format(end - start))
