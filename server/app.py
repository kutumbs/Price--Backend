from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, unset_jwt_cookies
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
from model import db, User, Product, Store, ProductStore;
from flask_migrate import Migrate;
import os

from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PriceHunter.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pricehunter_database_user:0HwKdAmMDR47cJDhftcSFVrcjILPTWpg@dpg-cp5h5a8cmk4c73f22eng-a.oregon-postgres.render.com/price_hunter_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '3dcc58af5f6d3a346e7a493c08bea722271ae47c4ac0d4fc76b984dc441ebc20' 

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)
CORS(app)


class UserRegister(Resource):
    @cross_origin()
    def post (self):
        data = request.get_json()
        print(data)
        name = data.get("name")
        email = data.get("email")
        password = str(data.get("password"))
        
        
        print(f"This is {data}")
        
        #check if the user exists
        user_exists = User.query.filter(User.name==name) 
        
        # if user_exists:
        #     return jsonify({"Error":"User exists"})
        
        # if password and confirm_password doesn't match
        # if password != confirm_password:
        #     return jsonify({"Error":"Password and confirm_password don't match"})
        
        # creating encrypted passwords
        hashed_password = bcrypt.generate_password_hash(password)
       
        
        access_token = create_access_token(identity=name)
        # User.access_token = access_token
        
        new_user = User(
           name = name,
           email = email,
           password = hashed_password,
            
        )
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            "id":"new_user.id",
            "name":"new_user.name",
            "access_token":access_token
            
        })
        
api.add_resource(UserRegister,"/user/register")

class UserLogin(Resource):
    def post(self):
        data = request.get_json()[0]
        print(data)
       
        email = data.get("email")
        password = str(data.get("password"))

        user = User.query.filter_by(email=email).first()

        if user is None:
            return jsonify({'error': 'Unauthorized'}), 401

        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({'error': 'Unauthorized, incorrect password'}), 401
       
        access_token = create_access_token(identity=email)
        user.access_token = access_token


        return jsonify({
            "id": user.id,
            "email": user.email,
            "access_token": user.access_token,
       
        })
       
api.add_resource(UserLogin,"/user/login")  

class UserByID(Resource):

    def get(self,id):
        user = User.query.filter(User.id==id).first()

        if user:
            return make_response(jsonify(user.to_dict(only=("id","name","email",))),200) 

    def patch(self,id):

        data = request.get_json()[0]

        user = User.query.filter(User.id==id).first()

        for attr in data:
            setattr(user,attr,data.get(attr))

        db.session.add(user)
        db.session.commit()

        return make_response(user.to_dict(only=("id","email","name",)),200)

    def delete(self,id):

        user = User.query.filter(User.id==id).first()

        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response("",204)
        else:
            return make_response(jsonify({"error":"User not found"}),404) 
        
api.add_resource(UserByID,"/users/<int:id>") 

class Products(Resource):
    def get(self):
        products = [product.to_dict(only=('id', 'name', "rating", 'price', 'image_url','user_id','product_stores.store_id'
)) for product in Product.query.all()]
        return make_response(jsonify(products), 200)

    def post(self):
        data = request.get_json()[0]
        new_product = Product(
            name=data.get("name"),
            rating=data.get("rating"),
            price=data.get("price"),
            image_url=data.get("image_url"),
            user_id=data.get("user_id")
        )
        db.session.add(new_product)
        db.session.commit()
        return make_response(new_product.to_dict(only=("name", "image_url", "price")))
    

class ProductByID(Resource):
      def get(self, id):
            product = Product.query.filter(Product.id==id).first()
            if product:
                
                return jsonify({
                    "id": product.id,
                    "name": product.name,
                    "rating": product.rating,
                    "price": product.price,
                    "image_url": product.image_url,
                    "user_id": product.user_id 
                })
            else:
               
                return jsonify({"error": "Product not found"}), 404
            

class Stores(Resource):
    def get(self):
        stores = [store.to_dict(only=("name","product")) for store in Store.query.all()]
        return make_response(jsonify(stores), 200)
    

class ProductStores(Resource):
    def post(self):
        data =  request.get_json()[0]
        
       
        
        try:
            new_product_store = ProductStore(
                store_id= data.get('store_id'),
                product_id = data.get('product_id'),
                
                
            )  
            db.session.add(new_product_store)
            db.session.commit() 
            
        except ValueError:
            return make_response(jsonify({"error":["validation errors"]}))    
        
        return make_response(new_product_store.to_dict(),201)
    
api.add_resource(ProductStores,"/productstore") 



            



api.add_resource(Products, "/products")
api.add_resource(Stores, "/stores")
api.add_resource(ProductByID, "/product/<int:id>")
        






if __name__ == '__main__':
    app.run(debug=True)