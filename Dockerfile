FROM python:3.8-alpine

ARG USER=captain
ARG GROUP=titanicrew
ENV HOME /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Installing packages
# Note: We need the following pkg dependencies for psycopg2 module if we use an Alpine image.
RUN apk update && apk add postgresql-dev build-base gcc python3-dev musl-dev sudo libffi-dev openssl-dev

RUN addgroup -S $GROUP && adduser -G $GROUP -D -h $HOME $USER  \
        && mkdir -p /etc/sudoers.d \
        && echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER \
        && chmod 0440 /etc/sudoers.d/$USER


# Defining working directory and adding source code
WORKDIR /usr/src/app

USER $USER


# Install API dependencies
RUN pip3 install --no-cache-dir psycopg2
COPY requirements.txt run.py ${HOME}/
RUN pip3 install --upgrade pip --no-cache-dir -r requirements.txt

# Copy app code
COPY src ./src


CMD echo "User $(whoami) running from $PWD with permissions: $(sudo -l)"
CMD echo "Dir permissions: $(ls -la $HOME)"

# Start app
EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["/usr/src/app/run.py"]