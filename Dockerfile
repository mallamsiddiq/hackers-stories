

FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN mkdir /seedtest


WORKDIR /seedtest


ADD . /seedtest/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn seedtest.wsgi:application --bind 0.0.0.0:$PORT