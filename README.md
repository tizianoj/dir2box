dir2box
=======

A simple python daemon for uploading a filesystem directory to dropbox. Developed in order to upload files from my home 
surveillance ftp server (a RaspberryPi :-) ) as soon as files are uploaded.

Create your own application at https://www.dropbox.com/developers/app, get an access token and save it into config.py

Then all the fies in DIR_TO_MONITOR (settings in config.py) will be watched. When a new file arrivez there, a
subdirectory with date pattern will be created and file will be time prefixed and moved there. An identical structure
will be replicated and uploaded to drobox under BASE_DIR_TO_UPLOAD with same structure.

Going to use it in the directory where my survellaince camera pictures get ftp'ed so that they will get directly sorted
and uploaded to my dropbox.

The script is meant to be as lightweight as possible, and to not write too much on the same sectors, so that a
Raspberry Pi with SD memory can handle it without problems and heavy synchronizations.


Requirements:

 * (for Raspberry PI Rasbian users) sudo apt-get install python-dev python-pip
 * sudo pip install watchdog
 * sudo pip install dropbox

