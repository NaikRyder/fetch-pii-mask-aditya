FROM ubuntu:latest
LABEL authors="adityavnaik"

ENTRYPOINT ["top", "-b"]