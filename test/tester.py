import sys
sys.path.append('../')

from skeletor import Skeletor
processor = Skeletor("../trace_config.json", "MSR-Cambridge")

print(processor.config)