FROM ubuntu:16.04
MAINTAINER Jonathan Kerr <jonathan@apply4.com>
RUN apt-get update && apt-get install -y \
apt-utils python3 python-dev python3-dev \
   build-essential libssl-dev libffi-dev \
   libxml2-dev libxslt1-dev zlib1g-dev \
   python-pip python-virtualenv \
   antiword unrtf poppler-utils pstotext tesseract-ocr \
   flac ffmpeg lame libmad0 libsox-fmt-mp3 sox \
   libjpeg-dev swig libpulse-dev
RUN apt-get install -y swig
#CMD ["curl https://raw.githubusercontent.com/OriHoch/textract/fake-pocketsphinx-for-swig-dependency/provision/fake-pocketsphinx.sh | bash -"]
WORKDIR /app
ADD . /app
RUN virtualenv -p python3 venv
RUN . venv/bin/activate
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "-u", "Script_reader.py"]
