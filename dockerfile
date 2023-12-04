FROM python:3.12.0-alpine

RUN apk update && apk upgrade && apk add --no-cache git

ENV DIRECTORY /APDI

WORKDIR ${DIRECTORY}

ADD blobsapdi/ blobsapdi/
ADD setup.py .
ADD requirements.txt .

RUN python -m venv venv
RUN source venv/bin/activate
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install .

ENTRYPOINT blob_server ${AUTH_SERVER_URL} -s ${BLOB_STORAGE_FOLDER}
