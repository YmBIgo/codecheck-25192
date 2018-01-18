import json

class Calendar:
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
				d_data[4] = False
	def create_month(self):
		month_week = self.month_day_week()
		month_result = []
		for m_count in range(len(month_week)):
			if month_week[m_count] in [0, 6]:
				month_result.append([self.year, self.month, m_count+1, month_week[m_count], False])
			elif month_week[m_count] in [1, 2 ,3, 4, 5]:
				month_result.append([self.year, self.month, m_count+1, month_week[m_count], True])
		# self.special_holiday(month_result)
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
		month_first_day_week = (amount_day+first_day_week) % 7
		print month_first_day_week
		month_day_week = [(m_d2+month_first_day_week-1)%7 for m_d2 in range(1, month_days[self.month-1]+1) ]
		return month_day_week
	def first_day_week(self):
		year_week 	= [0, 1, 2, 3, 5, 6, 0, 1, 3, 4, 5, 6, 0, 2] # 2017-2030
		return year_week[self.year-2017]
