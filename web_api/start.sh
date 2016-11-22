#!/bin/bash

echo Sleeping for 10 seconds
sleep 10
echo Sleeping for 10 seconds
sleep 10
python manage.py runserver 0.0.0.0:8888 --verbosity 3
