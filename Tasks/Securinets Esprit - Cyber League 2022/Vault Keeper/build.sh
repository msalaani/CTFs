#!/bin/bash
docker rm -f vault
docker build --tag=vault . && \
docker run -p 10006:1337 --restart=on-failure --name=vault --detach vault
