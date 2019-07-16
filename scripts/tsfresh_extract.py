from tsfresh.feature_extraction import extract_features, EfficientFCParameters, ComprehensiveFCParameters
import sys
import pandas as pd
import numpy as np


def main():

    ts_file_loc = sys.argv[1]
    df = pd.read_csv(ts_file_loc, names=["ts"], dtype={"ts": int})

    limit=len(df)
    ts = pd.DataFrame({
        "ts": df[:limit],
        "id": np.ones(limit),
        "time": np.arange(limit)
    });

    extracted_features = extract_features(ts, column_id="id", column_sort="time", column_value="ts", n_jobs=8, show_warnings=False,
                                                          default_fc_parameters=EfficientFCParameters())

    extracted_features.to_csv(sys.argv[2])


if __name__ == "__main__":
    main()

