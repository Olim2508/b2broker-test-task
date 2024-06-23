# pull official base image
FROM python:3.12-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV HOME=/usr/src/backend

# set work directory
WORKDIR $HOME

# Install dependencies
RUN apk add --update --no-cache mariadb-dev gcc python3-dev musl-dev \
    && pip install --upgrade pip setuptools

COPY ./backend/requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

# copy entrypoint.sh
COPY ./backend/entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/backend/entrypoint.sh
RUN chmod +x /usr/src/backend/entrypoint.sh

# copy project
COPY ./backend $HOME

# run entrypoint.sh
ENTRYPOINT ["/usr/src/backend/entrypoint.sh"]
