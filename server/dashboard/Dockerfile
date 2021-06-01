FROM debian:stable-slim

ENV TZ=Europe/Berlin
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update
RUN apt-get install -y python3 python3-pip

WORKDIR /usr/src/app

COPY req.txt ./

RUN apt-get install -y libmariadb-dev

RUN pip3 install --no-cache-dir -r req.txt

COPY . .

CMD [ "python3", "-u", "./server.py" ]
