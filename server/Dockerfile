FROM python:3.12.0-bullseye

WORKDIR /app

COPY server/requirements.txt server/requirements.txt

RUN pip install -r server/requirements.txt

COPY proto/ proto/

COPY server/ server/


CMD ["python", "-m", "server.main"]