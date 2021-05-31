#!/bin/sh

sudo docker build -t web:latest .
sudo docker run --rm -d -p 3000:3000 web:latest