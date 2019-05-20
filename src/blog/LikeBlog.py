from flask_restful import Resource, reqparse

from src.db.DbUtils import *
from src.Utils import *
from src.db.MySqlConnectionPool import MySQLConnectionPool


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
