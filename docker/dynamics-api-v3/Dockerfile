FROM python:3.10
ARG GITHUB_TOKEN
ENV PYTHONUNBUFFERED 1
RUN apt update -y && apt upgrade -y
RUN apt install -y supervisor
RUN groupadd apps
RUN mkdir /var/apps /var/apps/static
RUN useradd -g apps -s /bin/bash -d /var/apps apps
WORKDIR /var/apps
RUN git clone  --branch files_ws https://GITHUB_TOKEN@github.com/fmresolving/dynamics-api-v3.git
RUN pip install pipenv
WORKDIR /var/apps/dynamics-api-v3
RUN mkdir /var/www
RUN pipenv install
RUN pipenv run /var/apps/dynamics-api-v3/manage.py collectstatic --noinput
EXPOSE 8000
ENTRYPOINT pipenv run runserver