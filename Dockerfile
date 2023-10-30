FROM python:3.11.6

RUN mkdir /exchange_app

WORKDIR /exchange_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR src

RUN chmod a+x docker/*.sh

# RUN alembic upgrade head

# CMD gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
