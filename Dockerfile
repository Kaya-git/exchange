FROM python:3.11.6

RUN mkdir /exchange_app

WORKDIR /exchange_app

COPY /requirements.txt .

RUN pip install --upgrade pip \
  && pip install -r requirements.txt --no-cache-dir

COPY . .

WORKDIR src

CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
