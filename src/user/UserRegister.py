from src.db.MySqlConnectionPool import MySQLConnectionPool
from src.Const import Const
from flask_restful import reqparse, abort, Api, Resource
from flask import Flask


class UserRegister(Resource):

    def __init__(self):
        self._connection_pool = MySQLConnectionPool()
        self._parser = reqparse.RequestParser()
        self._parser.add_argument('user-type')

    def get(self, user_id):
        args = self._parser.parse_args()
        user_type = args['user-type']
        if user_type is None or (user_type != Const.USER_TYPE_FB and user_type != Const.USER_TYPE_GG):
            return {'register error': 'wrong user-type {}'.format(user_type)}, 200
        user = self.getUserInfo(user_id)
        if len(user) == 0:
            ret = self.register(user_id, user_type)
            if ret:
                return {"register": "successful"}
            else:
                return {"register": "fail"}
        else:
            current_user = user[0]
            if user_type != current_user[2]:
                return {"login error": "please login with account {}".format(current_user[2])}, 200
            else:
                return {"login successful": "hooray"}, 200

    def getUserInfo(self, user_id):
        sql = "select * from user_info where user_id='{}'".format(user_id)
        result = self._connection_pool.execute(sql)
        return result

    def register(self, user_id, user_type):
        sql = "insert into user_info (id, user_id, user_type) values (null,'{}','{}')".format(user_id, user_type)
        try:
            self._connection_pool.execute(sql, commit=True)
        except:
            return False
        return True
