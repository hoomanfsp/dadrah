# Use the official Python 3.11.13 slim image
FROM python:3.11.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requ*.txt ./requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy the rest of your application code
COPY . .

# Set default command to run your CLI app
CMD ["python", "main.py"]
