import sys
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == "__main__":
    file_location = sys.argv[1]
    df = pd.read_csv(file_location)
    df.plot(kind="line")
    plt.show()




