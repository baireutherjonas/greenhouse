FROM linuxserver/mariadb

ARG DB_USER
ARG DB_NAME
ARG DB_PASSWORD

COPY init_setup.sql init_setup.sql

#CMD mysql -u ${DB_USER} --password=${DB_PASSWORD} ${DB_NAME} < init_setup.sql