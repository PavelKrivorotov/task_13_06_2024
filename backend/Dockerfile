# syntax=docker/dockerfile:1

FROM python:3.10-alpine3.15
WORKDIR /app/

# Install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r ./requirements.txt

# Add source code (app)
COPY ./src /app/src

# Add run-app script
COPY ./run-app.sh /app/run-app.sh
RUN chmod u+x ./run-app.sh

# Add run-tests script
COPY ./run-tests.sh /app/run-tests.sh
RUN chmod u+x ./run-tests.sh

# Add environments
COPY ./.docker.env /app/.env

# Run
CMD [ "/bin/sh", "./run-app.sh" ]
