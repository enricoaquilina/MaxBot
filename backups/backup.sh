#!/bin/bash

HOST=127.0.0.1
PORT=27017
DRIVE=maxbot_1
FILENAME=dump_`date "+%F__%H.%M.%N"`.gz
DESTINATION=/media/p3rditus/$DRIVE
DATABASE=maxbot

#check if backups folder exists 

if [ ! -d $DESTINATION/$DATABASE'_backups' ]; then
    mkdir $DESTINATION/$DATABASE'_backups'/
fi

#Dump the contents of the db into the destination drive
mongodump --host $HOST:$PORT --db $DATABASE --gzip --out $DESTINATION/$DATABASE'_backups'/$FILENAME  #$SOURCE/$FILENAME

#mongorestore -h $HOST:$PORT --gzip --db $DATABASE dump_2020-03-16_17.38.gz/maxbot
 


