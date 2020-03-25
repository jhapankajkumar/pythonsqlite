from flask import Flask
from flask_restful import Api, Resource
from security import identity, authenticate
from flask_jwt import JWT, jwt_required
from user import UserRegister

from item import Item, Items


app = Flask(__name__)
api = Api(app)
app.secret_key = 'pankaj' #This must be long and unique

jwt = JWT(app=app,
          identity_handler=identity,
          authentication_handler=authenticate)

@app.route('/')
def home():
    return "Welcome to REST API"


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == "__main__":
    app.run(debug=True)
