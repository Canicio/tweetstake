FROM python:3.6.3
MAINTAINER Carlos Canicio Almendros<canicio7@gmail.com>

ENV DEBIAN_FRONTEND noninteractive

# Update system
RUN apt-get -qq update --fix-missing

# Path from now
WORKDIR /usr/src/app

# Install required packages
RUN apt-get install -y python3-dev python3-setuptools python3-pip

# Show python version
RUN python --version

# Copy files from files_to_container to container folder
COPY . /usr/src/app
RUN chmod 777 -R .

# Install app
RUN python setup.py install
