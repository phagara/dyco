FROM python:3.9-slim as builder

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

RUN useradd -mU dyco
RUN chown -R dyco:dyco /app
RUN pip install --no-cache-dir -r /app/requirements.txt

USER dyco
RUN pip install --user --no-cache-dir --no-index --editable /app

ENTRYPOINT ["/home/dyco/.local/bin/dyco"]
