FROM python:3.12.0-bullseye

WORKDIR /app

COPY client/requirements.txt client/requirements.txt

RUN pip install -r client/requirements.txt

COPY proto/ proto/

COPY client/ client/

CMD ["python", "-m", "client.main"]