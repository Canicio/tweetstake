FROM python:3.6.3
MAINTAINER Carlos Canicio Almendros<canicio7@gmail.com>

# NOTE:
# /usr/src/venv   <- project environment
# /usr/src/app    <- project code

ENV DEBIAN_FRONTEND noninteractive

# Update system
RUN apt-get -qq update --fix-missing

# Path from now
WORKDIR /usr/src/app

# Install required packages
RUN apt-get install -y python3.6-dev python3-setuptools python3-pip

# Show python version
RUN /usr/src/venv/bin/python --version

# Copy files from files_to_container to container folder
COPY . /usr/src/app
RUN ls -l

# Install app
RUN python setup.py install
