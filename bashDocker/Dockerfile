FROM alpine

RUN apk update && apk upgrade && apk add bash

RUN ["mkdir", "/script_dir"]

RUN ["wget", "-P", "/script_dir", "https://github.com/benbrandt/cs50/blob/master/pset5/texts/dracula.txt"]

COPY ./script_1.sh /script_dir

COPY ./script_2.sh /script_dir

