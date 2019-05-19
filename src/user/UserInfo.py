from flask_restful import Resource, reqparse

from src.Const import Const
from src.db.MySqlConnectionPool import MySQLConnectionPool


class UserInfo(Resource):
    def __init__(self):
        self._connection_pool = MySQLConnectionPool()
        self._parser = reqparse.RequestParser()
        self._parser.add_argument('user-name')
        self._parser.add_argument('user-phone')
        self._parser.add_argument('user-job')
        self._parser.add_argument('other-job')

    def get(self, user_id):
        args = self._parser.parse_args()
        user_name = args['user-name']
        user_phone = args['user-phone']
        user_job = args['user-job']
        other_job = args['other-job']
        user = self.getUserInfo(user_id)
        if len(user) == 0:
            return {'user info error': 'user is not registered, please register by FB or GG first!'}

        if user_name is None:
            return {'user info': user[0]}

        user_type = user[0][2]

        if user_type is None or (user_type != Const.USER_TYPE_FB and user_type != Const.USER_TYPE_GG):
            return {'user info error': 'wrong user-type {}'.format(user_type)}, 200

        if user_type == Const.USER_TYPE_FB:
            if self.validFbUser(user_name, user_phone):
                if self.addFbUserInfo(user_id, user_name, user_phone):
                    return {'user info': 'update info successfully'}
                else:
                    return {'user info': 'fail to update info, please try again'}
            else:
                return {'user info error': 'user name or user phone is wrong'}
        else:
            if self.validGGUser(user_name, user_job, other_job):
                if self.updateGGUserInfo(user_id, user_name, user_job, other_job):
                    return {'user info': 'update info successfully'}
                else:
                    return {'user info': 'fail to update info, please try again'}
            else:
                return {'user info error': 'user name or user job is wrong'}

    def validFbUser(self, name, phone):
        return name is not None and len(str(name)) > 0 and phone is not None and len(str(phone)) > 0

    def getUserInfo(self, user_id):
        sql = "select * from user_info where user_id='{}'".format(user_id)
        result = self._connection_pool.execute(sql)
        return result

    def addFbUserInfo(self, id, name, phone):
        sql = "update user_info set user_name='{}', user_phone='{}' where user_id='{}'".format(name, phone, id)
        try:
            self._connection_pool.execute(sql, commit=True)
            return True
        except:  # TODO: catch sql error here
            return False

    def validGGUser(self, name, jobType, otherJob):
        if name is None or len(str(name)) == 0:
            return False
        if jobType is None or (
                jobType != Const.JOB_STUDENT and jobType != Const.JOB_TEACHER and jobType != Const.JOB_OTHER):
            return False
        if jobType == Const.JOB_OTHER and (otherJob is None or len(str(otherJob)) == 0):
            return False
        return True

    def updateGGUserInfo(self, id, name, jobType, otherJob):
        if jobType == Const.JOB_OTHER:
            sql = "update user_info set user_name='{}', user_job_type='{}', user_job_other='{}' where user_id='{}'" \
                .format(name, jobType, otherJob, id)
        else:
            sql = "update user_info set user_name='{}', user_job_type='{}' where user_id='{}'".format(name, jobType, id)
        try:
            self._connection_pool.execute(sql, commit=True)
            return True
        except:  # TODO: catch sql error here
            return False
