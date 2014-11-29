# -*- coding: UTF-8 -*-
__author__ = 'tizianoj'

import os.path
import time
import datetime
import dropbox
import shutil
import watchdog.observers
import watchdog.events

from config import *
try:
    from config_local import *
except:
    pass

def wait_for_file_ready(file_path):
    """
    Checs if able to open a file. It retries every second for config.WAIT_UPLOAD_MAX_TIME_SECONDS.
    :param file_path: File path to be checked
    :return: True if able to open the file in read/write, false if it did not succeded
    """
    ready = False
    counter = 0
    while not ready:
        try:
            with open(file_path) as f:
                ready = True
        except (IOError, OSError) as ex:
            if counter >= WAIT_UPLOAD_MAX_TIME_SECONDS:
                logging.warning("Warning: file %s not ready after %s second(s)" % (file_path, counter))
                raise ex
            else:
                logging.info("File %s not ready after %s second(s), retrying..." % (file_path, counter))
                counter += 1
                time.sleep(1)
    return True


# Dropbox API's at https://www.dropbox.com/developers/core/docs/python
class FileHandler2Box(watchdog.events.FileSystemEventHandler):
    def __init__(self):
        super().__init__()
        self.dropbox_client = dropbox.client.DropboxClient(ACCESS_TOKEN)

    def on_created(self, event):
        event_time = datetime.datetime.now()
        try :
            if not event.is_directory:
                src_path = event.src_path
                logging.debug("Created filename %s" % src_path)

                # watchdog is cross platform, so it does not listen to Linux event of finished writing
                # Trying this way to wait for the file, alternatively I could chck filesze or revert to
                # pyinotify, Linux only library and catch event IN_CLOSE_WRITE
                wait_for_file_ready(src_path)

                # Organizing the structure and filenames
                
                remote_base_dir = "%s/%s" % (BASE_DIR_TO_UPLOAD, event_time.strftime("%Y-%m-%d"))
                local_base_dir = os.path.join(os.path.dirname(src_path), event_time.strftime("%Y-%m-%d"))
                filename = "%s_%s" % (event_time.strftime("%H_%M_%S"), os.path.basename(src_path))
                local_path = os.path.join(local_base_dir,filename)
                remote_path = remote_base_dir + "/" + filename

                # Moving thefile. It is moved outside the watched directory
                if not os.path.exists(local_base_dir):
                    os.makedirs(local_base_dir)
                    logging.debug("Created %s" % local_base_dir)
                shutil.move(src_path, local_path)
                logging.debug("Moved locally %s to %s" % (src_path, local_path))

                # Dropbox uploading
                with open(local_path, 'rb') as f:
                    logging.debug("Updating to %s" % remote_path)
                    response = self.dropbox_client.put_file(remote_path, f)
                    logging.debug("Uploaded: %s" % response)
        except Exception as e:
            logging.warning(e)

if __name__ == "__main__":
    if ACCESS_TOKEN == "<insert your access token here>":
        print("Please configure the program editing config.py file!")
        exit(-1)
    event_handler = FileHandler2Box()
    observer = watchdog.observers.Observer()
    # FIXME it should be not recursive, but once it uplaode D:\tmp\2014-11-29\20_32_40_510sH8glGlL._SL500_AA300_.jpg.
    # Maybe at directory creation?
    observer.schedule(event_handler, DIR_TO_MONITOR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

