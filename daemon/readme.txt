TEST IT!!!

su -s
cp dir2box-daemon /etc/init.d
chmod 544 /etc/init.d/dir2box-daemon
update-rc.d dir2box-daemon defaults
cp dir2box.py /usr/local/bin
chmod 755 /usr/local/bin/dir2box.py
