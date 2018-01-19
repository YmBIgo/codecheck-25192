#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import wap_cal_time as cal_time
import sys
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

class Calendar:
	# Calendar data structure
	# [Year, Month, Day, [Time...], Week, Holiday_Bool]
	def __init__(self):
		self.year 		= 2017
		self.month 		= 1
		self.day 		= 1
		self.week 		= 1  # sun:0/mon:1/tue:2/...sat:6
	def set_day(self, year=2017, month=1, day=1):
		self.year 		= year
		self.month		= month
		self.day 		= day
	def special_holiday(self, month):
		holiday = [[1,1],[1,2],[1,9],[2,11],[3,20],[4,29],[5,3],[5,4],[5,5],[7,17],[8,11],[9,18],[9,23],[10,9],[11,3],[11,23],[12,23]]
		for d_data in month:
			if d_data[2:3] in holiday:
				d_data[5] = False
	def create_month_week(self, input_data):
		month_result = []
		# for m_count in range(len(month_week)):
			# if month_week[m_count] in [0, 6]:
			# 	month_result.append([self.year, self.month, m_count+1, [], month_week[m_count], False])
			# elif month_week[m_count] in [1, 2 ,3, 4, 5]:
			# 	month_result.append([self.year, self.month, m_count+1, [], month_week[m_count], True])
		# self.special_holiday(month_result)
		# return month_result
		for input_day in input_data:
			self.set_day(input_day[0], input_day[1], input_day[2])
			month_week = self.month_day_week()
			if month_week in [0, 6]:
				month_result.append([self.year, self.month, self.day, input_day[3], month_week, False])
			elif month_week in [1, 2 ,3, 4, 5]:
				month_result.append([self.year, self.month, self.day, input_day[3], month_week, True])
		return month_result
	def uruu_year_month(self):
		uruu_month_day = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
		if self.year % 400 == 0:
			return uruu_month_day
		elif self.year % 4 == 0 and self.year % 100 == 0:
			return month_day
		elif self.year % 4 == 0:
			return uruu_month_day
		else:
			return month_day
	def month_day_week(self):
		month_days 		= self.uruu_year_month()
		first_day_week 	= self.first_day_week()
		amount_day		= 0
		if self.month != 1:
			for m_d1 in month_days[:self.month-1]:
				amount_day += m_d1
		month_day_week = (amount_day+first_day_week+self.day-1) % 7
		# month_first_day_week = (amount_day+first_day_week) % 7
		# month_day_week = [(m_d2+month_first_day_week-1)%7 for m_d2 in range(1, month_days[self.month-1]+1) ]
		return month_day_week
	def first_day_week(self):
		year_week 	= [0, 1, 2, 3, 5, 6, 0, 1, 3, 4, 5, 6, 0, 2] # 2017-2030
		return year_week[self.year-2017]

class CalTime:

	def __init__(self):
		self.calendar = Calendar()
		self.parser   = TimeParser()
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

def main(argv):
	c_t = CalTime()
	# time_strs = '''2017/01/30 08:00-12:00 13:00-16:00
	# 2017/01/31 00:00-04:00 08:00-12:00 13:00-16:00
	# 2017/02/01 08:00-12:00 13:00-16:00
	# 2017/02/02 08:00-12:00 13:00-16:00
	# 2017/02/03 08:00-12:00 13:00-18:00 20:00-23:00
	# 2017/02/06 13:00-16:00
	# 2017/02/07 08:00-12:00 13:00-16:00 17:00-23:00'''
	c_t.input_calendar(argv[1])
	calendar_results = c_t.calc_time()
	# print c_t.show_results(calendar_results)
	for i in c_t.show_results(calendar_results):
		print i

# main(sys.argv)
