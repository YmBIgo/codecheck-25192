import wap_parser as parser
import wap_calendar as calendar
import datetime

class CalTime:

	def __init__(self):
		self.calendar = calendar.Calendar()
		self.parser   = parser.TimeParser()
		ini_t = datetime.timedelta()
		self.week_time = [[ini_t, ini_t, ini_t, ini_t, ini_t, ini_t]]
	def input_calendar(self, input):
		results = self.parser.parse_times(input)
		calendar_results = self.calendar.create_month_week(results)
		self.calendar_data = calendar_results
		# return calendar_results

	def calc_time(self):
		for c_day in self.calendar_data:
			# print c_day[0], c_day[1], c_day[2], c_day[4]
			if c_day[4] in [1, 2, 3, 4, 5]:
				self.calc_workday_time(c_day)
			elif c_day[4] in [0, 6]:
				self.calc_holiday_time(c_day)
		return self.week_time

	# workday
	def calc_workday_time(self, date_data):
		# amount_time, in_law_overtime, out_law_overtime, midnight, saturday, sunday
		ini_t = datetime.timedelta()
		if date_data[4] == 1:
			self.week_time.append([ini_t, ini_t, ini_t, ini_t, ini_t, ini_t])
		current_time = self.week_time[-1]
		day_ammount = datetime.timedelta()
		for c_day_time in date_data[3]:
			time_amount = datetime.timedelta()
			time_amount += c_day_time[1] - c_day_time[0]
			day_ammount += time_amount
		# print date_data[0], date_data[1], date_data[2]
		# print day_ammount
		self.count_overtime(date_data, day_ammount)
		self.count_midnight(date_data[3])
		current_time[0] += day_ammount

	# holiday
	def calc_holiday_time(self, date_data):
		# amount_time, in_law_overtime, out_law_overtime, midnight, saturday, sunday
		ini_t = datetime.timedelta()
		if date_data[4] == 1:
			self.week_time.append([ini_t, ini_t, ini_t, ini_t, ini_t, ini_t])
		time_amount = datetime.timedelta()
		current_time = self.week_time[-1]
		for c_day_time in date_data[3]:
			time_amount += c_day_time[1] - c_day_time[0]
			if date_data[4] == 6:
				current_time[4] += time_amount
			elif date_data[4] == 0:
				current_time[5] += time_amount
			current_time[0] += time_amount
		self.count_midnight(date_data[3])

	def count_overtime(self, date_data, time_amount):
		current_time = self.week_time[-1]
		in_law_time = datetime.timedelta(hours=7)
		out_law_time = datetime.timedelta(hours=8)

		if self.check_overtime() == True:
			current_time[2] += time_amount
		else:
			if (current_time[0]+time_amount) > datetime.timedelta(hours=40):
				current_work_hour = current_time[0] + time_amount
				in_40_overwork_time =  current_work_hour - datetime.timedelta(hours=40)
				current_time[2] += in_40_overwork_time
				# print time_amount, "Out of law overtime 40hour", in_40_overwork_time
			elif time_amount > out_law_time:
				out_law_overtime_amount = time_amount - out_law_time
				# print time_amount ,"Out of law overtime", out_law_overtime_amount
				current_time[1] += datetime.timedelta(hours=1)
				current_time[2] += out_law_overtime_amount
			elif time_amount > in_law_time:
				# print time_amount ,"In law overtime"
				in_law_overtime_amount = time_amount - in_law_time
				current_time[1] += in_law_overtime_amount

	def check_overtime(self):
		current_time = self.week_time[-1]
		if current_time[0] < datetime.timedelta(hours=40):
			return False
		else:
			return True

	def count_midnight(self, date_data):
		current_time = self.week_time[-1]
		checker_5am = datetime.datetime(1900, 1, 1, 5, 0)
		checker_22pm = datetime.datetime(1900, 1, 1, 22, 0)
		for day_data in date_data:
			# 5am
			if day_data[0] <= checker_5am:
				# print "5am", day_data[1]
				midnight_hours = datetime.timedelta()
				if day_data[1] >= checker_5am:
					midnight_hours = checker_5am - day_data[0]
				elif day_data[1] <= checker_5am:
					midnight_hours = day_data[1] - day_data[0]
				current_time[3] += midnight_hours
			elif day_data[1] >= checker_22pm:
				# print "10pm", day_data[1]
				midnight_hours = day_data[1] - checker_22pm
				current_time[3] += midnight_hours

	def show_results(self, calendar_results):
		ini_t = datetime.timedelta()
		results = [ini_t, ini_t, ini_t, ini_t, ini_t]
		results_str = []
		for calendar_data in calendar_results:
			for i in range(5):
				results[i] += calendar_data[i+1]
		for r in results:
			results_str.append(str(r.seconds/3600))
		return results_str

# c_t = CalTime()
# time_strs = '''2017/01/30 08:00-12:00 13:00-16:00
# 2017/01/31 00:00-04:00 08:00-12:00 13:00-16:00
# 2017/02/01 08:00-12:00 13:00-16:00
# 2017/02/02 08:00-12:00 13:00-16:00
# 2017/02/03 08:00-12:00 13:00-18:00 20:00-23:00
# 2017/02/06 13:00-16:00
# 2017/02/07 08:00-12:00 13:00-16:00 17:00-23:00'''
# c_t.input_calendar(time_strs)
# calendar_results = c_t.calc_time()
# c_t.show_results(calendar_results)
