import sys, os

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

            cur_output_folder = os.path.join(output_folder_name, "data")
            run_command = "python3 process_msr_page.py {} {}".format(file_location, cur_output_folder)
            os.system(run_command)

            print("DONE PROCESSING {}".format(file_location))

            output_file = os.path.join(cur_output_folder, "{}_4096.csv".format(file_name))

            run_command = "python3 get_hit_rate.py {} 0".format(output_file)
            os.system(run_command)

            run_command = "mv {}/*HRC.png {}".format(cur_output_folder, os.path.join(output_folder, "HRC"))
            os.system(run_command)
            run_command = "mv {}/*reuse_stats.json {}".format(cur_output_folder,
                                                              os.path.join(output_folder, "reuse_stats"))
            os.system(run_command)
            run_command = "mv {}/*hit_rate.csv {}".format(cur_output_folder,
                                                          os.path.join(output_folder, "csv_hit_rate"))
            os.system(run_command)
            run_command = "mv {}/*_reuse.csv {}".format(cur_output_folder, os.path.join(output_folder, "csv_reuse"))
            os.system(run_command)




        except Exception as inst:

            print(type(inst))
            print(inst.args)
            print(inst)
            print("error processing file {}".format(file_location))
