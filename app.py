from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout


db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///product_catalog.db"
db.init_app(app)

class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_title = db.Column(db.String(50), nullable=False)
    product_price = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, default=False)


with app.app_context():
    db.create_all() 
    

@app.route('/')
def index():
    items = Items.query.all()
    title = "Главная страниа"   
    
    return render_template("index.html", title=title, items=items)

@app.route('/buy/<int:id>')
def buy(id):
    items = Items.query.get(id)
    api = Api(merchant_id=1396424,
          secret_key='test')
    checkout = Checkout(api=api)
    data = {
    "currency": "RUB",
    "amount": str(items.product_price) + "00"
    }
    url = checkout.url(data).get('checkout_url')  
    
    return redirect(url)


@app.route('/create_product', methods =["POST", "GET"])
def create_product():
    title = "Добавить товар"
    if request.method == "POST":
        product_title = request.form['product_title']
        product_price = request.form['product_price']
        is_active = request.form['is_active']
        print(is_active)
        if request.form.get('is_active'):
            is_active = True
        else:
            is_active = False
        
        items = Items(product_title=product_title,product_price=product_price, is_active=is_active)
        
        try:
            db.session.add(items)
            db.session.commit()
            return redirect(url_for('index')) 
        except:
            return "При добовлении товара произошла ошибка"  
    else:
        return render_template("create_product.html", title=title)     
        
    
    
    




if __name__ == "__main__":
    app.run(debug=True)