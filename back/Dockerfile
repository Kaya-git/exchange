FROM python:3.11.6

RUN mkdir /backend

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR src
