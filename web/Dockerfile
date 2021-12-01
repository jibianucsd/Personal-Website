FROM  python:3.8
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install libev-dev -y

COPY ./src/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

WORKDIR /app

EXPOSE 6000
CMD python server.py