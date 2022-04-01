from asyncio import constants
from crypt import methods
import os, sys
import zipfile
import asyncio
import shutil
from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from donkeycar.pipeline.training import train
from donkeycar.management.base import load_config, CreateCar

from constants import SetupConstants

def log(content):
   print(content, file=sys.stderr)

app = Flask(__name__)
SetupConstants(app)

ALLOWED_EXTENSIONS = set(['py', 'zip'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload():
   return render_template('upload.html')

@app.route('/train', methods = ['POST'])
async def train_model():
   tub_file_name = ''
   # getting multiple files - both a config and a zip/tar something compressed
   log(request.files)

   files = request.files.getlist('file')
   log(files)
   
   if not files:
      log("Not files")
      return redirect(url_for('upload'))
   
   for file in files:
      log('Filename: ' + file.filename)
      if file and allowed_file(file.filename):

         # TODO make uploaded files/folders names unique: get the files/folders
         #      - save then with specific unique names on the server and train with the same unique names again later
         # TODO show page loader when training

         # Convention: if not config.py, it is a zip of data
         if '.py' not in file.filename:
            tub_file_name = file.filename.replace('.zip', '')
            log(tub_file_name)
            with zipfile.ZipFile(file, 'r') as zip_ref:
               zip_extraction_location = os.path.join(app.config['DATA_FOLDER'], tub_file_name)
               log("zip_extraction_location: " + zip_extraction_location)
               zip_ref.extractall(zip_extraction_location)
         else:
            file.save(os.path.join(app.config['MYCAR_FOLDER'], 'config.py'))

   log('Train uploaded zip file')
   config_file = os.path.join(app.config['MYCAR_FOLDER'], 'config.py')
   log(config_file)
   tub_file = os.path.join(app.config['DATA_FOLDER'], os.path.join(tub_file_name, tub_file_name))
   log(tub_file)

   cfg = load_config(config_path=config_file)

   task = asyncio.create_task(train(cfg=cfg, tub_paths=tub_file, model=os.path.join(app.config['MODELS_FOLDER'], secure_filename(app.config['MODELS_FILE_NAME'])), model_type = None, transfer=None, comment=None))
   # python base.py train --tub ../../mycar/data/tub_1_20-02-22_new/ --model ../../mycar/models/mypilot.h5 --config=../../mycar/config.py

   # remove folders after training
   shutil.rmtree(tub_file)

   await task

   return send_file(os.path.join(app.config['MODELS_FOLDER'], secure_filename(app.config['MODELS_FILE_NAME'])), as_attachment=True, download_name=app.config['MODELS_FILE_NAME'])

@app.route('/basic-config', methods= ['GET'])
def get_basic_config():
   return send_file(os.path.join(app.config['MYCAR_FOLDER'], 'config.py'))

if __name__ == "__main__":
   c = CreateCar()
   log(app.root_path + '/mycar')
   c.create_car(path=app.root_path + '/mycar')

   port = int(os.environ.get('PORT', 5000))
   app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)