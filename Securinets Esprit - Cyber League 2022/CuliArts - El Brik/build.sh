#!/bin/bash
docker rm -f elbrik
docker rmi -f elbrik
docker build --tag=elbrik . && \
docker run -p 10007:1337 --restart=on-failure --name=elbrik --detach elbrik
