from tsfresh.feature_extraction import extract_features, EfficientFCParameters, ComprehensiveFCParameters
import sys
import pdb
import numpy as np
from tsfresh.utilities.dataframe_functions import impute
from tsfresh import extract_relevant_features
from tsfresh import select_features


import pandas as pd


def main():

    ts_file_loc = sys.argv[1]
    #y_loc = sys.argv[2]

    ts = pd.read_csv(ts_file_loc, names=["ts"], dtype={"ts": int})
    #y = pd.read_csv(y_loc)
    # print(ts.dtypes)
    #
    #
    ts.insert(0, "time", range(0, len(ts)))
    ts.insert(1, "id", [1]*len(ts))

    # print(ts.dtypes)
    #
    print(ts.head())

    pdb.set_trace()
    # ts = []
    # with open(ts_file_loc) as f:
    #     line = f.readline()
    #
    #     while line:
    #         ts.append(int(line))
    #         line = f.readline()
    #
    # #
    # # t = pandas.read_csv(y)
    #
    # ts = np.array(ts)

    limit = len(ts)

    print(len(ts))

    pdb.set_trace()
    #
    # ts = pd.DataFrame({
    #     "ts": ts[:limit],
    #     "id": np.ones(limit),
    #     "time": np.arange(limit)
    # });

    extracted_features = extract_features(ts, column_id="id", column_sort="time", column_value="ts", n_jobs=8, show_warnings=False,
                                                          default_fc_parameters=EfficientFCParameters())

    # print(extracted_features)
    #
    # impute(extracted_features)

    extracted_features.to_csv("ext_features.csv")

    # features_filtered = select_features(extracted_features, y)
    #
    # features_filtered.to_csv("ext_features_filtered.csv")



    # from tsfresh import select_features
    # from tsfresh.utilities.dataframe_functions import impute
    #
    # impute(extracted_features)
    # features_filtered = select_features(extracted_features, y)
    #
    # print(features_filtered)

if __name__ == "__main__":
    main()

