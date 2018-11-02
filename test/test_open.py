from skeletor import skeletor

file_loc = "web_0.csv.gz"

processor = skeletor()
processor.test_print()
processor.open_file(file_loc, trace_type="MSR_Cambridge")

# print(processor.read_next_line())
# print(processor.read_next_line())
# for i in range(100):
#     print(processor.get_next_line_array()[-2])



profiler = processor.get_io_profiler()

profiler.metric_calculator()

profiler.get_access_matrix("matrix.dat")

#profiler.plot_distribution("offset", "./test_fig.svg")

#profiler.plot_scatter("block", "./test_scatter_0.1_5bin.png", binSize=5, markerSize=5)
