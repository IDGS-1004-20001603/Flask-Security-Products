from ..models.Models import db, Product
from flask import request
from PIL import Image
import io
import base64


def setProduct(id, create_form):
    product = db.session.query(Product).filter(Product.id == id).first()
    create_form.id.data = product.id
    create_form.name.data = product.name
    create_form.price.data = product.price
    create_form.photo.data = product.photo

    return create_form


def insertProduct(create_form):
    photo = convertImageToBase64()

    product = Product(name=create_form.name.data,
                      price=create_form.price.data, photo=photo)
    db.session.add(product)
    db.session.commit()


def updateProduct(id, create_form):
    photo = convertImageToBase64()
    product = db.session.query(Product).filter(Product.id == id).first()
    product.name = create_form.name.data
    product.price = create_form.price.data
    product.photo = photo
    db.session.add(product)
    db.session.commit()


def deleteProduct(id):
    product = db.session.query(Product).filter(Product.id == id).first()
    db.session.delete(product)
    db.session.commit()


def convertImageToBase64():
    file = request.files["photo"]
    img = Image.open(file)

    buffered = io.BytesIO()
    img.save(buffered, format='PNG')
    return base64.b64encode(buffered.getvalue()).decode('utf-8')
