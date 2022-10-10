FROM python:3.10

# ENV VIRTUAL_ENV=/opt/venv

# RUN python3 -m venv $VIRTUAL_ENV

# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

ENV PYTHONUNBUFFERED 1

# ENV PATH=/venv/bin:$PATH

RUN mkdir /widgets

WORKDIR /widgets

ADD . /widgets/

RUN pip install -r requirements.txt

RUN python3 manage.py test