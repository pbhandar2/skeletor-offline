import pandas as pd
import numpy as np
import math

df = pd.read_csv("summary.csv")

data1 = df.iloc[:, 3:4]

data2 = df.iloc[:, 7:8].apply(lambda x: abs(x))


from scipy.stats import pearsonr

corr, _ = pearsonr(data1, data2)
print('Pearsons correlation: %.3f' % corr)