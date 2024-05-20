# Use a slim base image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Install git and dependencies
RUN apt-get update && apt-get install -y git 

# Clone repository
RUN git clone https://github.com/thd3r/godork.git

# Change the working directory to the cloned repository
WORKDIR /app/godork

# Install dependencies using pip
RUN pip install .

# Set the entrypoint to run godork
ENTRYPOINT ["godork"]