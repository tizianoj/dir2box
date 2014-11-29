# -*- coding: UTF-8 -*-
__author__ = 'tizianoj'

import os.path
import time
import datetime

import dropbox
import watchdog.observers
import watchdog.events

from config import *


try:
    from config_local import *
except:
    pass

# Dropbox API's at https://www.dropbox.com/developers/core/docs/python

class FileHandler2Box(watchdog.events.FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.dropbox_client= dropbox.client.DropboxClient(ACCESS_TOKEN)

    def on_created(self, event):
        if not event.is_directory:
            src_path=event.src_path
            logging.debug("Created filename %s" % src_path)

            # Todo wait somehow for file finished writing!.
            # See https://groups.google.com/forum/#!topic/watchdog-python/zExJb0Y5k3w
            # Probably best way is to check filesize increases in time, since watchdog is
            # cross platform and event of finished writing is not supported on all the OS

            # See http://stackoverflow.com/questions/23894221/upload-file-to-my-dropbox-from-python-script
            time_now = datetime.datetime.now()
            remote_base_dir="%s/%s" % (BASE_DIR_TO_UPLOAD, time_now.strftime("%Y-%m-%d"))
            remote_filename="%s_%s" % (time_now.strftime("%H_%M_%S"), os.path.basename(src_path))
            remote_path=remote_base_dir + "/" + remote_filename

            # Todo move file locally too!

            # self.dropbox_client.file_create_folder(remote_base_dir)
            with open(src_path, 'rb') as f :
                logging.debug("Updating to %s" % remote_path)
                response = self.dropbox_client.put_file(remote_path, f)
                logging.debug("Uploaded: %s" % response)



if __name__ == "__main__":
    event_handler = FileHandler2Box()
    observer = watchdog.observers.Observer()
    observer.schedule(event_handler, DIR_TO_MONITOR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

