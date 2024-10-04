FROM python:3.11.8-alpine

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["prefect", "agent", "start", "--work-pool", "main"]
