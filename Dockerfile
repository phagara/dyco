FROM python:3-alpine

ARG DYCO_VERSION=unknown
ENV DYCO_VERSION=$DYCO_VERSION

COPY . /app
WORKDIR /app

RUN \
    apk add --no-cache --virtual .build-deps=20200501.164132 gcc=9.2.0-r4 musl-dev=1.1.24-r2 &&\
    pip install -r requirements.txt &&\
    apk del .build-deps gcc musl-dev

CMD ["python3", "-m", "dyco"]