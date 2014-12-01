dir2box
=======

A simple python daemon for uploading a filesystem directory to dropbox. Developed in order to upload files from my home 
surveillance ftp server (a RaspberryPi :-) ) as soon as files are uploaded.

Create your own application at https://www.dropbox.com/developers/apps, get an access token and save it into the header
of file at the ACCESS_TOKEN constant. App has to be able to work with Core APIs and to manage files.

Check configuration in file header: all the files in DIR_TO_MONITOR will be watched. When a new file arrives there, a
subdirectory with date pattern will be created and file will be time prefixed and moved there. An identical structure
will be replicated and uploaded to dropbox under BASE_DIR_TO_UPLOAD with same structure.

Going to use it in the directory where my surveillance camera pictures get ftp'ed so that they will get directly sorted
and uploaded to my dropbox.

The script is meant to be as lightweight as possible, and to not write too much on the same sectors, so that a
Raspberry Pi with SD memory can handle it without problems and heavy synchronizations.

Installation
=======

Install requirements:
 * (for Raspberry PI Rasbian users) sudo apt-get install python-dev python-pip
 * sudo pip install watchdog
 * sudo pip install dropbox

copy dir2box.py everywhere and edit it. In the parameter section, change the parameters

If you want to run it as a daemon, check instructions under daemon/readme.txt





