# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.10.10

# Set the working directory in the container
WORKDIR /app

# Copy just the requirements.txt into the container
COPY requirements.txt /app/

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install spacy
RUN python -m spacy download en_core_web_lg
# pip install en_core_web_lg-3.6.0-py3-none-any.whl

EXPOSE 8080

# Run the Python application
CMD ["python", "main.py"]
