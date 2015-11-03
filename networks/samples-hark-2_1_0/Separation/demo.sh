#!/bin/sh

export BIN=.
export DATA=../data/MultiSpeech.wav
export DEVICE=plughw:0,0
export LOC=../config/kinect_tf.zip
export SEP=../config/kinect_tf.zip

if [ "$2" = "HRLE" ]
then
    export HRLE="HRLE"
else
    export HRLE=""
fi


if [ "$1" = "offline" ]
then
    echo "Offline mode"
    echo batchflow ${BIN}/demoOffline${HRLE}.n ${DATA} ${SEP} ${LOC} sep_files/offline${HRLE}_
    batchflow ${BIN}/demoOffline${HRLE}.n ${DATA} ${SEP} ${LOC} sep_files/offline${HRLE}_
elif [ "$1" = "online" ]
then
    echo "Online mode"
    echo batchflow ${BIN}/demoOnline${HRLE}.n ${DEVICE} ${SEP} ${LOC} sep_files/online${HRLE}_
    batchflow ${BIN}/demoOnline${HRLE}.n ${DEVICE} ${SEP} ${LOC} sep_files/online${HRLE}_
else
    echo "usage: sh demo.sh [online|offline] [HRLE]"
    echo "   online : run from microphone"
    echo "   offline: run from wave file"
    echo "   HRLE   : if exists, use HRLE. if not exists, do not use HRLE"
fi
