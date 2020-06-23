#!/bin/bash

# 创建镜像、启动服务。

docker build -t pipage .
docker-compose up -d
