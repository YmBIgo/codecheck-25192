import datetime

class TimeParser:
	# Parser Data Structure
	# [Year, Month, Day, [[Start, End]...]]
	def __init__(self):
		pass
	def parse_times(self, time_strs):
		parsed_results = []
		for t_str in time_strs.split('\n')[1:]:
			parsed_results.append(self.parse_time(t_str))
		return parsed_results
	def parse_time(self, time_str):
		# input example
		# 2017/01/30 08:00-12:00 13:00-16:00
		# 2017/01/31 08:00-12:00 13:00-16:00
		# 2017/02/01 08:00-12:00 13:00-16:00
		splited_time = time_str.split(' ')
		date_result  = self.parse_date(splited_time[0])
		hour_results = []
		for d_str in splited_time[1:]:
			hour_results.append(self.parse_hour(d_str))
		date_result.append(hour_results)
		return date_result

	def parse_date(self, date_str):
		# 2017/02/01
		parsed_date_result = []
		for s_d in date_str.split('/'):
			parsed_date_result.append(int(s_d))
		return parsed_date_result
	def parse_hour(self, hour_str):
		# 08:00-12:00
		splited_hour = hour_str.split('-')
		hour_results = []
		for s_h in splited_hour[:2]:
			# h_datetime = datetime.datetime.strptime(s_h, '%H:%M').time()
			h_datetime = datetime.datetime.strptime(s_h, '%H:%M')
			hour_results.append(h_datetime)
		return hour_results

# p = TimeParser()
# time_strs = '''2017/01/30 08:00-12:00 13:00-16:00
# 2017/01/31 08:00-12:00 13:00-16:00
# 2017/02/01 08:00-12:00 13:00-16:00
# 2017/02/02 08:00-12:00 13:00-16:00
# 2017/02/03 08:00-12:00 13:00-16:00
# 2017/02/06 13:00-16:00
# 2017/02/07 08:00-12:00 13:00-16:00 17:00-23:00'''
# results = p.parse_times(time_strs)
# print results
