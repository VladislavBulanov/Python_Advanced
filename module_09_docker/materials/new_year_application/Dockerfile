FROM python:3.10.6

RUN mkdir /app

WORKDIR /app

COPY . /app/

RUN python -m pip install -r /app/requirements.txt

ENTRYPOINT ["python", "app.py"]
