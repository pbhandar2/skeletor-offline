from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np
import math




ml_type="random_forest"
code="1M"
f = open("../summary_{}.csv".format(code))
line = f.readline()

raw_data = []

while line:
    line_split = line.split(",")

    name = line_split[0]
    mean = float(line_split[2])
    variance = float(line_split[3])
    skew = float(line_split[4])
    kurtosis = float(line_split[5])
    size = math.ceil(float(line_split[6]))
    unique_object_ratio = float(line_split[9])

    raw_data.append([name, unique_object_ratio, mean, variance, skew, kurtosis, size])

    line = f.readline()

#print(data)

np.random.shuffle(raw_data)

data = np.array(raw_data).reshape(-1, len(raw_data[0]))

from sklearn.preprocessing import normalize

#data = normalize(data)
#print(data[:, 1:-1])
trainx, testx, trainy, testy = train_test_split(data[:,:-1], data[:, -1], test_size=0.1, random_state=42)


regr_1 = RandomForestRegressor(
    max_depth=4,
    random_state=0,
    n_estimators=200)

regr_1.fit(trainx[:, 1:], trainy)

pred = regr_1.predict(testx[:,1:].astype('float'))

total_error = 0
err_arr = []
err_data = []
error_file_name = "{}_{}_error.csv".format(ml_type, code)
err_f = open(error_file_name, 'w+')


for file_name, real, p in zip(testx[:, 0], testy.astype('float'), pred.astype('float')):
    #print("{},{},{}".format(file_name, real, p))

    diff = abs(abs(p) - abs(real))
    rel_err = diff/abs(real)
    print("File: {} Real: {}, Predicted: {}, Difference: {} = {}MB, Error = {}".format(file_name, real, p, diff, (diff*4/1024), rel_err))
    total_error += rel_err
    err_arr.append(rel_err)
    err_f.write("{},{},{},{}\n".format(file_name, real, p, rel_err))

err_f.close()

average_error = total_error/len(pred)
print("Error: {} = {}MB".format(average_error, average_error*4/1024))






plt.subplot(211)
plt.plot(err_arr)
plt.yticks(fontsize=10)
plt.xticks(fontsize=10)
plt.title("{} Error for {} test cases with blocksize {} for {}"
		.format(ml_type, len(testy), 4096, code),
		fontsize=10)
plt.ylabel("Relative Error", fontsize=10)

plt.xlabel("Traces", fontsize=10)


plt.subplot(212)
plt.plot(err_arr)
plt.yticks(fontsize=10)
plt.xticks(fontsize=10)
plt.yscale("log")
plt.title("{} Log Error for {} test cases with blocksize {} for {}"
		.format(ml_type, len(testy), 4096, code),
		fontsize=10)
plt.ylabel("Log Relative Error", fontsize=10)
plt.xlabel("Traces", fontsize=10)

plt.subplots_adjust(hspace=1)
plt.tight_layout()

plt.savefig("./{}_{}.png".format(ml_type, code))



plt.show()
print("DONE")

plt.close()


