###########
# BUILDER #
###########

FROM python:3.9-slim-bullseye as builder
# set work directory
WORKDIR /usr/src/app
# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

#install packages
RUN apt-get update
RUN apt-get -y install netcat-traditional gcc python3-dev musl-dev
# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########
FROM python:3.9-slim-bullseye

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN groupadd app && useradd -g app -s /bin/sh app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update
RUN apt-get -y install netcat-traditional
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh
RUN chmod +x  $APP_HOME/entrypoint.sh

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]