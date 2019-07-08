from skeletor import Skeletor
import os, sys


def generate_reuse_data(file_loc, type, output_dir):
    processor = Skeletor()
    processor.open_file(file_loc, "../trace_config.json", type)
    profiler = processor.get_metric_extractor()
    profiler.extract_metric()
    profiler.plot_reuse_dist_top_k_pages(15, output_dir)
    return profiler.metrics["entropy"]


if __name__ == "__main__":

    file_list = os.walk(sys.argv[1]).__next__()[2]
    entropy_array = []
    f = open("entropy_{}.csv".format(sys.argv[2]), "w+")

    for file_name in file_list:
        if ".gz" in file_name:
            print("Working on {}".format(file_name))
            try:
                entropy = generate_reuse_data(os.path.join(sys.argv[1], file_name), sys.argv[2], sys.argv[3])
                f.write("{},{}\n".format(file_name, entropy))
            except Exception as inst:
                print(type(inst))
                print(inst.args)
                print(inst)
                print("error processing file {}".format(file_name))
            print("Done working on {}".format(file_name))

    f.close()





