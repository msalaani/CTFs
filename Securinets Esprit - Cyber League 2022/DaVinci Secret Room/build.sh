#!/bin/bash
docker rm -f room
docker build --tag=room . && \
docker run -p 10005:1337 --restart=on-failure --name=room --detach room
