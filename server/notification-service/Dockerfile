#FROM balenalib/raspberry-pi-openjdk:8-stretch
FROM openjdk:8
 
WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y python3 python3-pip

COPY req.txt ./
RUN pip3 install -r req.txt

COPY . .

CMD [ "python3", "-u", "./notification-service.py" ]
