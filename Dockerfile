# Dockerfile

# Use the official Python image as the base
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry (optional, if you're using it)
# RUN pip install poetry

# Copy dependency files
COPY requirements.txt .
COPY dev-requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r dev-requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000 for the app
EXPOSE 8000

# Define the default command to run the app using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
