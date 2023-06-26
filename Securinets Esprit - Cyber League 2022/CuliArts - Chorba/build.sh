#!/bin/bash
docker rm -f chorba
docker rmi -f chorba
docker build --tag=chorba . && \
docker run -p 10008:1337 --restart=on-failure --name=chorba --detach chorba
