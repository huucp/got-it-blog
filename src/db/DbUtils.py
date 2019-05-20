def getUserInfo(user_id, connection):
    sql = "select * from user_info where user_id='{}'".format(user_id)
    result = connection.execute(sql)
    return result
