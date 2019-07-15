def get_percentiles(hit_rate_array, max_hit_rate, percentiles):

	percentiles_array = []

	for p in sorted(percentiles):
		percentiles_array.append(p * max_hit_rate)

	current_percentile_index = 0
	cache_size_array = []

	for i, hit_rate in enumerate(hit_rate_array):
		if hit_rate >= percentiles_array[current_percentile_index]:
			current_percentile_index += 1
			cache_size_array.append(i)

			if current_percentile_index == len(percentiles_array):
				return cache_size_array

	raise ParamError("Please check the parameters to the function get_percentiles, \
		the percentiles of max_hit_rate are not in the hit_rate_array")



