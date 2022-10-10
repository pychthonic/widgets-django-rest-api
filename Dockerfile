FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /widgets

WORKDIR /widgets

ADD . /widgets/

RUN pip install -r requirements.txt

RUN python3 manage.py test