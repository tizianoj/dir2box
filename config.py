# -*- coding: UTF-8 -*-
__author__ = 'tizianoj'

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Obtain one for your personal app from https://www.dropbox.com/developers/apps
# App has to be able to work with Core APIs and to manage files.
ACCESS_TOKEN="<insert your access token here>"

DIR_TO_MONITOR = "/media/disk/mylocaldir"
BASE_DIR_TO_UPLOAD = "/my_cloud_dir"
WAIT_UPLOAD_MAX_TIME_SECONDS = 60