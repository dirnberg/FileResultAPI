# Use the official Python 3.11 slim image from the Docker Hub
FROM python:3.11-slim

# Set environment variables
ENV UPLOAD_FOLDER=/app/uploads
ENV RESULTS_FILE=/app/uploads/results.yml
ENV IOCS_FILE=/app/iocseek
ENV CONFIG_FILE=/app/config.yml
ENV ALLOWED_EXTENSIONS=md,yar,json,sigma,rules

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Create the necessary directories
RUN mkdir -p /app/uploads /app/config

# Set the working directory in the container
WORKDIR /app

# Install Git and other necessary packages
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app/

# Copy the iocseek tool into the container
COPY iocseek /app/

# Make the iocseek binary executable
RUN chmod +x /app/iocseek


# Make port 3000 available to the world outside this container
EXPOSE 3000

# Run app.py when the container launches
CMD ["python", "app.py"]
