FROM ubuntu:20.04

COPY . /project

RUN ln -snf /usr/share/zoneinfo/Europe\/Moscow /etc/localtime \
&& echo "Europe/Moscow" > /etc/timezone \
&& apt update \
&& apt install -y --no-install-recommends python3-pip build-essential \
python3-dev default-libmysqlclient-dev \
pkg-config \
gunicorn \
&& rm -rf /var/cache/apt/* \
&& apt autoremove \
&& mkdir -p /project \
&& pip3 install -r /project/requirements.txt --no-cache-dir

# Устанавливаем папку с wsgi приложением в качестве рабочей директории
WORKDIR /project/app

# Задаем команду для запуска
#CMD /usr/bin/gunicorn -b 0.0.0.0:8000 -w 4 app:app
CMD flask run -p 8000 -h 0.0.0.0
