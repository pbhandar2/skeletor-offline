from sklearn.linear_model import LogisticRegression

import numpy as np

from sklearn.model_selection import train_test_split

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

    size_flag = 0
    if size < 0:
        size_flag = 1

    data.append([mean, variance, skew, kurtosis, unique_object_ratio, size_flag])

    line = f.readline()

print(data)

np.random.shuffle(data)

data = np.array(data).reshape(-1, len(data[0]))

trainx, testx, trainy, testy = train_test_split(data[:, :-1], data[:, -1], test_size=0.1, random_state=42)

regr_1 = LogisticRegression()
regr_1.fit(trainx, trainy)

pred = regr_1.predict(testx)

total_error = 0
for real, p in zip(testy, pred):
    print("Real: {}, Predicted: {}".format(real, p))


print(trainy)
