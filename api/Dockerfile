FROM python:3.10-alpine AS builder
LABEL authors="daniel.c.ferreira"

WORKDIR /

COPY . ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

ENTRYPOINT ["python3"]
CMD ["app.py"]
