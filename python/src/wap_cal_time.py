import wap_parser as parser
import wap_calendar as calendar
import datetime

class CalTime:

	def __init__(self):
		self.calendar = calendar.Calendar()
		self.parser   = parser.TimeParser()
		self.week_time = []
	def input_calendar(self, input):
		results = self.parser.parse_times(time_strs)
		calendar_results = self.calendar.create_month_week(results)
		self.calendar_data = calendar_results
		# return calendar_results

	def calc_time(self):
		for c_day in self.calendar_data:
			print c_day[0], c_day[1], c_day[2], c_day[4]
			if c_day[4] in [1, 2, 3, 4, 5]:
				self.calc_workday_time(c_day)
			elif c_day[4] in [0, 6]:
				self.calc_holiday_time(c_day)
		print self.week_time

	# workday
	def calc_workday_time(self, date_data):
		# amount_time, in_law_overtime, out_law_overtime, midnight, saturday, sunday
		ini_t = datetime.timedelta()
		if date_data[4] == 1:
			self.week_time.append([ini_t, ini_t, ini_t, ini_t, ini_t, ini_t])
		time_amount = datetime.timedelta()
		current_time = self.week_time[-1]
		for c_day_time in date_data[3]:
			time_amount += c_day_time[1] - c_day_time[0]
			current_time[0] += time_amount
			self.count_overtime(date_data, time_amount)

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

	def count_overtime(self, date_data, time_amount):
		current_time = self.week_time[-1]
		in_law_time = datetime.timedelta(hours=7)
		out_law_time = datetime.timedelta(hours=8)
		if time_amount > out_law_time:
			print time_amount ,"Out law overtime"
			out_law_overtime_amount = time_amount - out_law_time
			current_time[1] += datetime.timedelta(hours=1)
			current_time[2] += out_law_overtime_amount
		elif time_amount > in_law_time:
			print time_amount ,"In law overtime"
			in_law_overtime_amount = time_amount - in_law_time
			current_time[1] += in_law_overtime_amount

	def count_midnight(self, date_data):
		pass

c_t = CalTime()
time_strs = '''2017/01/30 08:00-12:00 13:00-16:00
2017/01/31 08:00-12:00 13:00-16:00
2017/02/01 08:00-12:00 13:00-16:00
2017/02/02 08:00-12:00 13:00-17:00
2017/02/03 08:00-12:00 13:00-19:00
2017/02/04 10:00-12:00 13:00-18:00
2017/02/05 13:00-17:00 18:00-23:00
2017/02/06 13:00-16:00
2017/02/07 08:00-12:00 13:00-16:00 17:00-23:00'''
c_t.input_calendar(time_strs)
c_t.calc_time()
