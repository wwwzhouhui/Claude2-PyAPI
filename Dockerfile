FROM python:3.10-slim


# 非必要步骤，更换pip源
RUN echo '[global]' > /etc/pip.conf && \
    echo 'index-url = https://mirrors.aliyun.com/pypi/simple/' >> /etc/pip.conf && \
    echo 'trusted-host = mirrors.aliyun.com' >> /etc/pip.conf


# 进入工作路径
WORKDIR /home/claude

# 安装大部分依赖，利用Docker缓存加速以后的构建
COPY requirements.txt ./
COPY .  /home/claude/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 启动
CMD ["python", "-u", "claude_flask.py"]