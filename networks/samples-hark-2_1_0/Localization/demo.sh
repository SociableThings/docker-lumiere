#!/bin/sh

export BIN=.
export DATA=../data/MultiSpeech.wav
export DEVICE=plughw:1,0
export CONF=../config/kinect_tf.zip

#for deg in 000 090 180 270; do
  #echo Display sounds from ${deg} degrees.
  #${BIN}/demoOffline8ch.n ${DATA}/f101_${deg}.wav ${CONF}/music.dat Localization_${deg}.txt
#done

if [ "$1" = "offline" ]
then
    echo "Offline mode"
    echo ${BIN}/demoOffline.n ${DATA} ${CONF} Localization.txt \> log.txt
    ${BIN}/demoOffline.n ${DATA} ${CONF} Localization.txt > log.txt
elif [ "$1" = "online" ]
then
    echo "Online mode"
    echo ${BIN}/demoOnline.n ${DEVICE} ${CONF} Localization.txt \> log.txt
    ${BIN}/demoOnline.n ${DEVICE} ${CONF} Localization.txt > log.txt
else
    echo "usage: sh demo.sh [online|offline]"
fi
