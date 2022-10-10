FROM python:3.10

ENV PYTHONUNBUFFERED 1

# For running & testing docker container locally.
# Obviously not for production software:
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENV DJANGO_SUPERUSER_EMAIL=example@example.com

RUN mkdir /widgets

WORKDIR /widgets

ADD . /widgets/

RUN pip install -r requirements.txt

RUN python3 manage.py test