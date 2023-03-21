from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models.Models import Product
from flask_security.utils import login_user, logout_user
from flask_security import login_required, current_user
from flask_security.decorators import roles_accepted, roles_required
from ..controllers.product_controller import insertProduct, setProduct, updateProduct, deleteProduct
from ..models.forms import ProductForm

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
@roles_accepted('admin', 'client')
def profile():
    return render_template('profile.html', name=current_user.username)


@main.route('/information')
@login_required
@roles_accepted('client', 'admin')
def information():
    return render_template('information.html')

@main.route('/contact')
def contact():
    return render_template('contact.html')

@main.route('/catalogue-products')
@login_required
@roles_accepted('admin', 'client')
def catalogue_products():
    products = Product.query.all()
    return render_template('catalogue_products.html', products=products)

@main.route('/index-products')
@login_required
@roles_required('admin')
def index_products():
    products = Product.query.all()
    return render_template('index_products.html', products=products)

@main.route('/insert-product', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def insert_product():
    create_form = ProductForm(request.form)

    if(request.method == 'POST'):
        photo = request.form.get('photo')
        insertProduct(create_form)
        return redirect(url_for('main.index_products'))
    
    return render_template('insert_product.html', form = create_form)

@main.route('/update-product', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def update_product():
    create_form = ProductForm(request.form)

    if(request.method == 'GET'):
        id = request.args.get('id')
        response = setProduct(id, create_form)
        return render_template('update_product.html', form = response)

    if(request.method == 'POST'):
        updateProduct(create_form.id.data, create_form)
        return redirect(url_for('main.index_products'))
    
@main.route('/delete-product', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def delete_product():
    create_form = ProductForm(request.form)

    if(request.method == 'GET'):
        id = request.args.get('id')
        response = setProduct(id, create_form)
        return render_template('delete_product.html', form = response)

    if(request.method == 'POST'):
        deleteProduct(create_form.id.data)
        return redirect(url_for('main.index_products'))