FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN chmod +x run_backend.sh

EXPOSE 5000

CMD ["./run_backend.sh"]