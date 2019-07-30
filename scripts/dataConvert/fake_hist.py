import numpy as np
import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt



values = [100000, 50000, 44000, 72000, 5000, 3435, 2512, 2512, 5124, 10000, 15000, 4000, 2141, 1245, 12552, 242, 1252, 1202, 1245
                , 2522, 1822, 1092, 1202, 1112, 1124, 1125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 922, 1092, 1202, 1112, 1214, 125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 400, 2141, 1245, 2552, 242, 1252, 1202, 1245
                , 1522, 1822, 1092, 1202, 1112, 1124, 1125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 922, 1092, 1202, 1112, 1214, 125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 400, 2141, 1245, 1552, 242, 1252, 1202, 1245
                , 1522, 1822, 1092, 1202, 1112, 1124, 1125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 922, 1092, 1202, 1112, 1214, 125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 400, 2141, 1245, 1552, 242, 1252, 1202, 1245
                , 1522, 1822, 1092, 1202, 1112, 1124, 1125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 922, 1092, 1202, 1112, 1214, 125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 400, 2141, 1245, 1552, 242, 1252, 1202, 1245
                , 1522, 1822, 1092, 1202, 1112, 1124, 1125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 922, 1092, 1202, 1112, 1214, 125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 400, 2141, 1245, 1552, 242, 1252, 1202, 1245
                , 1522, 1822, 1092, 1202, 1112, 1124, 1125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 922, 1092, 1202, 1112, 1214, 125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 400, 2141, 1245, 1552, 242, 1252, 1202, 1245
                , 1522, 1822, 1092, 1202, 1112, 1124, 1125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 922, 1092, 1202, 1112, 1214, 125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 400, 2141, 1245, 1552, 242, 1252, 1202, 1245
                , 1522, 1822, 1092, 1202, 1112, 1124, 1125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 922, 1092, 1202, 1112, 1214, 125, 125, 1252, 111, 114, 1022, 1542, 1524
                , 400, 2141, 1245, 1552, 242, 1252, 1202, 1245]

indexes = np.arange(len(values))
plt.bar(indexes, values, width=1)
plt.axvline(x=4, color='g', label="L1 size")
plt.axvline(x=80, color='r', label="L1 + L2 size")
plt.xlabel("Reuse Distance")
plt.ylabel("Count")
# plt.axvline(x=181, color='g', linestyle='--')
# plt.axvline(x=1080, color='r')
# plt.axvline(x=1080-480, color='r', linestyle='--')
plt.legend()
plt.savefig("fake_reuse.png")
plt.close()

value_count=[]
cur_val = 0
for val in values:
    cur_val += val
    value_count.append(cur_val)

plt.plot(value_count)
plt.axvline(x=4, color='g', label="L1 size")
plt.axvline(x=80, color='r', label="L1 + L2 size")
plt.xlabel("Reuse Distance")
plt.ylabel("Cumulative Count")
plt.legend()
plt.savefig("fake_reuse_cum.png")
plt.close()

for i in range(5):
    temp = values[i]
    values[i] = values[80-i]
    values[80-i] = temp

plt.bar(indexes, values, width=1)
plt.axvline(x=76, color='r', label="L1 size")
plt.axvline(x=80, color='g', label="L1 + L2 size")
plt.xlabel("Reuse Distance")
plt.ylabel("Count")
# plt.axvline(x=181, color='g', linestyle='--')
# plt.axvline(x=1080, color='r')
# plt.axvline(x=1080-480, color='r', linestyle='--')
plt.legend()
plt.savefig("fake_reuse_rev.png")
plt.close()

value_count=[]
cur_val = 0
for val in values:
    cur_val += val
    value_count.append(cur_val)

plt.plot(value_count)
plt.axvline(x=76, color='r', label="L1 size")
plt.axvline(x=80, color='g', label="L1 + L2 size")
plt.xlabel("Reuse Distance")
plt.ylabel("Cumulative Count")
plt.legend()
plt.savefig("fake_reuse_cum_rev.png")
plt.close()