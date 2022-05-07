# for debian 11 bullseye
FROM python:3.9-slim-bullseye

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock

WORKDIR /app
RUN apt-get update &&\
    rm -rf ~/.cache &&\
    apt-get clean all &&\
    apt-get install -y\
    vim

RUN apt-get install -y apt-transport-https ca-certificates gnupg curl &&\
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | \
    tee -a /etc/apt/sources.list.d/google-cloud-sdk.list  &&\
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - &&\
    apt-get update && apt-get install -y google-cloud-sdk


RUN pip install --upgrade pip &&\
    pip install poetry &&\
    poetry config virtualenvs.create false --local &&\
    poetry run pip install --upgrade pip setuptools==60.2.0  &&\
    poetry install --no-dev &&\
    rm -rf ~/.cache # FIXME: setuptools 60.3.0 has some bugs. This is a workaround https://github.com/pypa/setuptools/issues/3002

WORKDIR /
COPY ./run_server.py /app/run_server.py
COPY ./ayeaye /app/ayeaye

COPY ./test /app/test
COPY README.md /app/README.md
RUN mkdir /app/result

WORKDIR /app
CMD ["tail", "-f", "/dev/null"]
VOLUME "/app"
