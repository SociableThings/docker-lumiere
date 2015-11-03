#!/bin/bash

echo "" > /var/log/hark.log

/usr/bin/supervisord -c /root/supervisord.conf

# start a shell
tail -f /var/log/hark.log
