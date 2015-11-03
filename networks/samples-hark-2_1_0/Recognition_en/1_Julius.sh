#!/bin/bash

echo "After you see the message \"waiting client at 10500\","
echo "press enter again [Press Enter]"
read Dmy

exec julius_mft -C julius.jconf -module &

read Dmy
exec python receive.py | tee result.txt
