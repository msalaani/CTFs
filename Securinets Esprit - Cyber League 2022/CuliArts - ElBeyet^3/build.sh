#!/bin/bash
docker rm -f beyet3
docker build --tag=beyet3 . && \
docker run -p 10011:1337 --restart=on-failure --name=beyet3 --detach beyet3
