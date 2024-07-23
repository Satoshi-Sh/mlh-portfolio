# FROM quay.io/centos/centos:stream9
# RUN dnf install -y python3.9 python3-pip image size 313MB

# Use smaller image size to make it faster  image sisze 193MB
FROM python:3.9-slim-buster

WORKDIR /mlh-portfolio

COPY requirements.txt .

# split this for the efficiency COPY . . 
# if requirements.txt is not updated, caching helps us to skilp the pip install step

RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask","run","--host=0.0.0.0"]

EXPOSE 5000