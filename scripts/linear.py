import numpy as np
from sklearn.linear_model import LinearRegression
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

    data.append([mean, variance, skew, kurtosis, unique_object_ratio, size])

    line = f.readline()

#print(data)

np.random.shuffle(data)

data = np.array(data).reshape(-1, len(data[0]))

trainx, testx, trainy, testy = train_test_split(data[:, :-1], data[:, -1], test_size=0.1, random_state=42)

regr_1 = LinearRegression()
regr_1.fit(trainx, trainy)

pred = regr_1.predict(testx)

total_error = 0
for real, p in zip(testy, pred):
    diff = abs(abs(p) - abs(real))
    print("Real: {}, Predicted: {}, Difference: {} = {}MB".format(real, p, diff, (diff*4/1024)))
    total_error += abs(p - real)

average_error = total_error/len(pred)
print("Error: {} = {}MB".format(average_error, average_error*4/1024))


