# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add metadata to the image to describe that the container is listening on port 8015
EXPOSE 8015

# Copy the local requirements.txt file to the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the service account key into the Docker image
COPY flash-garage-392521-6debd0f223c4.json /app/

# Set the environment variable for google cloud
ENV GOOGLE_APPLICATION_CREDENTIALS=/app/flash-garage-392521-6debd0f223c4.json

# Copy the current directory contents into the container at /app
COPY . /app/

# Run the command to start uvcorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8015"]
