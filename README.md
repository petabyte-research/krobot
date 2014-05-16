# KRobot

**Kleaning data for K-Monitors ahalo!**

A small web application to perform some of the data cleaning done by
K-Monitor when they import new data.

If you want to see it in action (not much to see there) Krobot lives on
http://krobot.herokuapp.com

## Contributing

You can make KRobot better:

* Look at it and file issues if you encounter an error or not intuitive
  behavior
* File an issue for features you'd love to have
* Create nicer design!
* Write some code

## Developing

Since KRobot is so simple I decided to go with web.py and jinja2 as a
framework for developing it. 

Install locally:
```
# create a virtualenv
virtualenv2 venv
# activate it
source venv/bin/activate
# install dependencies
pip install -r requirements.dev.txt
# run it
honcho start
```

Open your browser to http://127.0.0.1:5000 and you should have a running
instance.
