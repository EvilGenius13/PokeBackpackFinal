# Base image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install netcat for our startup script - doesn't come with slim-buster (needed for the startup script)
RUN apt-get update && apt-get install -y netcat && rm -rf /var/lib/apt/lists/*

# Copy the requirements file
COPY requirements.txt .

# Install the required dependencies
RUN pip install -r requirements.txt

# Copy the application code and the start-pokeapp.sh script into the container
COPY . .

# Ensure start-pokeapp.sh is executable
RUN chmod +x start-pokeapp.sh

# Expose the port your Flask app will be running on
EXPOSE 5000

# Run the Flask app with Gunicorn
CMD gunicorn app:app --bind 0.0.0.0:5000
