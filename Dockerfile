# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend folder into the container at /app/backend
COPY ./backend ./backend
# Copy the db and data folders so the container can access them
COPY ./db ./db
COPY ./data ./data

# Set the working directory to the backend code
WORKDIR /app/backend

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for the API key
# The actual key will be passed in when we run the container
ENV GOOGLE_API_KEY="Gemini 2.5 pro API Key"

# Run app.py when the container launches using Gunicorn
# This is a production-ready WSGI server

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "app:app"]
