import numpy as np

# create zipf distribution
_alpha = 2.5
dist = np.random.zipf(_alpha, size=int(1e4))

with open("_temp.csv", "w+") as f:
    f.write("\n".join(dist))

import skeletor

