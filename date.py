import datetime
import time

date = datetime.datetime.strptime("2021-03-19 09:13:00+00:00".replace('+00:00',''),"%Y-%m-%d %H:%M:%S")
tuple = date.timetuple()
timestamp = time.mktime(tuple)
print(time.ctime(timestamp).replace(' ','-'))