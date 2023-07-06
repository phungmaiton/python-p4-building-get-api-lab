#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route("/")
def index():
    return "<h1>Bakery GET API</h1>"


@app.route("/bakeries")
def bakeries():
    bakeries = []
    for bakery in Bakery.query.all():
        bakeries.append(bakery.to_dict())

    response = make_response(bakeries, 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/bakeries/<int:id>")
def bakery_by_id(id):
    bakery = Bakery.query.filter(id == id).first().to_dict()

    response = make_response(bakery, 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/baked_goods/by_price")
def baked_goods_by_price():
    baked_goods = [baked_good.to_dict() for baked_good in BakedGood.query.all()]
    sorted_baked_goods = sorted(baked_goods, key=lambda x: x["price"], reverse=True)

    response = make_response(sorted_baked_goods, 200)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route("/baked_goods/most_expensive")
def most_expensive_baked_good():
    baked_goods = [baked_good.to_dict() for baked_good in BakedGood.query.all()]
    sorted_baked_goods = sorted(baked_goods, key=lambda x: x["price"], reverse=True)
    most_expensive_good = sorted_baked_goods[0]
    response = make_response(most_expensive_good, 200)
    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
