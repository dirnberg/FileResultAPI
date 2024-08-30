Certainly! Below is a complete `README.md` for your `FileResultApi` project. It includes sections for project overview, installation, usage, and testing.

---

# FileResultApi

**FileResultApi** is a Flask-based web service designed to handle file uploads, process them using an external tool, and return the results in a structured JSON format. The service also includes logging for tracking the operations performed.

## Overview

This API allows users to upload files, which are then processed by the `iocseek` tool (configured via `config.yml`). The results of the processing are converted to JSON and returned in the API response.

## Project Structure

```
FileResultApi/
│
├── app.py                # Main application file
├── config.yml            # Configuration file for iocseek
├── Dockerfile            # Dockerfile for building the Docker image
├── requirements.txt      # Python package dependencies
└── README.md             # This documentation
```

## Installation

### Prerequisites

- Docker (for containerized deployment)
- Python 3.11 (for local development)

### Docker Installation

1. **Build the Docker Image:**

   ```sh
   docker build -t fileresultapi .
   ```

2. **Run the Docker Container:**

   ```sh
   docker run -p 3000:3000 fileresultapi
   ```

   The application will be available at `http://localhost:3000`.

### Local Installation

1. **Clone the Repository:**

   ```sh
   git clone https://github.com/yourusername/FileResultApi.git
   cd FileResultApi
   ```

2. **Create a Virtual Environment:**

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Run the Application:**

   ```sh
   python app.py
   ```

   The application will be available at `http://localhost:3000`.

## Configuration

The application uses environment variables for configuration. You can set these in your environment or modify the `Dockerfile` to include them.

- `UPLOAD_FOLDER`: Directory for uploaded files (default: `/app/uploads`)
- `RESULTS_FILE`: Path to the results file (default: `/app/uploads/results.yml`)
- `IOCS_FILE`: Path to the `iocseek` tool (default: `/app/iocseek`)
- `CONFIG_FILE`: Path to the configuration file for `iocseek` (default: `/app/config.yml`)
- `ALLOWED_EXTENSIONS`: Comma-separated list of allowed file extensions (default: `md,yar,json,sigma,rules`)

## Usage

### Uploading a File

To upload a file to the API, use the following `curl` command:

```sh
curl -X POST http://localhost:3000/upload -F "file=@path/to/your/config.md" | python -m json.tool | pygmentize -l json
```

**Explanation:**

- `curl -X POST http://localhost:3000/upload -F "file=@path/to/your/config.md"`: Sends a POST request with the file `config.md`. Replace `path/to/your/config.md` with the path to your file.
- `python -m json.tool`: Formats the JSON response for readability.
- `pygmentize -l json`: Adds syntax highlighting to the JSON response.

### Example Response

```json
{
    "filename": "config.md",
    "files_in_uploads": [
        "results.yml",
        "config.md"
    ],
    "message": "File uploaded and processed successfully",
    "path": "/app/uploads/config.md",
    "results": {
        "flags": [
            "CTF{b8c1a066ea}",
            "CTF{f51c6c8d86}",
            "CTF{9fc5d3f019}",
            "CTF{1ba7791df2}",
            "CTF{889b5a7e45}"
        ],
        "max_points": 5,
        "points_per_category": {
            "Domains": "1/1",
            "IP Addresses": "0/0",
            "MAC Addresses": "1/1",
            "MITRE Techniques": "1/1",
            "Protocols": "0/0",
            "SHA-256 Hashes": "1/1",
            "URLs": "1/1"
        },
        "total_points": 5
    }
}
```

**Fields in the Response:**

- **filename**: Name of the uploaded file.
- **files_in_uploads**: List of files in the upload directory.
- **message**: Status message indicating success.
- **path**: Path where the file is stored.
- **results**: Processed results in JSON format.

## Troubleshooting

If you encounter issues, check the following:

- **Logs**: View the logs to see detailed error messages.
- **File Permissions**: Ensure that the application has the necessary permissions to read/write files.
- **Dependencies**: Verify that all dependencies are installed correctly.

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.