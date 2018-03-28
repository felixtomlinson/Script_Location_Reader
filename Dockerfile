FROM ubuntu:16.04
MAINTAINER Jonathan Kerr <jonathan@apply4.com>
RUN useradd -m script-basher
RUN apt-get update && apt-get install -y \
apt-utils python3 python-dev python3-dev \
   build-essential libssl-dev libffi-dev \
   libxml2-dev libxslt1-dev zlib1g-dev \
   python-pip python-virtualenv \
   antiword unrtf poppler-utils pstotext tesseract-ocr \
   flac ffmpeg lame libmad0 libsox-fmt-mp3 sox \
   libjpeg-dev swig libpulse-dev
RUN apt-get install -y swig
COPY requirements.txt requirements.txt
RUN virtualenv -p python3 venv
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN . venv/bin/activate
WORKDIR /home/script-basher
COPY app app
COPY migrations migrations
COPY config.py main.py Script_reader.py ./
ENV FLASK_APP main.py
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
