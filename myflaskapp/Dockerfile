FROM ubuntu:20.04
ENV TZ=Europe/Moscow 
WORKDIR /project-app
COPY . .
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
    apt-get update -y && apt-get install -y --no-install-recommends \
    python3-pip build-essential \
    python3-dev default-libmysqlclient-dev \
    pkg-config \
    gunicorn && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir -r requirements.txt
WORKDIR /project-app/myflaskapp
CMD /usr/bin/gunicorn -b 0.0.0.0:80 -w 4 app:app
