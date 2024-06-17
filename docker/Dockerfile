FROM python:3.12-bookworm

RUN apt-get update &&  \
    apt-get install -y \
        fonts-dejavu \
        spi-tools \
        python3-libgpiod \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/240-py

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# use .dockerignore to exclude files from the image
COPY . .

# copy piligraphs from deps
COPY deps/piligraphs/piligraphs ./piligraphs

ENTRYPOINT ["python", "main.py"]