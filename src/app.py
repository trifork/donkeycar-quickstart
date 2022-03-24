import os
import subprocess
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from donkeycar.pipeline.training import train
from donkeycar.management.base import load_config

app = Flask(__name__)

uploads_dir = os.path.join(app.root_path, '../data')
model_dir = os.path.join(app.root_path, '../models')
model_file_name = 'mypilot.h5'

app.config['DATA_FOLDER'] = uploads_dir
app.config['MODELS_FOLDER'] = model_dir
app.config['MODELS_FILE_NAME'] = model_file_name

ALLOWED_EXTENSIONS = set(['py', 'zip'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload():
   return render_template('upload.html')

@app.route('/train', methods = ['GET', 'POST'])
def train():
   tub_file_name = ''
   if request.method == 'POST':
      # getting multiple files - both a config and a zip/tar something compressed
      files = request.files.getlist('files[]')
      for file in files:
         if file and allowed_file(file.filename):
               if '.py' not in file.filename:
                  tub_file_name = file.filename
               filename = secure_filename(file.filename)
               file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

      print('Train uploaded zip file')
      config_file = os.path.join(app.config['UPLOAD_FOLDER'], 'config.py')
      tub_file = os.path.join(app.config['UPLOAD_FOLDER'], tub_file_name)

      cfg = load_config(config_path=config_file)
      train(cfg=cfg, tub_paths=tub_file, model=os.path.join(app.config['MODELS_FOLDER'], secure_filename(app.config['MODELS_FILE_NAME'])), model_type = None, transfer=None, comment=None)
      # python base.py train --tub ../../mycar/data/tub_1_20-02-22_new/ --model ../../mycar/models/mypilot.h5 --config=../../mycar/config.py

      return send_file(os.path.join(app.config['MODELS_FOLDER'], secure_filename(app.config['MODELS_FILE_NAME'])), as_attachment=True, attachment_filename=app.config['MODELS_FILE_NAME'])

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)