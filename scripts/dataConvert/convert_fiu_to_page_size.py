import gzip, sys, os, math

file_location = "./homes-1101108-112108.20.blkparse"
output_file_dir = "./"
if len(sys.argv) > 1:
	file_location = sys.argv[1]
if len(sys.argv) > 2:
	output_file_dir = sys.argv[2]

page_size = 4096

output_file_name = os.path.join(output_file_dir, "{}_{}.csv".format(file_location.split("/")[-1], page_size))

with open(file_location) as f:
	with open(output_file_name, 'w+') as g:
		line = f.readline().decode("utf-8")

		while len(line) > 0:

			line_split = line.split(",")

			label = int(line_split[4])
			size = int(line_split[5])

			page_start = int(math.floor(label/page_size))
			page_end = int(math.floor((label + size*512)/page_size))

			while page_start <= page_end:
				string_write = "{}\n".format(page_start)
				g.write(string_write)
				page_start += page_size

			line = f.readline().decode("utf-8")




