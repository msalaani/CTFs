#!/bin/bash
docker rm -f ccybercup
docker rmi -f ccybercup
docker build --tag=ccybercup . && \
docker run -p 10204:1337 --restart=on-failure --name=ccybercup --detach ccybercup
