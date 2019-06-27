f = open("error.dat")

line = f.readline()
line_num = 0
error_array = []
cur_array = []
while line:
    cur_array.append(float(line))
    if line_num % 7 == 6:
        error_array.append(cur_array)
        cur_array = []
    line_num += 1
    line = f.readline()

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

avg_error = []
for i, error_arr in enumerate(error_array):
    avg_error.append(np.mean(error_arr))


print(avg_error)
plt.plot(avg_error)

plt.title("Average error over iteration")
plt.xlabel("Iterations")
plt.ylabel("Error in MB")
plt.savefig("test.png")

print("DONE")