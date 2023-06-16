FROM python:3.10.6

RUN mkdir /app

WORKDIR /app

COPY requirements.txt /app/
RUN python -m pip install -r /app/requirements.txt

COPY . /app/

ENTRYPOINT ["python", "app.py"]
