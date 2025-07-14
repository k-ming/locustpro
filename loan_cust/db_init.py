import json

import pymysql
from pymysql import connect
# from db_config import FAT_CUST

class MySQLClient:
    def __init__(self, db):
        self.cursor = None
        try:
            self.conn = connect(**db)
            # print(self.conn)
            # self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor) #查询的时候显示字段名
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise e

    def query(self, sql, *args):
        """
        :param sql: 查询语句
        :param args: 查询语句中参数，防止sql注入，传值时，可直接传入tuple，程序自动取sql=tuple[0], 参数为tuple[0:]
        :return: 查询结果
        """
        try:
            self.cursor.execute(sql, args)
            # print('sql语句：',sql, '参数:', args)
            res = self.cursor.fetchall()
            return res
            # print(result)
        except Exception as e:
            raise e

    def querymany(self, sql, *args):
        """ 查询多条语句
        :param sql:
        :param args:
        :return:
        """
        try:
            self.cursor.executemany(sql, args)
            res = self.cursor.fetchmany()
            return res
        except Exception as e:
            raise e

    def execute(self, sql, *args):
        """
        :param sql: 要执行的语句
        :param args: 执行语句中的参数，防止sql注入
        :return: 影响的行数
        """
        try:
            res = self.cursor.execute(sql, args)
            # res = self.cursor.fetchall()
            self.conn.commit()
            return res
        except Exception as e:
            raise e

    def close(self):
        """
        : 关闭连接
        """
        self.cursor.close()
        self.conn.close()


# if __name__ == '__main__':
#     cust = MySQLClient(FAT_CUST)
#     sql1 = ("select email from cust_personal_info where cust_no=%s", '800000065501', )
#     result = cust.query(*sql1)
#     print(result[0][0])
    # sql2 = ('delete from cust_work_info where cust_no=%s', '800000031502')
    # result2 = cust.execute(*sql2)
    # print(result2)
    # sql3 = 'SELECT * FROM cust_account_info where mobile_no=%s'
    # params = [('8100000006'), ('8100000021',)]
    # result3 = cust.querymany(sql3, params)
    # print(result3)
    # cust.close()

