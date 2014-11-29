dir2box
=======

A simple python daemon for uploading a filesystem directory to dropbox. Developed in order to upload files from my home 
surveillance ftp server (a RaspberryPi :-) ) as soon as files are uploaded.

Python client based on: http://stackoverflow.com/questions/23894221/upload-file-to-my-dropbox-from-python-script
https://www.dropbox.com/developers/blog/94/generate-an-access-token-for-your-own-account
and https://www.dropbox.com/developers/core/start/python

Requirements:

 * (for Raspberry PI Rasbian users) sudo apt-get install python-dev python-pip
 * sudo pip install watchdog
 * sudo pip install dropbox

