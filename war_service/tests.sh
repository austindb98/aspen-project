#!/bin/bash

./run.sh
docker container exec -it war_service python manage.py flush --noinput
sleep 2
python tests.py
docker logs war_service