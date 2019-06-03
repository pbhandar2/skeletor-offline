import sys
from guppy import hpy
h = hpy()

sys.path.append('../')

from skeletor import Skeletor
processor = Skeletor()
processor.open_file("web_0.csv.gz", "../trace_config.json", "MSR-Cambridge")
profiler = processor.get_io_profiler()
profiler.metric_calculator()

print(len(profiler.reader.data["io_type"]))
print(len(profiler.reader.data["time"]))
print(profiler.reader.data["time"][1:10])


print h.heap()