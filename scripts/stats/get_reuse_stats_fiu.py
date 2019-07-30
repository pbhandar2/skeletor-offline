import sys, os
from skeletor import Skeletor
sys.path.append('../')

raw_data_folder_location = sys.argv[1]
output_folder_name = sys.argv[2]

if not os.path.isdir(output_folder_name):
    os.mkdir(output_folder_name)

sub_out_folders = ["data", "csv_hit_rate", "csv_reuse", "HRC", "reuse_stats", "reuse_dist_plots"]

for sub_out_folder_name in sub_out_folders:
    if not os.path.isdir(os.path.join(output_folder_name, sub_out_folder_name)):
        os.mkdir(os.path.join(output_folder_name, sub_out_folder_name))

file_list = os.walk(raw_data_folder_location).__next__()[2]

for file_name in file_list:
    if ".gz" in file_name:
        try:
            file_location = os.path.join(raw_data_folder_location, file_name)

            processor = Skeletor()
            processor.open_file(os.path.join(raw_data_folder_location, file_name), "../trace_config.json", "FIU")
            profiler = processor.get_metric_extractor()
            profiler.extract_metric()

        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
            print("error processing file {}".format(file_location))
