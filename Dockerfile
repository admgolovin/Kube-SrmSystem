FROM centos:latest
Maintainer Stark
COPY /DB /
RUN rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
RUN yum upgrade
RUN yum update
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm --nogpgcheck
RUN yum install -y python36u python36u-libs python36u-devel python36u-pip --nogpgcheck


