import gzip, sys, os, math, tarfile

file_location = "../test/web_1.csv.gz"
output_file_dir = "./"
if len(sys.argv) > 1:
	file_location = sys.argv[1]
if len(sys.argv) > 2:
	output_file_dir = sys.argv[2]

page_size = 4096

output_file_name = os.path.join(output_file_dir, "{}_{}.csv".format(file_location.split("/")[-1], page_size))

with tarfile.open(file_location) as t:
	with open(output_file_name, 'w+') as g:

		member_list = sorted(t.getnames(), key=lambda k: int(k.split(".")[-2]))

		for member in member_list:

			f = t.extractfile(member)
	
			line = f.readline().decode("utf-8")

			while len(line) > 0:

				line_split = line.split(" ")

				label = int(line_split[3])
				size = int(line_split[4]) * 512

				page_start = int(math.floor(label/page_size))
				page_end = int(math.floor((label + size)/page_size))

				while page_start <= page_end:
					string_write = "{}\n".format(page_start)
					g.write(string_write)
					page_start += page_size

				line = f.readline().decode("utf-8")



