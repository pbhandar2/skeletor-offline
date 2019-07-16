from tsfresh.feature_extraction import extract_features, EfficientFCParameters, ComprehensiveFCParameters
import sys
import pandas as pd


def main():

    ts_file_loc = sys.argv[1]
    ts = pd.read_csv(ts_file_loc, names=["ts"], dtype={"ts": int})
    ts.insert(0, "time", range(0, len(ts)))
    ts.insert(1, "id", [1]*len(ts))

    extracted_features = extract_features(ts, column_id="id", column_sort="time", column_value="ts", n_jobs=8, show_warnings=False,
                                                          default_fc_parameters=EfficientFCParameters())

    extracted_features.to_csv(sys.argv[2])

if __name__ == "__main__":
    main()

