# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Set environment variables
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    gcc \
    libsqlite3-mod-spatialite \  
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt ./
RUN apt-get update && pip install --no-cache-dir -r requirements.txt

COPY requirements-reports.txt ./
RUN apt-get update && pip install --no-cache-dir -r requirements-reports.txt

# Copy the current directory contents into the container at /usr/src/app/
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Define environment variable
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

RUN ls

# Run the application:
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8080"]
