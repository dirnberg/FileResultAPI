#!/bin/bash

# Define paths
UPLOAD_DIR="/data"
RESULTS_DIR="/data"
LOG_DIR="/data"

# Create necessary directories with proper permissions
mkdir -p "$UPLOAD_DIR" "$RESULTS_DIR" "$LOG_DIR"
chmod 700 "$UPLOAD_DIR" "$RESULTS_DIR" "$LOG_DIR"

# Function to generate a unique session ID
generate_session_id() {
    echo $(date +%s%N | sha256sum | head -c 16)
}

# Function to log the request
log_request() {
    local session_id="$1"
    local client_ip="$2"
    local user_agent="$3"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "$timestamp - IP: $client_ip - User-Agent: $user_agent" >> "$LOG_DIR/${session_id}_requests.log"
}

# Function to sanitize filenames
sanitize_filename() {
    echo "$1" | sed 's/[^\w.-]/_/g'
}

# Function to process files
process_files() {
    local session_id="$1"
    local session_path="$UPLOAD_DIR/$session_id"
    mkdir -p "$session_path"

    # Read and save incoming files
    while IFS= read -r file; do
        sanitized_filename=$(sanitize_filename "$(basename "$file")")
        echo "$file" | base64 -d > "$session_path/$sanitized_filename"
    done

    # Example processing (to be replaced with actual processing)
    local result_file="$RESULTS_DIR/${session_id}_result.txt"
    echo "Files processed for session $session_id" > "$result_file"

    # Output the result file
    cat "$result_file"
}

# Generate a unique session ID
session_id=$(generate_session_id)

# Get client IP and User-Agent (set by Docker run command or default)
client_ip=${CLIENT_IP:-"unknown"}
user_agent=${USER_AGENT:-"unknown"}

# Log the request
log_request "$session_id" "$client_ip" "$user_agent"

# Use netcat to handle HTTP requests
while :; do
    echo "Listening for HTTP requests on port 8080..."
    echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n" | nc -l -p 8080 -q 1 | {
        read request
        if [[ $request == *"Content-Disposition:"* ]]; then
            process_files "$session_id"
        fi
    }
done
