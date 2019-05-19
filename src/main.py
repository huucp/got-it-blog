from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from src.HelloWorld import Home
from src.user.UserRegister import UserRegister

app = Flask(__name__)
api = Api(app)

api.add_resource(Home, '/')
api.add_resource(UserRegister, '/user-register/<user_id>')
# api.add_resource(UserRegister, '/todos/<todo_id>')

if __name__ == '__main__':
    app.run(debug=True)

