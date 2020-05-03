FROM python:3-alpine

ARG DYCO_VERSION
ARG DYCO_UID
ARG DYCO_GID

ENV DYCO_VERSION=${DYCO_VERSION:-unknown}
ENV DYCO_UID=${DYCO_UID:-1000}
ENV DYCO_GID=${DYCO_GID:-1000}

LABEL version=${DYCO_VERSION}
LABEL description="a silly discord bot"

COPY dyco /app/dyco/
COPY LICENSE MANIFEST.in requirements.txt setup.py /app/
WORKDIR /app

RUN \
    apk add --no-cache --virtual .build-deps 'gcc=9.2.0-r4' 'musl-dev=1.1.24-r2' &&\
    pip install --no-cache --require-hashes -r /app/requirements.txt &&\
    apk del --no-network .build-deps &&\
    pip install --no-cache --no-index --no-deps . &&\
    rm -rf /app &&\
    addgroup -g 1000 dyco &&\
    adduser -D -u 1000 -G dyco dyco

USER dyco
WORKDIR /
ENTRYPOINT ["dyco"]
