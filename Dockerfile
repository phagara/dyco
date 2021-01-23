FROM python:3-alpine

ARG DYCO_VERSION
ARG DYCO_UID
ARG DYCO_GID

ENV DYCO_VERSION=${DYCO_VERSION:-unknown}
ENV DYCO_UID=${DYCO_UID:-1000}
ENV DYCO_GID=${DYCO_GID:-1000}

LABEL version=${DYCO_VERSION}
LABEL description="a silly discord bot"

# Even though /app will be removed from the final image,
# it will still be present in the layers, wasting space.
# Staged builds won't help here, as "COPY --from" has the
# same issue. We don't want to pull the dyco package from
# a pypi, as that will break local dev builds. Squashing
# the image at build time would help, but that feature is
# still experimental. That's containers in TYOOL 2020.
COPY dyco /app/dyco/
COPY LICENSE MANIFEST.in requirements.txt setup.py /app/
WORKDIR /app

RUN \
    pip install --no-cache-dir wheel==0.36.2 &&\
    apk add --no-cache --virtual .build-deps 'gcc=9.3.0-r2' 'musl-dev=1.1.24-r10' &&\
    pip install --no-cache-dir -r /app/requirements.txt &&\
    apk del --no-network .build-deps &&\
    pip install --no-cache-dir --no-index --no-deps . &&\
    rm -rf /app &&\
    addgroup -g 1000 dyco &&\
    adduser -D -u 1000 -G dyco dyco

USER dyco
WORKDIR /
ENTRYPOINT ["dyco"]
