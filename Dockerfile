# Use a minimal base image with bash and necessary utilities
FROM alpine:latest

# Install necessary packages: bash, curl, netcat
RUN apk --no-cache add bash curl netcat-openbsd

# Set the working directory in the container
WORKDIR /app

# Copy the script and configuration directory into the container
COPY file_upload.sh /app/file_upload.sh
COPY config/ /app/config/

# Copy the external tool into the container
#COPY external-tool /usr/local/bin/external-tool

# Make the script and external tool executable
#RUN chmod +x /app/file_upload.sh /usr/local/bin/external-tool

# Create the data directory and its subdirectories
RUN mkdir -p /data/uploads /data/results /data/logs

# Expose the port the application will run on
EXPOSE 8080

# Use a non-root user for security reasons
USER nobody

# Run the script when the container starts
CMD ["sh", "/app/file_upload.sh"]
