# Use a slim base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    ffmpeg \
    unzip \
    && apt-get clean \
    && python -m pip install --upgrade pip

# Set working directory
WORKDIR /app

# Download Chrome browser and install
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt -f install \
    && apt-get install ./google-chrome-stable_current_amd64.deb -y 

# Take the Chrome version and put it through the files
RUN google-chrome --version | cut -d ' ' -f3 | while read -r line; do echo $line > /tmp/google-version.txt; done

# Download chromedriver based on Chrome browser version
RUN cat /tmp/google-version.txt | while read -r version; do wget https://storage.googleapis.com/chrome-for-testing-public/$version/linux64/chromedriver-linux64.zip; done

# Extract chromedriver and move the path
RUN unzip /app/chromedriver-linux64.zip && cp /app/chromedriver-linux64/chromedriver /usr/bin

# Remove tracks
RUN rm /app/google-chrome-stable_current_amd64.deb && rm -rf /app/chromedriver-linux64

# Copy the entire project
COPY . /app/

# Install dependencies using pip
RUN pip install -r requirements.txt

# Install the godork tool
RUN python setup.py install

# Set entrypoint
ENTRYPOINT ["godork"]