from Const import Const


def getUserInfo(user_id, connection):
    sql = "select * from user_info where user_id='{}'".format(user_id)
    result = connection.execute(sql)
    return result


def validUser(user_info):
    if user_info[3] is None:
        return False
    user_type = user_info[2]
    if user_type == Const.USER_TYPE_FB:
        if user_info[4] is None:
            return False
    else:
        if user_info[5] is None:
            return False
        if user_info[5] == Const.JOB_OTHER and user_info[6] is None:
            return False
    return True
