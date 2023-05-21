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
import os, random
import db
from db import config

app = Flask(__name__)
flask_conf = config(section='flask')
app.config['SECRET_KEY'] = flask_conf['secret_key']
app.config['UPLOADED_PHOTOS_DEST'] = flask_conf['uploaded_photos_dest']
photos = UploadSet('photos', tuple('jpg jpeg png'.split()))
configure_uploads(app, photos)
predictor = Predictor()
detector = Detector()
DbManager = db.DbManager()
DbManager.init_database()

@app.route('/uploads/<filename>')
def get_preview(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)  
  
@app.route('/', methods = ['GET', 'POST'])
@app.route('/<lang>', methods = ['GET', 'POST'])
def main(lang = None):
    translator = Translator(currentLanguage= lang, DbManager= DbManager)
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

@app.route('/birds/<bird>')
def get_random_bird(bird):
    path = f"birds/{bird.rsplit(sep=':')[1]}"
    filename = random.choice(os.listdir(path))
    return send_from_directory(path, filename)  

@app.route('/<lang>/bird/<bird>', methods = ['GET'])
def bird(lang=None, bird=None):
    translator = Translator(currentLanguage=lang, DbManager=DbManager)
    bird_data = translator.getBird(bird)
    file_url = url_for('get_random_bird', bird= bird_data[4])
    bird = showBird(bird_data[0], bird_data[1], bird_data[2], bird_data[3])
    return render_template('bird.html', file_url = file_url, bird = bird)

app.run(port=int(flask_conf['port']), debug=True)