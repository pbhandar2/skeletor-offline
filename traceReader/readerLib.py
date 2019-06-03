func_map = {
    "float":  lambda x: float(x),
    "integer": lambda x: int(x),
    "string": lambda x: str(x)
}

def process_line(line, fields):
	field_value_json = {}

	try:
		for key in fields:
			field_obj = fields[key]
			field_value = line[field_obj["index"]]
			field_value_json[key] = func_map[field_obj["type"]](field_value)
	except:
		print("Error encountered")
		print("Line: {}".format(line))
		print("Key: {}".format(key))

	return field_value_json



