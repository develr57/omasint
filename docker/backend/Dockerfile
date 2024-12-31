FROM python:3.13-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk --no-cache add gcc musl-dev

COPY ./reqs.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r reqs.txt

#EXPOSE 8000