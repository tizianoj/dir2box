#!/usr/bin/env python

# -*- coding: UTF-8 -*-

__author__ = 'tizianoj'

import os.path
import time
import datetime
import dropbox
import logging
import shutil
import getopt
import watchdog.observers
import watchdog.events
import sys

# ####################### CONFIGURATION START ########################

# Obtain one for your personal app from https://www.dropbox.com/developers/apps
# App has to be able to work with Core APIs and to manage files.
ACCESS_TOKEN = "<insert your access token here>"


DIR_TO_MONITOR = "/home/pi/cameras"
BASE_DIR_TO_UPLOAD = "/Cameras"
DIR_DATE_FORMAT = "%Y-%m-%d"
LOG_LEVEL=logging.WARNING
WAIT_UPLOAD_MAX_TIME_SECONDS = 60



# ######################## CONFIGURATION END #########################

try:
    from config_local import *
except:
    pass

logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s:%(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

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


# Dropbox API's at http://dropbox-sdk-python.readthedocs.io/en/latest/
class FileHandler2Box(watchdog.events.FileSystemEventHandler):
    def __init__(self):
        # super().__init__() # Python 3 code
        super(watchdog.events.FileSystemEventHandler, self).__init__() # Compatible with python2 too
        self.dropbox_client = dropbox.Dropbox(ACCESS_TOKEN)

    def on_created(self, event):
        event_time = datetime.datetime.now()
        src_path = event.src_path

        try:
            # There is a bug in watchdog? After a subdirectory is created first time  and file is moved there, whatchdog
            # will report the event for file in subdir even in observer is not recursive. I have to take that in account
            # hence this tmp1 == tmp2 check
            tmp1 = os.path.dirname(src_path)
            tmp2 = os.path.dirname(os.path.join(DIR_TO_MONITOR.rstrip("/\\"), "dummy"))  # cannot dirname on a directory
            if (not event.is_directory) and (tmp1 == tmp2):

                logging.debug("Created filename %s" % src_path)

                # watchdog is cross platform, so it does not listen to Linux event of finished writing
                # Trying this way to wait for the file, alternatively I could chck filesze or revert to
                # pyinotify, Linux only library and catch event IN_CLOSE_WRITE
                wait_for_file_ready(src_path)

                # Organizing the structure and filenames

                remote_base_dir = "%s/%s" % (BASE_DIR_TO_UPLOAD, event_time.strftime(DIR_DATE_FORMAT))
                local_base_dir = os.path.join(os.path.dirname(src_path), event_time.strftime(DIR_DATE_FORMAT))
                filename = "%s_%s" % (event_time.strftime("%H_%M_%S"), os.path.basename(src_path))
                local_path = os.path.join(local_base_dir, filename)
                remote_path = remote_base_dir + "/" + filename

                # Moving the file. It is moved outside the watched directory.
                if not os.path.exists(local_base_dir):
                    os.makedirs(local_base_dir)
                    logging.debug("Created %s" % local_base_dir)

                shutil.move(src_path, local_path)
                logging.debug("Moved locally %s to %s" % (src_path, local_path))

                # Dropbox uploading
                with open(local_path, 'rb') as f:
                    content = f.read()
                    logging.debug("Updating to %s" % remote_path)
                    response = self.dropbox_client.files_upload(content, remote_path, mode=dropbox.files.WriteMode('add'), autorename=True, mute=True)
                    logging.debug("Uploaded: %s" % response)
        except Exception as e:
            logging.warning(e)


def main():
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

def is_file_to_delete(filename, days):
    try :
        file_date = datetime.datetime.strptime(filename, DIR_DATE_FORMAT)
        if ( datetime.datetime.now() - file_date > datetime.timedelta(days=days) ) :
            return True
    except  :
        logging.debug("Filename " + filename + " is not a date")
    return False

def delete_older_than(days) :
    all_files=os.listdir(DIR_TO_MONITOR)
    dropbox_client = dropbox.Dropbox(ACCESS_TOKEN)
    for f in all_files :
        if is_file_to_delete(f, days) :
            logging.info("Deleting %s since older than %s days" % (f, days))
            shutil.rmtree(os.path.join(DIR_TO_MONITOR, f))

            remote_f = "%s/%s" % (BASE_DIR_TO_UPLOAD, f)
            try :
                dropbox_client.files_delete_v2(remote_f)
            except dropbox.files.DeleteError as de :
                logging.warning(de)







if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    if ACCESS_TOKEN == "<insert your access token here>":
        print("Please configure the program editing the configuration lines!")
        exit(-1)

    try :
        opts, args = getopt.getopt(sys.argv[1:],"c:") # accetta parametro -c con valore
        for o, a in opts :
            if o == "-c" :
                # TODO: Message in case not integer
                days = int(a)
                delete_older_than(days)
                sys.exit(0)
        else :
            main()
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)


