import os
import shutil
import requests
import tempfile

from gevent.pywsgi import WSGIServer
from flask import Flask, after_this_request, render_template, request, send_file
from subprocess import call

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = set(['svg'])

app = Flask(__name__)


# Convert using Libre Office
def convert_file(input_file_path, output_dir, output_file_path):
    call('inkscape --file %s  --export-png %s ' %
         (input_file_path, output_file_path), shell=True)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def api():
    output_extension = 'png'
    file_name = 'image'
    work_dir = tempfile.TemporaryDirectory()
    input_file_path = os.path.join(work_dir.name, file_name)
    output_file_path = os.path.join(work_dir.name, file_name + '.' + output_extension)

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file provided'
        file = request.files['file']
        if file.filename == '':
            return 'No file provided'
        if file and allowed_file(file.filename):
            file.save(input_file_path)

    if request.method == 'GET':
        url = request.args.get('url', type=str)
        if not url:
            return render_template('index.html')
        # Download from URL
        response = requests.get(url, stream=True)
        with open(input_file_path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)
        del response

    convert_file(input_file_path, work_dir.name, output_file_path)

    @after_this_request
    def cleanup(response):
        work_dir.cleanup()
        return response
 
    return send_file(output_file_path, mimetype='image/png')


if __name__ == "__main__":
    http_server = WSGIServer(('', int(os.environ.get('PORT', 8080))), app)
    http_server.serve_forever()
