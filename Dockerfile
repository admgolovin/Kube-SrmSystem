FROM centos:latest
Maintainer Stark
COPY . /Project/
RUN yum upgrade -y --nogpgcheck
RUN yum update -y --nogpgcheck
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm --nogpgcheck
RUN yum install -y python36u python36u-libs python36u-devel python36u-pip --nogpgcheck
RUN python3.6 -m pip install flask
RUN python3.6 -m pip install -r /Project/requirements.text
RUN export LC_ALL=en_US.utf-8
RUN export LANG=en_US.utf-8
RUN export FLASK_APP=/Project/app/app.py
CMD ["/bin/bash", "echo 'Done!'"]

