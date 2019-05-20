from src.db.MySqlConnectionPool import MySQLConnectionPool
from flask_restful import Resource, reqparse
from src.Utils import *


class Likes(Resource):
    def __init__(self):
        self._connection_pool = MySQLConnectionPool()

    def get(self, blog_id):
        if validateParams(blog_id):
            ret = self.getLikes(blog_id)
            list = []
            if ret is not None:
                list = [row[0] for row in ret]
            dict = {'blog-id': blog_id, 'likes': list}
            return dict, 200
        else:
            return {'get likes error': 'blog id is invalid'}

    def getLikes(self, blog_id):
        sql = 'select user_id from like_tbl'
        try:
            return self._connection_pool.execute(sql)
        except:
            return None
