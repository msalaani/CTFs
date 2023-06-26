#!/bin/bash
docker rm -f elbeyet
docker build --tag=elbeyet . && \
docker run -p 10009:1337 --restart=on-failure --name=elbeyet --detach elbeyet
