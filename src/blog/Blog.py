from flask_restful import Resource, reqparse

from db.DbUtils import *
from db.MySqlConnectionPool import MySQLConnectionPool


class Blog(Resource):
    def __init__(self):
        self._connection_pool = MySQLConnectionPool()
        self._parser = reqparse.RequestParser()
        self._parser.add_argument('user-id')
        self._parser.add_argument('blog-title')
        self._parser.add_argument('blog-content')

    def post(self):
        args = self._parser.parse_args()
        user_id = args['user-id']
        if user_id is None:
            return {'post blog error': 'wrong user id'}
        user = getUserInfo(user_id, self._connection_pool)
        if len(user) == 0:
            return {'post blog  error': 'user is not registered, please register by FB or GG first!'}
        if not validUser(user[0]):
            return {'user info error': 'please update user info first'}

        blog_title = args['blog-title']
        blog_content = args['blog-content']
        if blog_title is None or len(str(blog_title)) == 0:
            return {'post blog error': 'title cannot be null or empty'}
        else:
            if self.addBlog(user_id, blog_title, blog_content):
                return {'post blog': 'successful'}
            else:
                return {'post blog': 'fail'}

    def addBlog(self, user_id, blog_title, blog_content):
        sql = "insert into blog (id, user_id, title, content) values (null,'{}','{}','{}')" \
            .format(user_id, blog_title, blog_content)
        try:
            self._connection_pool.execute(sql, commit=True)
            return True
        except:  # TODO: catch sql error here
            return False
