import pymysql


def get_list(sql, args):
    """
    返回查询到的所有结果
    :param sql:
    :param args:
    :return:
    """
    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test', charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 执行sql
    cursor.execute(sql, args)
    # 获取查询到的内容
    ret = cursor.fetchall()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return ret


def get_one(sql, args):
    """
    返回查询到的一条结果
    :param sql:
    :param args:
    :return:
    """
    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test', charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 执行sql
    cursor.execute(sql, args)
    # 获取查询到的内容
    ret = cursor.fetchone()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    return ret


def modify(sql, args):
    """
    修改和删除操作
    :param sql:
    :param args:
    :return:
    """
    # 创建连接
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test', charset='utf8')
    # 创建游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    # 执行sql
    cursor.execute(sql, args)
    # 提交事务
    conn.commit()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()

