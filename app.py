from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db = SQLAlchemy()
db.init_app(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        description = request.form['description']
        price = request.form['price']
        new_product = Product(name=name, code=code, description=description, price=price)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_product.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.code = request.form['code']
        product.description = request.form['description']
        product.price = request.form['price']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_product.html', product=product)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('delete_product.html', product=product)




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
