# syntax = docker/dockerfile:experimental

# Some housekeeping to get the app locally in the container
FROM alpine
RUN apk add --no-cache openssh-client git
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
#RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts

VOLUME ["/data/db"]
WORKDIR /data
#WORKDIR /media/p3rditus/maxbot_1
RUN --mount=type=ssh git clone git@github.com:enricoaquilina/MaxBot.git MaxBot

