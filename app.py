import os
import subprocess
import json
import yaml
import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Read configuration from environment variables
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/app/uploads')
RESULTS_FILE = os.getenv('RESULTS_FILE', '/app/uploads/results.yml')
IOCS_FILE = os.getenv('IOCS_FILE', '/app/iocseek')
CONFIG_FILE = os.getenv('CONFIG_FILE', '/app/config.yml')
ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS', 'md,yar,json,sigma,rules').split(',')

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        app.logger.warning('No file part in the request')
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        app.logger.warning('No selected file')
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        try:
            file.save(file_path)
        except Exception as e:
            app.logger.error('Error saving file: %s', e)
            return jsonify({'error': 'Error saving file'}), 500

        app.logger.info('File uploaded successfully: %s', file.filename)

        # Call iocseek tool
        try:
            result = subprocess.run(
                [IOCS_FILE, '--config', CONFIG_FILE, '--input', UPLOAD_FOLDER, '--output', RESULTS_FILE],
                check=True, text=True, capture_output=True
            )
            app.logger.info('iocseek output: %s', result.stdout)
        except subprocess.CalledProcessError as e:
            app.logger.error('iocseek error: %s', e.stderr)
            return jsonify({'error': 'Error processing file'}), 500

        # Read and convert results to JSON
        try:
            with open(RESULTS_FILE, 'r') as results_file:
                results_yaml = yaml.safe_load(results_file)  # Parse YAML to Python dict
                results_json = json.dumps(results_yaml, indent=4)  # Convert dict to JSON
        except Exception as e:
            app.logger.error('Error reading or converting results file: %s', e)
            return jsonify({'error': 'Error reading or converting results file'}), 500

        # List all files in the uploads directory
        try:
            files_list = os.listdir(UPLOAD_FOLDER)
        except Exception as e:
            app.logger.error('Error listing files in upload directory: %s', e)
            files_list = []

        # Clean up the upload directory
        try:
            for filename in os.listdir(UPLOAD_FOLDER):
                file_to_remove = os.path.join(UPLOAD_FOLDER, filename)
                os.remove(file_to_remove)
        except Exception as e:
            app.logger.error('Error removing files from upload directory: %s', e)

        return jsonify({
            'filename': file.filename,
            'path': file_path,
            'message': 'File uploaded and processed successfully',
            'results': json.loads(results_json),  # Include the results as a JSON object
            'files_in_uploads': files_list
        }), 200
    else:
        app.logger.warning('File type not allowed')
        return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    port = int(os.getenv('PORT', 3000))
    app.logger.info(f'Starting Flask application on port {port}')
    app.run(host='0.0.0.0', port=port, debug=False)
