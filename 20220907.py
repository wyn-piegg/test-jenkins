# -*- coding: utf-8 -*-
import datetime
import time
from datetime import date

# time_now = time.strftime("%D", time.localtime())

# t = date.toLocaleDateString()
now_time = datetime.datetime.now().strftime("%Y%m%d")
print(now_time)

