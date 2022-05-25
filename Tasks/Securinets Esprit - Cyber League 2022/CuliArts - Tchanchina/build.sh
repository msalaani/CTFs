#!/bin/bash
docker rm -f tchanchina
docker build --tag=tchanchina . && \
docker run -p 10010:1337 --restart=on-failure --name=tchanchina --detach tchanchina
