from flask import Flask, render_template, send_from_directory, url_for
from flask_uploads import UploadSet, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_ngrok import run_with_ngrok
from wtforms import SubmitField
import pandas as pd
import uuid
from bird import Bird
from predictor import Predictor
from translator import Translator
from showBird import showBird
from detector import Detector

app = Flask(__name__)
data = pd.read_excel('BirdsFinal.xlsx').to_dict('records')
bd_birds = [Bird(d['bird_ru'], d['bird_en'], d['desc_en'], d['desc_ru'], d['place_ru'], d['place_en'], d['size_ru'], d['size_en']) for d in data]
app.config['SECRET_KEY'] = 'asdasda'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'
photos = UploadSet('photos', tuple('jpg jpeg png'.split()))
configure_uploads(app, photos)
predictor = Predictor('modelBase.hdf5', bd_birds)
detector = Detector('yolov3')

@app.route('/uploads/<filename>')
def get_preview(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)  
  
@app.route('/', methods = ['GET', 'POST'])
@app.route('/<lang>', methods = ['GET', 'POST'])
def main(lang = None):
    translator = Translator(lang)
    post_form = translator.getFileForm()
    hello_msg = translator.Hello()
    if post_form.validate_on_submit():
        filename = photos.save(post_form.photo.data, name=f"{uuid.uuid4().hex}.")
        file_url = url_for('get_preview', filename=filename)
        if (detector.detectBirds(file_url)):
            bird_data = predictor.predict_bird(translator, file_url)
            class_bird = bird_data[0]
            bird = showBird(bird_data[0], bird_data[1], bird_data[2], bird_data[3])
        else:
            class_bird = translator.throwError()
            bird = None
    else:
        file_url = None
        class_bird = None
        bird = None
    return render_template('index.html', Hello_Message = hello_msg, form = post_form, file_url = file_url, bird = bird, class_bird = class_bird)

app.run(port=4996, debug=True)