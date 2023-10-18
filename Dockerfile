FROM python:3.11.6
WORKDIR /src
COPY /requirements.txt .
RUN pip install --upgrade pip \
  && pip install -r requirements.txt --no-cache-dir
COPY .. .
CMD ["python", "src/main.py"]
