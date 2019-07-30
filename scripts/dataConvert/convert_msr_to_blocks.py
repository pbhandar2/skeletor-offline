import gzip, sys, os, math, sys

file_location = "./test/data/web_1.csv.gz"
output_file_dir = "./test/data/"
if len(sys.argv) > 1:
	file_location = sys.argv[1]
if len(sys.argv) > 2:
	output_file_dir = sys.argv[2]

page_size = 512

output_file_name = os.path.join(output_file_dir, "{}_{}.csv".format(file_location.split("/")[-1], page_size))

with gzip.open(file_location) as f:
	with open(output_file_name, 'w+') as g:
		line = f.readline().decode("utf-8")

		while len(line) > 0:

			line_split = line.split(",")

			label = int(line_split[4])
			size = int(line_split[5])

			page_start = int(label)
			page_end = int(math.floor(label + size))

			while page_start <= page_end:
				string_write = "{}\n".format(page_start)
				g.write(string_write)
				page_start += page_size

			line = f.readline().decode("utf-8")




