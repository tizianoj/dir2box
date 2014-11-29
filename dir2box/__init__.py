# -*- coding: UTF-8 -*-
__author__ = 'tizianoj'

import sys
import time
import datetime
import logging
import watchdog.observers
import watchdog.events

DIR_TO_MONITOR = "D:\\tmp"


class MyFileHandler(watchdog.events.FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print("Created filename %s" % event.src_path)

if __name__ == "__main__":
    time_now = datetime.datetime.now()
    full_date_str = time_now.strftime("%Y-%m-%d")
    date_str = time_now.strftime("%Y-%m-%d_%H:%M:%S")

    # path = sys.argv[1] if len(sys.argv) > 1 else '.'
    path = DIR_TO_MONITOR
    event_handler = MyFileHandler()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()