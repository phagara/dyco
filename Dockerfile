FROM python:3-alpine

ARG DYCO_VERSION
ARG DYCO_UID
ARG DYCO_GID

ENV DYCO_VERSION=${DYCO_VERSION:-unknown}
ENV DYCO_UID=${DYCO_UID:-1000}
ENV DYCO_GID=${DYCO_GID:-1000}

LABEL version=${DYCO_VERSION}
LABEL description="a silly discord bot"

COPY dyco/ requirements.txt LICENSE /app/dyco/

RUN \
    apk add --no-cache --virtual .build-deps 'gcc=9.2.0-r4' 'musl-dev=1.1.24-r2' &&\
    pip install --require-hashes -r /app/dyco/requirements.txt &&\
    apk del --no-network .build-deps &&\
    addgroup -g 1000 dyco &&\
    adduser -D -u 1000 -G dyco dyco

USER dyco
ENTRYPOINT ["python3", "-m", "dyco"]
