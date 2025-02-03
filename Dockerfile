# Use a slim base image
FROM python:3.10-slim

RUN apt-get clean \
    && apt-get update \
    && apt-get install -y \
    git \
    wget \
    ffmpeg \
    unzip \
    && python -m pip install --upgrade pip

# Set the working directory
WORKDIR /app

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt -f install \
    && apt-get install ./google-chrome-stable_current_amd64.deb -y

RUN wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.108/linux64/chromedriver-linux64.zip \
    && unzip chromedriver-linux64.zip \
    && cp chromedriver-linux64/chromedriver /usr/bin

RUN rm google-chrome-stable_current_amd64.deb && rm -rf chromedriver-linux64

# Clone repository
RUN git clone https://github.com/thd3r/godork.git

# Change the working directory to the cloned repository
WORKDIR /app/godork

RUN pip install --no-cache-dir -r requirements.txt

# Install dependencies using pip
RUN pip install --no-cache-dir .

# Set the entrypoint to run godork
ENTRYPOINT ["godork"]
