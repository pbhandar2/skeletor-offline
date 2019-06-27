import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

f = open("summary.csv")

line = f.readline()

data = []

while line:
    line_split = line.split(",")

    #print(line_split)

    mean = float(line_split[2])
    variance = float(line_split[3])
    skew = float(line_split[4])
    kurtosis = float(line_split[5])
    size = abs(float(line_split[7]))
    unique_object_ratio = float(line_split[9])

    data.append([mean, variance, skew, kurtosis, unique_object_ratio, size])

    line = f.readline()


np.random.shuffle(data)

data = np.array(data).reshape(-1, len(data[0]))

trainx, testx, trainy, testy = train_test_split(data[:, :-1], data[:, -1], test_size=0.1, random_state=42)

regr_1 = DecisionTreeRegressor(max_depth=4)
regr_1.fit(trainx, trainy)

pred = regr_1.predict(testx)

total_error = 0
error_array = []
f = open("error.dat", "a+")
for real, p in zip(testy, pred):
    diff = abs(abs(p) - abs(real))
    diff_mb = diff*4/1024
    print("Real: {}, Predicted: {}, Difference: {} = {}MB".format(real, p, diff, diff_mb))
    total_error += diff
    error_array.append(diff_mb)
    f.write(str(diff_mb))
    f.write("\n")

average_error = total_error/len(pred)
print("Error: {} = {}MB".format(average_error, average_error*4/1024))

import matplotlib
#matplotlib.use('Agg')

import matplotlib.pyplot as plt
plt.plot(error_array)
plt.show()





