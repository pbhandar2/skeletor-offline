import sys, os, json
from collections import defaultdict
from ast import literal_eval
import matplotlib.pyplot as plt


def process_file_set(input_dir, file_set, key, code):
    sorted(file_set, key=lambda k: int(k.split(".json")[0].split("_")[-1]))
    cache_list = []
    for file_name in file_set:
        try:
            with open(os.path.join(input_dir, file_name)) as json_file:
                data = literal_eval(json.load(json_file))
                cache_size = data["min_cache_size_70"]
                cache_list.append(cache_size)
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print("error processing file {}".format(file_name))

    print(file_set[0])
    print(cache_list)
    plt.plot(cache_list)
    plt.title("window: {} for file {} with {} windows".format(code, key, len(file_set)))
    plt.ylabel("cache size for 70")
    plt.xlabel("windows")
    plt.savefig(os.path.join("../data/window_plot", "{}_{}.png".format(key, code)))
    plt.close()

def main(input_dir, code, pre):
    file_list = os.walk(input_dir).__next__()[2]

    file_types = defaultdict(list)

    for file_name in file_list:
        key = file_name.split(".csv")[0]
        file_types[key].append(file_name)

    for key in file_types:
        process_file_set(input_dir, file_types[key], key, code)


if __name__=="__main__":
    input_dir = sys.argv[1]
    code = sys.argv[2]
    pre = sys.argv[3]
    main(input_dir, code, pre)