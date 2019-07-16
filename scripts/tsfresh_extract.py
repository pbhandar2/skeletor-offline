from tsfresh.feature_extraction import extract_features, EfficientFCParameters, ComprehensiveFCParameters
import sys
import pandas as pd


def main():

    ts_file_loc = sys.argv[1]
    ts = pd.read_csv(ts_file_loc, names=["ts"], dtype={"ts": int})
    extracted_features = extract_features(ts, column_id="id", column_sort="time", column_value="ts", n_jobs=8, show_warnings=False,
                                                          default_fc_parameters=ComprehensiveFCParameters())
    extracted_features.to_csv("ext_features.csv")

if __name__ == "__main__":
    main()

