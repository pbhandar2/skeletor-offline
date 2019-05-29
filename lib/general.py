import json

def check_config(json_file_location, trace_type):

	json_file_handle = open(json_file_location, 'r')
	config_json_array = json.load(json_file_handle)

	assert type(config_json_array) == list

	trace_type_config = None 

	for config_json in config_json_array:
		if config_json["name"] == trace_type:
			trace_type_config = config_json
			break

	if trace_type_config is None:
		raise Exception("The type {} was not found in the json file at {}. Please check to make sure that the name provided matches the name field in one of the json entries in the file.".format(trace_type, json_file_location))

	return trace_type_config





