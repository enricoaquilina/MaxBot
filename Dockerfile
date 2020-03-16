# syntax = docker/dockerfile:experimental

# Some housekeeping to get the app locally in the container
FROM alpine as start
RUN apk add --no-cache openssh-client git
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
#RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

VOLUME ["/test/db"]
WORKDIR /test

#RUN --mount=type=ssh git clone git@github.com:enricoaquilina/MaxBot.git MaxBot

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#---------------------$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$----------------------



# Starting the mongo installation now
FROM ubuntu

MAINTAINER perieratutopia@gmail.com
#ENV DEBIAN_FRONTEND=noninteractive

RUN \
  apt-get update && apt-get install -y gnupg2 && \
  apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4 && \
  echo 'deb [arch=amd64,arm64] http://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/4.0 multiverse' | tee /etc/apt/sources.list.d/mongodb-org-4.0.list && \
  apt-get update && apt-get install -y \
  mongodb-org
#  git \
#  openssh-client \
#  python-pip \
#  python-dev \
#  --no-install-recommends apt-utils \
#  python-setuptools
#  pip install markupsafe dopy boto linode-python pyrax



#VOLUME ["/data/db"]
#WORKDIR /data


EXPOSE 27017
CMD ["mongod"]

#ENV HOME /media/p3rditus/maxbot_1
#ENV HOME /root
#RUN ssh-keygen -f /root/.ssh/id_rsa -q -N ""

