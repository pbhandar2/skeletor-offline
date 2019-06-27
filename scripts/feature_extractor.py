from tsfresh.feature_extraction import extract_features, EfficientFCParameters
import sys

file_loc = sys.argv[1]

f = open(file_loc)
line = f.readline()

while line:
    r = int(line)
    line = f.readline()