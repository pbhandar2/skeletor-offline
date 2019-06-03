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

			if key == "io_type":
				if field_obj["values"]["read"] == field_value:
					field_value = 'r'
				elif field_obj["values"]["write"] == field_value:
					field_value = 'w'

			field_value_json[key] = func_map[field_obj["type"]](field_value)
	except:
		print("Error encountered")
		print("Line: {}".format(line))
		print("Key: {}, Field Value: {}".format(key, field_value))

	return field_value_json



