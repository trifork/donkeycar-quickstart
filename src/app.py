from asyncio import constants
from crypt import methods
import os, sys
import zipfile
import asyncio
import shutil
import secrets
from classifier import DonkeyCarClassifier
from logger import log
from flask import Flask, render_template, request, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from donkeycar.pipeline.training import train
from donkeycar.management.base import load_config, CreateCar

def get_random_token():
    """
    Creates a cryptographically-secure, URL-safe string
    """
    return secrets.token_urlsafe(16)

app = Flask(__name__)

@app.route('/')
def upload():
   return render_template('upload.html')

@app.route('/train', methods = ['POST'])
async def train_model():

   c = CreateCar()
   random_token = get_random_token()
   unique_mycar_folder = os.path.join(app.root_path, 'mycar' + random_token)
   log(unique_mycar_folder)
   c.create_car(path=unique_mycar_folder)
   data_folder = os.path.join(unique_mycar_folder, 'data')
   models_folder = os.path.join(unique_mycar_folder, 'models')
   model_file_name = 'mypilot.h5'

   donkeyCarClassifier = DonkeyCarClassifier(unique_mycar_folder=unique_mycar_folder,model_path=models_folder,data_path=data_folder,model_file_name=model_file_name)

   files = request.files.getlist('files[]')
   
   if not files:
      log("Not files")
      return redirect(url_for('upload'))
   
   donkeyCarClassifier.set_files(files=files)
   donkeyCarClassifier.train()

   response = send_file(donkeyCarClassifier.model_location, as_attachment=True, download_name=model_file_name)
   response.headers["x-filename"] = model_file_name   
   response.headers["Access-Control-Expose-Headers"] = 'x-filename'
   return response

@app.route('/myconfig', methods= ['GET'])
def get_basic_config():
   return send_file(os.path.join(app.root_path, 'myconfig.py'))

if __name__ == "__main__":
   port = int(os.environ.get('PORT', 5000))
   app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)