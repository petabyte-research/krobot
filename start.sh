#!/bin/bash
PORT=5000
if [ ! -z "$1" ]; then
	PORT=$1
fi
echo "Starting KRobot on port $PORT"
python service.py $PORT &>krobot.log &
PID=$!
echo "PID is $PID, use 'stop.sh $PORT' to kill it"
