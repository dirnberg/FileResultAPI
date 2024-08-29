# Use a minimal base image with bash and necessary utilities
FROM alpine:latest

# Install necessary packages: bash, curl, netcat (for listening to HTTP requests), and zip (for example use case)
RUN apk --no-cache add bash curl netcat-openbsd zip

# Set the working directory in the container
WORKDIR /app

# Copy the script and configuration file into the container
COPY file_upload.sh /app/file_upload.sh
COPY config_file.conf /app/config_file.conf

# Make the script executable
RUN chmod +x /app/file_upload.sh

# Expose the port the application will run on
EXPOSE 8080

# Use a non-root user for security reasons
USER nobody

# Run the script when the container starts
CMD ["sh", "/app/file_upload.sh"]
