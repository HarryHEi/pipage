#!/bin/bash

# 创建镜像、启动服务。

docker build -t pipages .
docker-compose up -d
