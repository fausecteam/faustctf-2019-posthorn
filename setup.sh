#!/bin/sh

sudo -u postgres createuser -l posthorn
sudo -u postgres createdb -O posthorn posthorn
sudo -u posthorn psql -f /srv/posthorn/schema.sql
adduser www-data posthorn

touch /srv/posthorn/setup
