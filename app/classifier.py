
from tokenize import String
from typing import List
from xmlrpc.client import Boolean
from logger import log
import os
import zipfile
import shutil

from donkeycar.pipeline.training import train
from donkeycar.management.base import load_config

from werkzeug.utils import secure_filename

from cv2 import FileStorage


class DonkeyCarClassifier:

    def __allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.__ALLOWED_EXTENSIONS

    def __init__(self, unique_mycar_folder, model_path:String, data_path:String, model_file_name:String) -> None:
        self.model_path:String = model_path
        self.__data_path:String = data_path
        self.__model_file_name:String = model_file_name
        self.__ALLOWED_EXTENSIONS = set(['py', 'zip'])
        self.__unique_mycar_path = unique_mycar_folder
        self.__tub_file_name = ''
        self.__config_file_path = ''
        self.__tub_file_path = ''

    def set_files(self, files:List[FileStorage]) -> None:
        self.files = files
        for file in files:
            log('Filename: ' + file.filename)
            if file and self.__allowed_file(file.filename):
                # Convention: if not .py, it is a zip of data
                if '.py' not in file.filename:
                    self.__tub_file_name = file.filename.replace('.zip', '')
                    log(self.__tub_file_name)
                    with zipfile.ZipFile(file, 'r') as zip_ref:
                        zip_extraction_location = os.path.join(self.__data_path, self.__tub_file_name)
                        log("zip_extraction_location: " + zip_extraction_location)
                        zip_ref.extractall(zip_extraction_location)
                else:
                    file.save(os.path.join(self.__unique_mycar_path, 'myconfig.py'))

        log("Getting config file")
        self.__config_file_path = os.path.join(self.__unique_mycar_path, 'config.py')
        log(self.__config_file_path)

        log("Getting data folder location")
        self.__tub_file_path = os.path.join(self.__data_path, os.path.join(self.__tub_file_name, self.__tub_file_name))
        log(self.__tub_file_path)

    def train(self) -> None:
        cfg = load_config(config_path=self.__config_file_path)
        log(cfg)
        log('Train uploaded zip file')
        # python base.py train --tub ../../mycar/data/tub_1_20-02-22_new/ --model ../../mycar/models/mypilot.h5 --config=../../mycar/config.py
        try:
            history = train(cfg=cfg, tub_paths=self.__tub_file_path, model=os.path.join(self.model_path, secure_filename(self.__model_file_name)), model_type = None, transfer=None, comment=None)
        except Exception as e:
            from data_format import convert_to_tub_v2
            legacy_tub_path = self.__tub_file_path
            self.__tub_file_path = self.__tub_file_path + '_new'

            #python convert_to_tub_v2.py --tub=/Users/jolu/Repos/donkeycar/mycar/data/tub_1_20-02-22 --output=/Users/jolu/Repos/donkeycar/mycar/data/tub_1_20-02-22_new
            convert_to_tub_v2(legacy_tub_path, self.__tub_file_path)
            history = train(cfg=cfg, tub_paths=self.__tub_file_path, model=os.path.join(self.model_path, secure_filename(self.__model_file_name)), model_type = None, transfer=None, comment=None)

    @property
    def model_location(self) -> String:
        return os.path.join(self.model_path, secure_filename(self.__model_file_name))

    def __del__(self) -> None:
        # remove folders after training
        shutil.rmtree(self.__unique_mycar_path)