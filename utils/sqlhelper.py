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


class SqlHelper:
    def __init__(self):
        self.conn()

    def conn(self):
        self.conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='test',
                                    charset='utf8')
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def get_list(self, sql, args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchall()
        return result

    def get_one(self, sql, args):
        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def modify(self, sql, args):
        self.cursor.execute(sql, args)
        self.conn.commit()

    def multiple_modify(self, sql, args):
        self.cursor.executemany(sql, args)
        self.conn.commit()

    def create(self, sql, args):
        self.cursor.execute(sql, args)
        self.conn.commit()
        return self.cursor.lastrowid

    def close(self):
        self.cursor.close()
        self.conn.close()
