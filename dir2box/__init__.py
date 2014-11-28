# -*- coding: UTF-8 -*-
__author__ = 'tizianoj'

import sys
import time
import datetime
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

if __name__ == "__main__":
    time_now=datetime.datetime.now()
    full_date_str=time_now.strftime("%Y-%m-%d")
    date_str=time_now.strftime("%Y-%m-%d_%H:%M:%S")

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()