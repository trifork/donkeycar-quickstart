
import os

class SetupConstants():
    def __init__(self, app) -> None:
        root_path = app.root_path
        data_folder = os.path.join(root_path, 'mycar/data')
        model_folder = os.path.join(root_path, 'mycar/models')
        mycar_folder = os.path.join(root_path, 'mycar')
        model_file_name = 'mypilot.h5'

        app.config['DATA_FOLDER'] = data_folder
        app.config['MODELS_FOLDER'] = model_folder
        app.config['MODELS_FILE_NAME'] = model_file_name
        app.config['MYCAR_FOLDER'] = mycar_folder