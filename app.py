from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from flask_cors import CORS 
from dotenv import load_dotenv

import os

load_dotenv()

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
CORS(app)

class GearItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=False)

    def __init__(self, title, price, description, img):
        self.title = title
        self.price = price
        self.description = description
        self.img = img

class GearItemSchema(ma.Schema):
    class Meta: 
        fields = ("title", "price", "description", "img")

gear_item_schema = GearItemSchema()
multiple_gear_item_schema = GearItemSchema(many=True)


@app.route('/gear-item/add', methods=["POST"])
def add_gear_item():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    title = post_data.get('title')
    price = post_data.get('price')
    description = post_data.get('description')
    img = post_data.get('img')

    item = db.session.query(GearItem).filter(GearItem.title == title).first()

    if title == None:
        return jsonify("Error: Data must have a 'title' key.")

    if price == None:
        return jsonify("Error: Data must have a 'price' key.")

    if description == None:
        return jsonify("Error: Data must have a 'description' key.")

    if img == None:
        return jsonify("Error: Data must have a 'img' key.")

    
    new_item = GearItem(title, price, description, img)
    db.session.add(new_item)
    db.session.commit()

    return jsonify("You've added a new gear item!")


@app.route('/gear-item/get', methods=["GET"])
def get_gear_items():
    items = db.session.query(GearItem).all()
    return jsonify(multiple_gear_item_schema.dump(items))


@app.route('/gear-item/get/<id>', methods=["GET"])
def get_gear_item_by_id(id):
    item = db.session.query(GearItem).filter(GearItem.id == id).first()
    return jsonify(gear_item_schema.dump(item))


@app.route('/gear-item/delete/<id>', methods=["DELETE"])
def delete_gear_item(id):
    item = db.session.query(GearItem).filter(GearItem.id == id).first()
    db.session.delete(item)
    db.session.commit()

    return jsonify("The Gear item has been deleted")


@app.route('/gear-item/update/<id>', methods=["PUT", "PATCH"])
def update_gear_item_by_id(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    title = post_data.get('title')
    price = post_data.get('price')
    description = post_data.get('description')
    img = post_data.get('img')

    item = db.session.query(GearItem).filter(GearItem.id == id).first()

    if title != None:
        item.title = title
    if price != None:
        item.price = price
    if description != None:
        item.description = description
    if img != None:
        item.img = img

    db.session.commit()
    return jsonify("Gear item has been updated.")





class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String, nullable=False)

    def __init__(self, title, price, img):
        self.title = title
        self.price = price
        self.img = img

class CartSchema(ma.Schema):
    class Meta: 
        fields = ("title", "price", "img")

cart_schema = CartSchema()
multiple_cart_schema = CartSchema(many=True)


@app.route('/cart/add', methods=["POST"])
def add_cart_item():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    title = post_data.get('title')
    price = post_data.get('price')
    img = post_data.get('img')

    item = db.session.query(Cart).filter(Cart.title == title).first()

    if title == None:
        return jsonify("Error: Data must have a 'title' key.")

    if price == None:
        return jsonify("Error: Data must have a 'price' key.")

    if img == None:
        return jsonify("Error: Data must have a 'img' key.")

    
    new_item = Cart(title, price, img)
    db.session.add(new_item)
    db.session.commit()

    return jsonify("You've added a new cart item!")


@app.route('/cart/get', methods=["GET"])
def get_cart_items():
    items = db.session.query(Cart).all()
    return jsonify(multiple_cart_schema.dump(items))


# @app.route('/cart/get/<id>', methods=["GET"])
# def get_cart_item_by_id(id):
#     item = db.session.query(Cart).filter(Cart.id == id).first()
#     return jsonify(cart_schema.dump(item))


# @app.route('/cart/delete/<id>', methods=["DELETE"])
# def delete_cart_item_by_id(id):
#     item = db.session.query(Cart).filter(Cart.id == id).first()
#     db.session.delete(item)
#     db.session.commit()

#     return jsonify("The cart item has been deleted")


@app.route('/cart/delete', methods=['DELETE'])
def delete_all_cart_items():
    all_cart_items = db.session.query(Cart).all()
    for item in all_cart_items:
        db.session.delete(item)
    
    db.session.commit()
    return jsonify('All your cart items have been deleted.')
    

if __name__ == "__main__":
    app.run(debug=True)