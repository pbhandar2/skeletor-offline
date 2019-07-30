import sys
import pandas as pd
import matplotlib.pyplot as plt

def main(file_loc):
    df = pd.read_csv(file_loc, names=["file_name", "real", "pred", "rel_error"])
    df.sort_values(by=["real"])
    print(df)
    df.plot(x="real", y="rel_error", style="o")
    plt.show()


if __name__ == "__main__":
    file_loc = sys.argv[1]
    main(file_loc)