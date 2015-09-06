#!/bin/bash

echo "" > /var/log/hark.log

# start up supervisord, all daemons should launched by supervisord.
/usr/bin/supervisord -c /root/supervisord.conf

# start a shell
tail -f /var/log/hark.log
