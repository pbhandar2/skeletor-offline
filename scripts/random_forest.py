from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split

import numpy as np


f = open("summary.csv")

line = f.readline()

data = []

while line:
    line_split = line.split(",")
    mean = float(line_split[2])
    variance = float(line_split[3])
    skew = float(line_split[4])
    kurtosis = float(line_split[5])
    size = abs(float(line_split[7]))
    unique_object_ratio = float(line_split[9])

    data.append([mean, variance, skew, kurtosis, unique_object_ratio, size])

    line = f.readline()

print(data)

np.random.shuffle(data)

data = np.array(data).reshape(-1, len(data[0]))

X, testx, y, testy = train_test_split(data[:, :-1], data[:, -1], test_size=0.1, random_state=42)

regr = RandomForestRegressor(max_depth=2, random_state=0,
                             n_estimators=100)
regr.fit(X, y)

pred = regr.predict(testx)

total_error = 0
for real, p in zip(testy, pred):
    print("Real: {}, Predicted: {}".format(real, p))
    total_error += p - real

print("Error: {}".format(total_error/len(pred)))


