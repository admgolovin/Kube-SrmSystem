FROM centos:latest
MAINTAINER Anton Golovin
COPY . /mydir/
RUN yum update
RUN yum upgrade
RUN yum install epel-release -y
RUN yum install https://centos7.iuscommunity.org/ius-release.rpm -y
RUN yum install python36 -y
RUN yum install python36u-pip -y
RUN pip3.6 install --upgrade pip
RUN pip3.6 install --upgrade pip setuptools
RUN pip3.6 install Flask
RUN cd /mydir/db/
RUN export FLASK_APP=dbservice.py
RUN localedef -c -f UTF-8 -i en_US en_US.UTF-8
RUN export LC_ALL=en_US.UTF-8

 


