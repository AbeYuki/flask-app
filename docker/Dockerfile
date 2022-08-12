FROM python:3.10
ENV PYTHONUNBUFFERED=1
WORKDIR /usr/src
COPY requirements.txt /code/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt