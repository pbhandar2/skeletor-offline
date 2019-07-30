import sys
import matplotlib.pyplot as plt
from collections import Counter


def main(file_name):
    obj_list = []
    with open(file_name) as f:
        line = f.readline()

        while len(line):
            obj_list.append(int(line))
            line = f.readline()

    return obj_list


def plot_obj_list(obj_list):
    counter = Counter(obj_list)
    limit = 1000
    pages, final_list = zip(*counter.most_common(limit))
    print(final_list)

    output_dir = sys.argv[2]
    plt.plot(range(limit), final_list)
    plt.xlabel("Pages")
    plt.ylabel("Number of Accesses")
    plt.savefig(output_dir)
    plt.close()


if __name__ == "__main__":

    if len(sys.argv) < 3:
        sys.exit("Not enough arguments")

    file_name = sys.argv[1]
    plot_obj_list(main(file_name))