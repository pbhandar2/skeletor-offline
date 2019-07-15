import numpy as np
from sklearn.linear_model import LinearRegression

f = open("summary.csv")

line = f.readline()
x = []
y = []

while line:
	split_line = line.split(",")
	x.append([float(split_line[3]), float(split_line[4]), float(split_line[5])])
	y.append(abs(float(split_line[-2])))
	line = f.readline()

x = np.array(x).reshape(-1,3)
y = np.array(y).reshape(-1,1)

reg = LinearRegression().fit(x[:-1], y[:-1])

pred = reg.predict([x[-1]])

from sklearn.tree import DecisionTreeRegressor

regr_1 = DecisionTreeRegressor(max_depth=5)
regr_1.fit(x[:-1], y[:-1])
y_1 = regr_1.predict([x[-1]])

print(y_1)
print(pred)
print(y[-1])



