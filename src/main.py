from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from HelloWorld import Home
from blog.Likes import Likes
from blog.HomePage import HomePage
from user.UserRegister import UserRegister
from user.UserInfo import UserInfo
from blog.Blog import Blog
from blog.LikeBlog import LikeBlog

app = Flask(__name__)
api = Api(app)

api.add_resource(Home, '/')
api.add_resource(UserRegister, '/user-register/<user_id>')
api.add_resource(UserInfo, '/user-info/<user_id>')
api.add_resource(Blog, '/blog')
api.add_resource(LikeBlog, '/like')
api.add_resource(HomePage, '/home')
api.add_resource(Likes, '/like-list/<blog_id>')
if __name__ == '__main__':
    app.run(debug=False)

