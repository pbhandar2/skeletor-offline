import pandas as pd
import numpy as np


df = pd.read_csv("summary.csv")
df = df.drop(df.columns[0], axis=1)
df = df.drop(df.columns[1], axis=1)
df = df.drop(df.columns[2], axis=1)
df = df.drop(df.columns[4], axis=1)
df = df.drop(df.columns[5], axis=1)
df = df.drop(df.columns[6], axis=1)

import matplotlib.pyplot as plt

labels = ["var", "size"]

print(df.columns)

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