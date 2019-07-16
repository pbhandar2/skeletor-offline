from tsfresh.feature_extraction import extract_features, EfficientFCParameters, ComprehensiveFCParameters
import sys
import pandas as pd
import numpy as np


def main():

    ts_file_loc = sys.argv[1]
    df = pd.read_csv(ts_file_loc, dtype={"ts": int, "id": int, "time": int})
    # df.insert(0, "time", pd.Series(range(0, len(df)), dtype='int32'))
    # df.insert(1, "id", pd.Series([1]*len(df), dtype='int32'))

    print(df.head())

    limit = int(sys.argv[3])

    if limit == -1:
        limit = len(df)

    # limit = 2
    # id_array = np.ones(limit)
    # ts_array = np.random.rand(1, limit)
    # print(df)
    #
    # ts = pd.DataFrame({
    #     "ts": np.reshape(df.values[:limit], (-1, limit))[0],
    #     "id": np.reshape(id_array, (-1, limit))[0],
    #     "time": range(limit)
    # });



    extracted_features = extract_features(df[:limit], column_id="id", column_sort="time", column_value="ts", n_jobs=8, show_warnings=False,
                                                          default_fc_parameters=EfficientFCParameters())

    extracted_features.to_csv(sys.argv[2])


if __name__ == "__main__":
    main()

