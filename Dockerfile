FROM python:3.8-slim-buster

# enviorment
ENV PYHTONDONTWRITEBYTECODE=1
ENV PYHTONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY ./core/ /app

