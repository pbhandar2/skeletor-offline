from skeletor import skeletor

file_name = "casa-110108-112108.1.blkparse"
file_loc = "/home/pranav/Desktop/Research/traces/fiu/home1/{}".format(file_name)

processor = skeletor()
processor.open_file(file_loc, "../trace_config.json", trace_type="FIU")

profiler = processor.get_io_profiler()
profiler.plot_scatter_interval_vanila("block", "{}".format(file_name), 1800, binSize=0, markerSize=5)
