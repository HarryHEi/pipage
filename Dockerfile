# 该镜像只安装必要的运行环境，不会拷贝源码。
# 使用docker-compose将容器绑定本地数据卷。

FROM python:3.7

WORKDIR /opt/pipages
COPY requirements.txt /opt/pipages
RUN pip install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

ENTRYPOINT ["/bin/bash"]
