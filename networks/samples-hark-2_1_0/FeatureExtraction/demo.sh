#!/bin/sh

export BIN=.
export DATA=../data

FrameLength=512    # (Sample)
FrameShift=160     # (Sample)
SamplingRate=16000 # (Hz)
NumFilterBank=13   # 


case $1 in
    "1") # MSLS(13)
         echo "MSLS"; 
         ${BIN}/demo1.n ${DATA}/sample.wav ${FrameLength} ${FrameShift} ${SamplingRate} ${NumFilterBank};;
    "2") # MSLS(13) + delta MSLS(13)
         echo "MSLS + DeltaMSLS";
         ${BIN}/demo2.n ${DATA}/sample.wav ${FrameLength} ${FrameShift} ${SamplingRate} ${NumFilterBank};; 
    "3") # MALS(13) + log Energy(1) 
         echo "MSLS + Power"; 
         ${BIN}/demo3.n ${DATA}/sample.wav ${FrameLength} ${FrameShift} ${SamplingRate} ${NumFilterBank};; 
    "4") # MALS(13) + log Energy(1)+ delta MSLS(13)) + delta log Energy(1) 
         echo "MSLS + Delta MSLS + Power + Delta Power";
         ${BIN}/demo4.n ${DATA}/sample.wav ${FrameLength} ${FrameShift} ${SamplingRate} ${NumFilterBank} `expr ${NumFilterBank} + 1`;; 
    "5") echo "MSLS + Delta MSLS + Delta Power";
         ${BIN}/demo5.n ${DATA}/sample.wav ${FrameLength} ${FrameShift} ${SamplingRate} ${NumFilterBank} `expr ${NumFilterBank} + 1`;; 
    "6") echo "MSLS + Delta MSLS + Delta Power with PreEmphasis";
         ${BIN}/demo6.n ${DATA}/sample.wav ${FrameLength} ${FrameShift} ${SamplingRate} ${NumFilterBank} `expr ${NumFilterBank} + 1`;; 
*) echo "usage: demo.sh [1-6]" ;;
esac
find . -name "*.sw" -exec sox -r ${SamplingRate} -c 1 --bits 16 -s {} {}.wav \;
rm -f *.sw
