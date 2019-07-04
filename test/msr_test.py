from skeletor import Skeletor
import sys
import pdb

sys.path.append('../')


def main(file_loc):
    processor = Skeletor()
    processor.open_file(file_loc, "../trace_config.json", "MSR")
    profiler = processor.get_metric_extractor()
    profiler.extract_metric()
    pdb.set_trace()


if __name__ == "__main__":
    file_loc = sys.argv[1]
    main(file_loc)

