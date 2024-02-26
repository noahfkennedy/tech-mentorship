FROM python:3.8-slim

RUN apt-get update -yqq && \
    apt-get upgrade -yqq &&  \
    apt-get install -yqq --no-install-recommends \
    build-essential \
    libssl-dev \
    libffi-dev \
    cargo \
    curl \
    git

# Downloading gcloud package
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz

# Installing the package
RUN mkdir -p /usr/local/gcloud \
    && tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz \
    && /usr/local/gcloud/google-cloud-sdk/install.sh

# Adding the package path to local
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

WORKDIR /
RUN pip install -U pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY dbt/ dbt/
COPY docker/entrypoint.py entrypoint.py

WORKDIR /dbt
ENTRYPOINT ["python3", "/entrypoint.py"]
