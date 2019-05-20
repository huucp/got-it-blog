from flask_restful import Resource, reqparse

from src.Const import Const
from src.db.DbUtils import *
from src.Utils import *
import json
from src.db.MySqlConnectionPool import MySQLConnectionPool


class HomePage(Resource):
    like_query = "select l.blog_id, group_concat(l.user_id) as like_user, m.count " \
                 "from like_tbl l inner join " \
                 "(select blog_id, max(id) as last,min(id) as first, count(1) as count from like_tbl group by blog_id) m " \
                 "on l.blog_id = m.blog_id and (l.id = m.last or l.id=m.first) group by l.blog_id"

    def __init__(self):
        self._connection_pool = MySQLConnectionPool()
        self._parser = reqparse.RequestParser()
        self._parser.add_argument('user-id')
        self._parser.add_argument('blog-id')

    def get(self):
        args = self._parser.parse_args()
        user_id = args['user-id']
        blog_id = args['blog-id']
        if user_id is None and blog_id is None:
            ret = self.getHomePage()
        else:
            if user_id is not None:
                ret = self.getPersonalpage(user_id)
            else:
                ret = self.getBlog(blog_id)

        if ret is None:
            return {'home page error': 'cannot get home page'}
        retDict = []
        for idx in range(len(ret)):
            row = ret[idx]
            like_users = row[2]
            like_count = row[3]
            if like_count > 2:
                like_users += " and {} others".format(like_count - 2)

            content = row[1].strip()
            if len(row[1]) >= Const.CONTENT_LIMIT and user_id is not None:
                content += ' ...'
            retDict.append({'id':row[4],"title": row[0], "content": content, "like": like_users})

        # rs = json.dumps(retDict).strip()
        return {'blog':retDict}

    def getHomePage(self):
        sql = "select title,substr(content,1,{}) as content,lk.like_user,lk.count,id " \
              "from blog b left join " \
              "({}) as lk " \
              "on b.id=lk.blog_id".format(Const.CONTENT_LIMIT, self.like_query)
        try:
            return self._connection_pool.execute(sql)
        except:
            return None

    def getPersonalpage(self, user_id):
        sql = "select title,substr(content,1,{}) as content, lk.like_user,lk.count,id from blog b " \
              "left join ({}) lk on b.id=lk.blog_id " \
              "where b.user_id='{}'".format(Const.CONTENT_LIMIT, self.like_query, user_id)
        try:
            return self._connection_pool.execute(sql)
        except:
            return None

    def getBlog(self, blog_id):
        sql = "select title,content, lk.like_user,lk.count,id from blog b " \
              "left join ({}) lk on b.id=lk.blog_id " \
              "where b.id={}".format(self.like_query, blog_id)
        try:
            return self._connection_pool.execute(sql)
        except:
            return None
