from flask import Flask, render_template, send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_ngrok import run_with_ngrok
from wtforms import SubmitField
from PIL import Image
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img , img_to_array
import pandas as pd
import uuid
import cvlib
import cv2

app = Flask(__name__)
model_class = load_model('modelBase.hdf5')
data = pd.read_excel('BirdsFinal.xlsx').to_dict('records')
classes_en = [d['bird_en'] for d in data]
classes_ru = [d['bird_ru'] for d in data]
app.config['SECRET_KEY'] = 'asdasda'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

def check_birds(filename):
    image = cv2.imread(filename[1:])
    _, label, _ = cvlib.detect_common_objects(image, model='yolov3')
    birds = label.count('bird')
    if birds < 0 or birds > 1:
        return False
    else: return True

def translate(lang, bird):
    bird = list(filter(lambda dict: dict['bird_en'] == bird, data))[0]
    if lang == 'en':
        return bird['bird_en']
    else:
        return bird['bird_ru']

def get_desc(bird, lang):
    if lang == 'en':
        bird = list(filter(lambda dict: dict['bird_en'] == bird, data))[0]
        return bird['desc_en']
    else:
        print(bird)
        bird = list(filter(lambda dict: dict['bird_ru'] == bird, data))[0]
        return bird['desc_ru']
def predict_class(filename , model, lang):
    if check_birds(filename):
        img = Image.open(filename[1:])
        img = img.resize((224, 224))
        img_to_predict = np.array([np.array(img)])
        img_to_predict = img_to_predict/255.0
        prediction = np.argmax(model.predict(img_to_predict)[0])
        if lang == 'en':
            return translate('en', classes_en[prediction])
        else:
            return translate('ru', classes_en[prediction])
    else:
        if lang == 'en':
            return 'A photo of one bird is required'
        else: return 'Необходимо фото одной птицы'

class EnLoadForm(FlaskForm):
    photo = FileField(
        validators = [
            FileAllowed(photos, 'Invalid photo format'),
            FileRequired('Image required for classification')
        ]
    )
    submit = SubmitField('Load')

class RuLoadForm(FlaskForm):
    photo = FileField(
        validators = [
            FileAllowed(photos, 'Некорректный формат изображения'),
            FileRequired('Необходимо изображение для классификации')
        ]
    )
    submit = SubmitField('Загрузить')

@app.route('/uploads/<filename>')
def get_preview(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)  
  
@app.route('/', methods = ['GET', 'POST'])
@app.route('/<lang>', methods = ['GET', 'POST'])
def main(lang = None):
    if lang == 'en':
        post_form = EnLoadForm()
        hello_msg = 'Show me the bird and I"ll tell you who it is'
    else:
        post_form = RuLoadForm()
        hello_msg = 'Покажи мне птичку, а я скажу тебе кто она'
    if post_form.validate_on_submit():
        filename = photos.save(post_form.photo.data, name=f"{uuid.uuid4().hex}.")
        file_url = url_for('get_preview', filename=filename)
        class_file = predict_class(file_url, model_class, lang)
        if class_file in classes_en or class_file in classes_ru:
            desc_file = get_desc(class_file, lang)
        else: desc_file = None
    else:
        file_url = None
        class_file = None
        desc_file = None
    return render_template('index.html', Hello_Message = hello_msg, form = post_form, file_url = file_url, class_file = class_file, desc_file = desc_file)

app.run(port=4996, debug=True)