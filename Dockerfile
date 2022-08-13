FROM python:3.10
WORKDIR /usr/src/
COPY . ./
RUN pip install --upgrade pip \
    && pip install -r app/requirements.txt