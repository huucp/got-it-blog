from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from src.HelloWorld import Home
from src.blog.Likes import Likes
from src.blog.HomePage import HomePage
from src.user.UserRegister import UserRegister
from src.user.UserInfo import UserInfo
from src.blog.Blog import Blog
from src.blog.LikeBlog import LikeBlog

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
    app.run(debug=True)

