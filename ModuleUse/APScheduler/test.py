# -*- coding: utf-8  -*-
# -*- author: jokker -*-

"""
非阻塞调度，在指定的时间执行一次
"""


from datetime import datetime
import time
import os

from apscheduler.schedulers.background import BackgroundScheduler  # 非阻塞方式
from apscheduler.schedulers.blocking import BlockingScheduler  # 阻塞方式

def tick():
    print('Tick! The time is: %s' % datetime.now())
    time.sleep(10)


if __name__ == '__main__':

    # scheduler = BackgroundScheduler()
    # scheduler.add_job(tick, 'interval', seconds=3)
    # scheduler.add_job(tick, 'interval', seconds=5)
    # scheduler.add_job(tick, 'interval', minutes=1)  # todo 非阻塞方式 触发方式为时间间隔， 可以换一种触发方式
    # scheduler.add_job(tick, 'date', run_date='2016-02-14 15:01:05')  # todo 非阻塞方式 在指定的时间，只执行一次


    scheduler = BlockingScheduler()
    scheduler.add_job(tick, 'cron', day_of_week='6', second='*/5')  # todo 阻塞的方式，间隔3秒执行一次


    # 这里的调度任务是独立的一个线程
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    i = 0

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while i < 5:
            i += 1
            # 其他任务是独立的线程执行
            time.sleep(5)
            print('sleep!')
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
        print('Exit The Job!')

    print('stop')
