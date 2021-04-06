#!/usr/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

cp pobDNSupdate.py /usr/local/bin/
cp pobDNSupdate.service /usr/lib/systemd/system/
mkdir /etc/pobDNSupdate/
cp prefs.conf /etc/pobDNSupdate/ 
systemctl enable pobDNSupdate.service
systemctl start pobDNSupdate.service
