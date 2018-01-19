import wap_cal_time as cal_time

# print ("Hello, world!")

c_t = cal_time.CalTime()
time_strs = raw_input()
# time_strs = '''2017/01/30 08:00-12:00 13:00-16:00
# 2017/01/31 00:00-04:00 08:00-12:00 13:00-16:00
# 2017/02/01 08:00-12:00 13:00-16:00
# 2017/02/02 08:00-12:00 13:00-16:00
# 2017/02/03 08:00-12:00 13:00-18:00 20:00-23:00
# 2017/02/06 13:00-16:00
# 2017/02/07 08:00-12:00 13:00-16:00 17:00-23:00'''
c_t.input_calendar(time_strs)
calendar_results = c_t.calc_time()
c_t.show_results(calendar_results)
