#!/usr/bin/bash
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [ "$1" = "" ]
then
    cp pobDNSupdate.py /usr/local/bin/
    chmod +x /usr/local/bin/pobDNSupdate.py
    cp pobDNSupdate.service /usr/lib/systemd/system/
    cp pobDNSupdate.timer /usr/lib/systemd/system/
    mkdir /etc/pobDNSupdate/
    cp prefs.conf /etc/pobDNSupdate/ 
    systemctl enable pobDNSupdate.service
    systemctl enable pobDNSupdate.timer
    systemctl start pobDNSupdate.service
    systemctl start pobDNSupdate.timer
fi


if [ "$1" = "uninstall" ]
then
        echo "Remove all ..."
        systemctl disable pobDNSupdate.timer
        systemctl disable pobDNSupdate.service
        systemctl stop pobDNSupdate.timer
        systemctl stop pobDNSupdate.service
        rm /usr/local/bin/pobDNSupdate.py
        rm /usr/lib/systemd/system/pobDNSupdate.*
        
fi
