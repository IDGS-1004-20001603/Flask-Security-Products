from wtforms import Form, StringField, IntegerField, DecimalField, FileField, validators
from flask_wtf.file import FileRequired, FileAllowed

class ProductForm(Form):
    id = IntegerField('id')
    name = StringField('name', [
        validators.DataRequired(message='You need to write something')
    ])
    price = DecimalField('price', [
        validators.DataRequired(message='You need to write something')
    ])
    photo = FileField('photo', validators=[
            FileRequired(),
            FileAllowed(["png", "jpg", "jpeg"], "This file is not a valid image !",)
    ])