#!/bin/bash

./build.sh

if [ `docker container ps | grep war_service | wc -l` -ne 0 ]
then
    docker kill war_service 
    docker container rm war_service
fi
if [ `docker container ls | grep war_service | wc -l` -ne 0 ]
then
    docker container rm war_service
fi
docker run --name war_service -d -p 8000:8000 war_service:latest