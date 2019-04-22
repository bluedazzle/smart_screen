FROM python:2.7

WORKDIR /code

ADD . /code

RUN ["apt-get", "update", "-y"]
RUN ["apt-get", "install", "-y", "libfbclient2"]
RUN ["pip", "install", "-r", "requirements.txt"]
RUN ["pip", "install", "django==1.8.0"]
RUN ["pip", "install", "celery==4.1.0"]

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]

