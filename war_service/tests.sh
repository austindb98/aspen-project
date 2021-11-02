#!/bin/bash

echo 'yes' | python manage.py flush
python manage.py runserver &
pid=$!
sleep 3
python tests.py
kill $pid
