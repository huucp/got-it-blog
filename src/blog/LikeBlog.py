from flask_restful import Resource, reqparse

from Utils import *
from db.DbUtils import *
from db.MySqlConnectionPool import MySQLConnectionPool


class LikeBlog(Resource):
    def __init__(self):
        self._connection_pool = MySQLConnectionPool()
        self._parser = reqparse.RequestParser()
        self._parser.add_argument('user-id')
        self._parser.add_argument('blog-id')



    def get(self):
        args = self._parser.parse_args()
        user_id = args['user-id']
        blog_id = args['blog-id']
        if not validateParams(user_id) or not validateParams(blog_id):
            return {'like blog error', 'params is invalid'}
        else:
            user = getUserInfo(user_id, self._connection_pool)
            if len(user) == 0:
                return {'user error': 'this user is not exist!'}
            if not validUser(user[0]):
                return {'user info error': 'please update user info first'}
            if self.like(user_id, blog_id):
                return {'like blog': 'successful'}
            else:
                return {'like blog': 'fail'}

    def like(self, user_id, blog_id):
        sql = "insert into like_tbl (id,user_id, blog_id) values (null,'{}',{})".format(user_id, blog_id)
        try:
            self._connection_pool.execute(sql, commit=True)
            return True
        except:  # TODO: catch sql error here
            return False
