FROM ubuntu:22.04

ENV NOVATUBE_HOME="/novatube"

RUN apt update && apt install -y \
    python3 python3-pip python3-dev

COPY devops/novatube "$NOVATUBE_HOME"
WORKDIR "$NOVATUBE_HOME"

RUN pip3 install .

ENTRYPOINT ["novatube"]
