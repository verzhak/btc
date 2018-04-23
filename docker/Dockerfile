
FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /cc
WORKDIR /cc
ADD requirements.txt /cc
RUN pip install -r requirements.txt
COPY init.py /init.py
COPY init.sh /init.sh
RUN chmod +x /init.sh

