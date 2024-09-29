# Use an official Python runtime as a parent image
FROM python:3.12-alpine

# Set the working directory in the container
WORKDIR /kit

# Copy only the necessary files to install dependencies
COPY setup.py setup.cfg ./

# Install dependencies
RUN pip install --no-cache-dir .

# Copy the rest of the application code
COPY . .

# Install the local package
RUN pip install --no-cache-dir .
