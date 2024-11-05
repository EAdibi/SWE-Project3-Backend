# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define environment variables
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8080"]