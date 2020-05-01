FROM python:3-alpine

ARG DYCO_VERSION=unknown
ENV DYCO_VERSION=$DYCO_VERSION

COPY . /app
WORKDIR /app

RUN \
    apk add --no-cache --virtual .build-deps gcc musl-dev &&\
    pip install -r requirements.txt &&\
    apk del .build-deps gcc musl-dev

CMD ["python3", "-m", "dyco"]