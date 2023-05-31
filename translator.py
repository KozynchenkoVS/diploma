from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from bird import Bird

photos = UploadSet('photos', tuple('jpg jpeg png'.split()))

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

class Translator:
    def __init__(self,DbManager, currentLanguage="en"):
        self.currentLanguage = currentLanguage
        self.db_manager = DbManager
    def getFileForm(self):
        if self.currentLanguage == "ru":
            return RuLoadForm()
        else: return EnLoadForm()

    def getBird(self, bird_id, lang_bird):
        bird = self.db_manager.execute_query("SELECT " + ", ".join(list((Bird().__dict__).keys())) 
                    + f" FROM classes JOIN {lang_bird} ON classes.bird_id={lang_bird}.bird_id WHERE {lang_bird}.bird_id = {bird_id}")

        bird = Bird(*bird[1])
        if self.currentLanguage == "ru":
            return bird.getRusssian()
        else: return bird.getEnglish()

    def throwError(self):
        if self.currentLanguage == 'en':
            return 'A photo of one bird is required'
        else: return 'Необходимо фото одной птицы'

    def Hello(self):
        if self.currentLanguage == 'en':
            return 'Show me the bird and I"ll tell you who it is'
        else: return 'Покажи мне птичку, а я скажу тебе кто она'

    
