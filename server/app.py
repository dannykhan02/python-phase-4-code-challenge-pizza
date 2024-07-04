#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


class Restaurants(Resource):
    def get(self):
       #ipdb.set_trace()
       restaut = Restaurant.query.all()
       rest_list = [rest.to_dict(rules=('-restaurant_pizzas',)) for rest in restaut]
       return  make_response(rest_list,200)
    
    def post(self):
        incoming=request.json
        new_restaut =Restaurant(**incoming)
        db.session.add(new_restaut)
        db.session.commit()
        return make_response(new_restaut.to_dict(),201)
    
class RestaurantById(Resource):
    def get(self,id):
        #ipdb.set_trace()
        restau = Restaurant.query.filter(Restaurant.id==id).first()
        if restau:
            return make_response(restau.to_dict(),200)
        else:
            return make_response({"error": "Restaurant not found"},404)
    def delete(self,id):
        restau = Restaurant.query.get(id)
        if restau:
            db.session.delete(restau)
            db.session.commit()
            return make_response({},204)
        else:
            return make_response({"error": "Restaurant not found"},404)
    
class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        pizzas_list = [pizza.to_dict(rules=('-restaurant_pizzas',)) for pizza in pizzas]
        return make_response(pizzas_list,200)
    def post(self):
        incoming = request.json
        new_pizza = Pizza(**incoming)
        db.session.add(new_pizza)
        db.session.commit()
        return make_response(new_pizza.to_dict(),201)
    
class RestaurantPizzas(Resource):
    def get(self):
        
        restau_pizza = RestaurantPizza.query.all()
        restau_pizza_list = [rest_pizza.to_dict() for rest_pizza in restau_pizza ]
        return make_response(restau_pizza_list,200)
        
    def post(self):
       try:
            incoming = request.get_json()
            
            new_rest_piz = RestaurantPizza(**incoming)
            db.session.add(new_rest_piz)
            db.session.commit()
            return make_response(new_rest_piz.to_dict(),201)
       except ValueError:
            return make_response({"errors": ["validation errors"]},400)
       


api.add_resource(Restaurants,"/restaurants")
api.add_resource(RestaurantById,"/restaurants/<int:id>")
api.add_resource(RestaurantPizzas,"/restaurant_pizzas")
api.add_resource(Pizzas,'/pizzas')

if __name__ == "__main__":
    app.run(port=5555, debug=True)