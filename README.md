# FileResultAPI

**FileResultAPI** is a lightweight API service designed to handle file uploads, process them based on configurable settings, and return the result. The service runs inside a Docker container and includes features for logging and session management. This example demonstrates file handling with a ZIP archive, but the tool can be adapted for different types of processing.

## Features

- **Upload Multiple Files**: Accept and handle multiple files in a single request.
- **Configurable Processing**: Process files according to configuration settings.
- **Result Handling**: Return the processed result in various formats.
- **Session Management**: Unique session handling and logging for each request.
- **Dockerized**: Easy deployment using Docker with configurable volume mounts for data persistence.

## Installation

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your machine.

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/FileResultAPI.git
   cd FileResultAPI
   ```

2. **Build the Docker Image:**

   ```bash
   docker build -t file-result-api .
   ```

3. **Run the Docker Container:**

   ```bash
   docker run -p 8080:8080 \
              -v /path/to/local/uploads:/data/uploads \
              -v /path/to/local/results:/data/results \
              -v /path/to/local/logs:/data/logs \
              -e CLIENT_IP=$(curl -s ifconfig.me) \
              file-result-api
   ```

   - **`-p 8080:8080`**: Maps port 8080 of the container to port 8080 on the host.
   - **`-v /path/to/local/uploads:/data/uploads`**: Maps a local directory to the container's upload directory.
   - **`-v /path/to/local/results:/data/results`**: Maps a local directory to the container's results directory.
   - **`-v /path/to/local/logs:/data/logs`**: Maps a local directory to the container's logs directory.
   - **`-e CLIENT_IP=$(curl -s ifconfig.me)`**: Sets the `CLIENT_IP` environment variable.

## Usage

### Uploading Files

To upload files, send a POST request to the running server with the files as form-data:

```bash
curl -X POST \
     -F "file1=@/path/to/file1.txt" \
     -F "file2=@/path/to/file2.txt" \
     http://localhost:8080
```

The server will process the files and return the result. If you use the default processing, you will get a text file with the processing outcome.

### Accessing Logs

Log files for each session are stored in the `data/logs` directory. They include details like the timestamp, client IP, and user agent.

## Configuration

- **`file_upload.sh`**: Modify this script to adjust file processing behavior or integrate with different tools.
- **`config_file.conf`**: Use this configuration file for tool-specific settings.

## Example Docker Setup

For demo purposes, the Docker setup includes a simple ZIP use case. To adapt it for other use cases:

1. Modify `file_upload.sh` to handle different processing requirements.
2. Update Dockerfile and configuration files as needed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork the repository, make changes, and submit pull requests. Please ensure that your contributions follow the project's coding standards and include appropriate tests and documentation.

