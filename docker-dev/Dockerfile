
###############################################################################
# Software:         CWL-Airflow
# Software Version: always latest commit from master
# Image Version:    latest
# Description:      CWL-Airflow image for LocalExecutor and MYSQL backend
#                   using default Python 3.8
# Website:          https://cwl-airflow.readthedocs.io/en/latest/
# Provides:         Airflow, CWL-Airflow, cwltool
# Base Image:       ubuntu:20.04
# Build Cmd:        docker build --rm -t biowardrobe2/cwl-airflow:latest .
###############################################################################


FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /opt/cwl-airflow

RUN apt-get update && \
    # installing dependencies (including docker dependencies)
    apt-get install -y python3-dev python3-pip nodejs gcc git wget curl \
                       libmysqlclient-dev mysql-client apt-transport-https \
                       ca-certificates gnupg-agent software-properties-common && \
    # installing docker-ce-cli
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get -y install docker-ce-cli unzip
#     # installing cwl-airflow
COPY ./packaging/docker_compose/local_executor/cwl_airflow/scripts/start_webserver.sh /usr/local/bin/start_webserver.sh
COPY ./packaging/docker_compose/local_executor/cwl_airflow/scripts/start_scheduler.sh /usr/local/bin/start_scheduler.sh
COPY ./packaging/docker_compose/local_executor/cwl_airflow/scripts/start_apiserver.sh /usr/local/bin/start_apiserver.sh
COPY ./cwl_airflow ./src/cwl_airflow
COPY  setup.py setup.cfg MANIFEST.in README.md  ./src/
COPY ./packaging/constraints/constraints-3.8.txt ./src

RUN    pip3 install -U pip                                                                  && \
    cd src                                                                                  && \
    pip3 install ".[mysql]" --constraint ./constraints-3.8.txt                              && \
    # cleaning up
    apt-get clean                                                                           && \
    apt-get purge                                                                           && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*                          && \
    strip /usr/local/bin/*; true
