FROM python:3.12.0-alpine

RUN apk update && apk upgrade && apk add --no-cache git

RUN mkdir /APDI

WORKDIR /APDI

ADD blobsapdi/ blobsapdi/
ADD setup.py .
ADD requirements.txt .
ADD pyblob.db .

RUN python -m venv venv
RUN source venv/bin/activate
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install .

RUN chown -R 1000:1000 /APDI

ENTRYPOINT blob_server http://auth-svc/api/ -s storage
