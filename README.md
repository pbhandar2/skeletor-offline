# skeletor-offline

A framework for analysis of block I/O traces. Configure the trace_config.json to tell the framework about the format of the trace. The framework will extract the necessary information and give you the metrics of the workload. 

Currently the workload metrics that it gives are: 

self.metrics = {
	"read_count": 0,
	"write_count": 0,
	"total_io": 0,
	"read_write_ratio": None,
	"read_rate": None,
	"write_rate": None,
	"io_rate": None,
	"total_io_size": 0,
	"total_read_size": 0,
	"total_write_size": 0,
	"average_read_size": None,
	"average_write_size": None,
	"average_io_size": None,
	"min_read_size": None,
	"min_write_size": None,
	"max_read_size": None,
	"max_write_size": None
}

To test, run the tester.py in the test folder. 

