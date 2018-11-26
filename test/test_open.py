from skeletor import skeletor

#file_loc = "web_0.csv.gz"

file_loc = "/home/pranav/Desktop/Research/traces/FIU/casa-110108-112108.1.blkparse"

processor = skeletor()
processor.open_file(file_loc, "../trace_config.json", trace_type="FIU")

profiler = processor.get_io_profiler()

#profiler.metric_calculator()

# step_size = 1800
# for i in range(48):
# 	profiler.plot_scatter_interval("block", "test_scatter_fiu_0.1_5bin_TEST.png", [i*step_size, (i+1)*step_size], binSize=0, markerSize=5)


#processor.test_print()
#processor.open_file(file_loc, trace_type="MSR_Cambridge")

# processor.open_file(file_loc, trace_type="FIU")

# # print(processor.read_next_line())
# # print(processor.read_next_line())
for i in range(100):
    line = processor.get_next_line_array()
    if (line[5])



# profiler = processor.get_io_profiler()

# profiler.metric_calculator()

# profiler.get_access_matrix("matrix.dat")

#profiler.plot_distribution("offset", "./test_fig.svg")

#profiler.plot_scatter("block", "./test_scatter_fiu_0.1_5bin.png", binSize=5, markerSize=5)
