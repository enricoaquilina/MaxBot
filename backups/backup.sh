DATABASE=maxbot
DRIVE1=maxbot_1
DRIVE2=maxbot_2
DESTINATION1=/media/p3rditus/$DRIVE1
DESTINATION2=/media/p3rditus/$DRIVE2
FILENAME=dump_`date "+%F__%H.%M.%N"`.gz
HOST=127.0.0.1
PORT=27017


#Check if backups folder exist in destinations
if [ ! -d $DESTINATION1/$DATABASE'_backups' ]; then
    mkdir $DESTINATION1/$DATABASE'_backups'/
fi

if [ ! -d $DESTINATION2/$DATABASE'_backups' ]; then
    mkdir $DESTINATION2/$DATABASE'_backups'/
fi


#Dump the contents of the db into the destination drive
mongodump --host $HOST:$PORT --db $DATABASE --gzip --out $DESTINATION1/$DATABASE'_backups'/$FILENAME

mongodump --host $HOST:$PORT --db $DATABASE --gzip --out $DESTINATION2/$DATABASE'_backups'/$FILENAME

#mongorestore -h $HOST:$PORT --gzip --db $DATABASE dump_2020-03-16_17.38.gz/maxbot



