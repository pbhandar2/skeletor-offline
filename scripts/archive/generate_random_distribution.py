"""
    The script generates random block I/O workload using a zipf distribution. This distribution is
    often found in the popularity of blocks in a workload.
"""

import numpy as np
import random
import math
import sys
import os

output_location = sys.argv[1]

for a in np.arange(1.1, 4.0, step=0.05):

    # create zipf distribution
    s = np.random.zipf(float(a), size=int(1e5))

    # roll a die for sequentiality
    seq_chances = random.uniform(0.2,0.7)

    # roll a die for average length of sequentiality
    seq_length_mean = random.randint(1,5)
    seq_length_sd = random.uniform(1.0, 3.0)

    file_name = "synthetic_zipf_{}_{}_{}_{}".format(a, seq_chances, seq_length_mean, seq_length_sd)

    print("Generating file {}".format(file_name))

    with open(os.path.join(output_location,file_name), "w+") as f:
        for sample in s:
            seq_roll = random.uniform(0.0,1.0)
            f.write("{}\n".format(sample))
            if seq_roll <= seq_chances:
                size = math.ceil(np.random.normal(loc=seq_length_mean, scale=seq_length_sd))
                if size > 1:
                    for i in range(size):
                        sample = sample + i
                        f.write("{}\n".format(sample))

    print("Done! {}".format(file_name))