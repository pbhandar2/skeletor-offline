# import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt

f = open("summary.csv")

line = f.readline()

data = []
x = []
y = []

while line:
    line_split = line.split(",")
    mean = float(line_split[2])
    variance = float(line_split[3])
    skew = float(line_split[4])
    kurtosis = float(line_split[5])
    size = float(line_split[7])

    size_flag = 0
    if size < 0:
        size_flag = 1

    x.append(variance)
    y.append(size)

    line = f.readline()

plt.scatter(x, y)
plt.show()

