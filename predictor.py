from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img , img_to_array
from translator import Translator
from detector import Detector
from db import config

class Predictor:
    def __init__(self):
        self.model = load_model(**config(section="mobilenet"))

    def predict_bird(self, translator:Translator, filename:str):
            img = Image.open(filename[1:])
            if '.png' in (filename[1:]):
                img = img.convert('RGB')
            img = img.resize((224, 224))
            img_to_predict = np.array([np.array(img)])
            img_to_predict = img_to_predict/255.0
            pred_class = self.model.predict(img_to_predict)
            prediction = np.argmax(pred_class, axis = 1)[0] + 1
            lang_bird = 'ruBirds' if translator.currentLanguage == 'ru' else 'enBirds' 
            return translator.getBird(prediction, lang_bird)