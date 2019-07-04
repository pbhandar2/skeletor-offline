import sys, os, pandas, json
from ast import literal_eval
import pdb

csv_directory = sys.argv[1]
stats_directory = sys.argv[2]
limit = int(sys.argv[3])
output_file_name = sys.argv[4]

csv_file_list = os.walk(csv_directory).__next__()[2]
stats_file_list = os.walk(stats_directory).__next__()[2]


# The id column is needed to signify that these are different time series to ts_fresh
time_series_id = 1
main_df = None
y = []

for csv_file_name in csv_file_list:

    file_name = csv_file_name.split("_reuse.csv")[0]
    stats_file_name = "{}_reuse_stats.json".format(file_name)
    stats_file_loc = os.path.join(stats_directory, stats_file_name)
    csv_file_loc = os.path.join(csv_directory, csv_file_name)

    if os.path.isfile(stats_file_loc):

        stats_file = open(stats_file_loc)
        df = pandas.read_csv(csv_file_loc, names=["ts"])

        #pdb.set_trace()

        df.insert(0, "time", range(0, len(df)))
        df.insert(1, "id", [time_series_id]*len(df))
        time_series_id += 1

        #pdb.set_trace()

        if main_df is None:
            main_df = df
            main_df.to_csv("test_reuse_distance_csv.csv", index=False)
        else:
            main_df = main_df.append(df)

        #pdb.set_trace()

        data = literal_eval(json.load(stats_file))
        y.append(data["min_cache_size_70"])

        print("Done processing {} with time_series_id {}".format(csv_file_name, time_series_id))

        if time_series_id > limit:
            break


    else:
        print("Stats file not found {}, for csv {}".format())

main_df.to_csv("{}.csv".format(output_file_name), index=False)
y_df = pandas.DataFrame(y)
y_df.to_csv("70_{}.csv".format(output_file_name), index=False)