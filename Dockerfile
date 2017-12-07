FROM miseyu/docker-ubuntu16-python3.6
MAINTAINER Carlos Canicio Almendros<canicio7@gmail.com>

# NOTE:
# /usr/src/app    <- project code

ENV DEBIAN_FRONTEND noninteractive

# Update system
RUN apt-get -qq update --fix-missing

# Path from now
WORKDIR /usr/src/app

# Install required packages
RUN apt-get install -y python3.6-dev python3-setuptools python3-pip

# Copy project to container folder
COPY . /usr/src/app

# Install app
RUN python setup.py install
