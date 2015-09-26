#!/bin/bash
# Program:
#       This program is to start mongo db and restful server codee 
# History:
# 2013/07/29	Yao Nien, Yang	First release
# logfile: mongo.log ; mongoerror.log ; server_init.log.txt

echo -e "Kill all the related processes"


ps -ef | grep mongo|awk '{print $2}'| xargs -i kill {}
ps -ef | grep restserver.py|awk '{print $2}'| xargs -i kill {}



echo -e "Start MongoDB"

nohup /home/mongodb-linux-x86_64-2.4.4/bin/mongod --dbpath /home/mongodata/db/ > /home/backend/log/MongoDB/mongo.log > /home/backend/log/MongoDB/mongoerror.log &
echo -e "Wait 5 seconds until MongoDB starts"
sleep 5

echo -e "Start REST server"
nohup python /home/backend/restserver.py &>  /home/backend/log/REST/server_init.log &

echo -e "Done , run ps aux or tail to check the status of server!"

echo -e "Search process from PS and show their status "

sleep 5


if pgrep mongod >/dev/null 2>&1
then
    echo "MongoDB Running!"
else
    echo "MongoDB Stopped!"
fi

sleep 10 

if ps -ef | grep restserver.py  >/dev/null 2>&1
then
    echo "REST server Running!"
else
    echo "REST Stopped!"
fi


