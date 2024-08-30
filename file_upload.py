import os
import datetime
import base64
import logging
import subprocess
from flask import Flask, request, send_from_directory

app = Flask(__name__)

UPLOAD_DIR = '/data/uploads'
RESULTS_DIR = '/data/results'
LOG_DIR = '/data/logs'
CONFIG_DIR = '/app/config'

# Create necessary directories
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(filename=os.path.join(LOG_DIR, 'requests.log'),
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def log_request(client_ip, user_agent):
    logging.info(f"IP: {client_ip}, User-Agent: {user_agent}")

def process_files(session_id):
    session_path = os.path.join(UPLOAD_DIR, session_id)
    os.makedirs(session_path, exist_ok=True)

    # Example processing (replace with actual external tool call)
    result_file = os.path.join(RESULTS_DIR, f'{session_id}_result.txt')
    with open(result_file, 'w') as f:
        f.write(f"Files processed for session {session_id}\n")

    # Simulate external tool execution (replace with actual tool command)
    subprocess.run([
        'external-tool', 
        '--config', os.path.join(CONFIG_DIR, 'config.yml'),
        '--input', session_path,
        '--output', result_file
    ], check=True)

    return result_file

@app.route('/upload', methods=['POST'])
def upload_files():
    session_id = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    files = request.files.getlist('files')
    client_ip = request.headers.get('X-Forwarded-For', 'unknown')
    user_agent = request.headers.get('User-Agent', 'unknown')

    log_request(client_ip, user_agent)

    for file in files:
        filename = file.filename
        file_path = os.path.join(UPLOAD_DIR, session_id, filename)
        file.save(file_path)

    result_file = process_files(session_id)

    return send_from_directory(RESULTS_DIR, os.path.basename(result_file), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
