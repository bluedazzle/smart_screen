FROM python:3.6

WORKDIR /code

ADD . /code

RUN ["apt-get", "update", "-y"]
RUN ["apt-get", "install", "-y", "libfbclient2"]
RUN ["pip", "install", "-r", "requirements.txt"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

