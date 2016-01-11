#!/bin/bash
PORT=5000
if [ ! -z "$1" ]; then
	PORT=$1
fi
if [ $(ps ax | grep "service.py[ ]$PORT" | wc -l) -eq 1 ]; then
	PID=$(ps ax | grep "service.py[ ]$PORT" | cut -d" " -f1)
	echo "Killing KRobot with PID $PID"
	kill $PID
fi
