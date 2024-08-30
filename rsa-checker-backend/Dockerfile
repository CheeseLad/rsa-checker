FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "127.0.0.1:5000", "wsgi:app", "-w", "4"]