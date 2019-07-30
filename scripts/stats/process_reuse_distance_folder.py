import sys, os, json
import numpy as np
import pandas as pd
import math
from scipy.stats import describe
from collections import Counter
from scripts.scripts_lib import process_reuse_distance_file


def main(input_dir, output_dir, chunk_size):
    input_file_list = os.walk(input_dir).__next__()[2]

    for input_file_name in input_file_list:
        process_reuse_distance_file(input_file_name, input_dir, output_dir, chunk_size)


if __name__ == "__main__":
    input_folder_dir = sys.argv[1]
    output_folder_dir = sys.argv[2]
    chunk_size = int(sys.argv[3])
    main(input_folder_dir, output_folder_dir, chunk_size)
