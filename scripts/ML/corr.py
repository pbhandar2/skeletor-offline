import pandas as pd
import numpy as np


df = pd.read_csv("../summary_1M.csv")

print(df.columns)



df = df.drop([df.columns[0], df.columns[1], df.columns[7], df.columns[8], df.columns[9]], axis=1)
# df = df.drop(df.columns[1], axis=1)
# df = df.drop(df.columns[2], axis=1)
# df = df.drop(df.columns[4], axis=1)
# df = df.drop(df.columns[5], axis=1)
# df = df.drop(df.columns[6], axis=1)

# df = df.drop(, axis=1)
# df = df.drop(df.columns[8], axis=1)
# df = df.drop(df.columns[9], axis=1)

import matplotlib.pyplot as plt

labels = ["mean", "var", "skew", "kurt", "size"]



from sklearn.decomposition import PCA

pca = PCA(n_components=2)
pca.fit(df)

print(pca.explained_variance_ratio_) 
print(pca.components_)

plt.matshow(df.corr())
plt.xticks(np.arange(len(labels)), labels, fontsize=30)
plt.yticks(np.arange(len(labels)), labels, fontsize=30)
plt.colorbar()
plt.show()