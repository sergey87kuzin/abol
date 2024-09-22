ARG BASE_IMAGE=python:3.12
FROM $BASE_IMAGE

# system update & package install
RUN apt-get -y update

COPY . .
WORKDIR .

# pip & requirements
RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install -r requirements.txt

ENTRYPOINT [ "bin/bash", "entrypoint.sh" ]