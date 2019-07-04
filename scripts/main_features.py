from tsfresh.feature_extraction.feature_calculators import number_cwt_peaks
import pandas as pd
import sys


def main(file_loc):
    df = pd.read_csv(file_loc)
    ts = df.as_matrix()
    peaks = number_cwt_peaks(ts, 2)
    print(peaks)

if __name__ == "__main__":
    file_loc = sys.argv[1]
    main(file_loc)