from skeletor import Skeletor
import sys
import pdb


def main(file_loc):
    processor = Skeletor()
    processor.open_file(file_loc, "../trace_config.json", "MSR-Cambridge")
    profiler = processor.get_metric_extractor()
    profiler.extract_metric()

    pdb.set_trace()


if __name__ == "__main__":
    sys.path.append('../')
    file_loc = sys.argv[1]
    main(file_loc)

