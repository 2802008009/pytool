#! /usr/bin/env python
# -*- coding: utf-8 -*- 

import mysql.connector


class QyDb:
    sql = []
    conn = None
    db = None

    def __init__(self, host, username, password, database, port=3306, charset='utf8', tablePrefix='',
                 raise_on_warnings=True):
        '''
        构造函数
        :param host: 数据库的地址，IP
        :param username: 用户
        :param password: 密码
        :param database: 数据名
        :param port: 端口
        :param charset: 字符编码
        :param tablePrefix: 数表的前缀
        :param raise_on_warnings:
        :return:
        '''
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = int(port)
        self.charset = charset
        self.tablePrefix = tablePrefix
        self.raise_on_warnings = bool(raise_on_warnings)

    def connect(self, force=False):
        if self.conn is None or force is True:
            try:
                self.conn = mysql.connector.connect(host=self.host, user=self.username, password=self.password,
                                                    database=self.database, port=self.port,
                                                    raise_on_warnings=self.raise_on_warnings)
                self.db = self.conn.cursor(dictionary=True, buffered=True)
                if self.charset is not None:
                    self.query(
                        "SET character_set_connection='%s', character_set_results='%s', character_set_client=binary"
                        % (self.charset, self.charset))
            except Exception as err:
                raise Exception, err

        return self.conn

    def reconnect(self):
        if not self.conn.is_connected():
            self.conn.reconnect()

    def count(self, table='', where=None, sql=None):
        count = 0
        if not sql:
            where = where if where else '1=1'
            sql = "SELECT COUNT(1) AS NUM FROM %s WHERE %s" % (
                self.table(table), where)
        self.query(sql)
        rs = self.db.fetchone()
        if rs is not None:
            count = rs.values()[0]
        return count

    def find(self, table='', where=None, field=None, order=None, sql=None):
        if not sql:
            where = where if where else '1=1'
            field = field if field else '*'
            order = ('order by %s' % order) if order else ''
            if type(field) == list:
                field = '`%s`' % ("`,`".join(field))
            sql = "SELECT %s FROM %s WHERE %s %s limit 1" % (
                field, self.table(table), where, order)
        self.query(sql)
        return self.db.fetchone()

    def findAll(self, table='', where=None, field=None, order=None, limit=None, sql=None):
        if not sql:
            where = where if where else '1=1'
            field = field if field else '*'
            if type(field) == list:
                field = '`%s`' % ("`,`".join(field))
            order = ('order by %s' % order) if order else ''
            limit = ('limit %s' % str(limit)) if limit else ''
            sql = "SELECT %s FROM %s WHERE %s %s %s" % (
                field, self.table(table), where, order, limit)
        self.query(sql)
        return self.db.fetchall()

    def findCol(self, table='', where=None, col=None, order=None, sql=None):
        col = col if col else 'id'
        if not sql:
            where = where if where else '1=1'
            order = ('order by %s' % order) if order else ''
            sql = "SELECT %s FROM %s WHERE %s %s" % (
                col, self.table(table), where, order)
        self.query(sql)
        rs = self.db.fetchone()
        result = ''
        if rs is not None:
            result = rs[col]
        return result

    def query(self, sql, params=None):
        self.sql.append(sql)
        if params:
            t = type(params)
            if t == dict:
                return self.db.execute(sql, params)
            elif t == list:
                return self.db.executemany(sql, params)
        return self.db.execute(sql, params)

    def insert(self, table, params):
        field = []
        t = type(params)
        if t == dict:
            field = params.keys()
        elif t == list:
            field = params[0]
            if not isinstance(field, dict):
                raise Exception("error params,need list[dict]")
            field = field.keys()
        else:
            raise Exception("error params,need dict")
        if not field or not isinstance(field, list):
            raise Exception("error params,need dict")
        values = '%({})s'.format(")s,%(".join(field))
        field = '`%s`' % "`,`".join(field)
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (self.table(table), field, values)
        self.query(sql, params)
        self.conn.commit()
        return self.db.lastrowid

    def update(self, table, where, params):
        field = []
        t = type(params)
        if t == dict:
            field = params.keys()
        elif t == list:
            field = params[0]
            if not isinstance(field, dict):
                raise Exception("error params,need list[dict]")
            field = field.keys()
        else:
            raise Exception("error params,need dict")
        if not field or not isinstance(field, list):
            raise Exception("error params,need dict")
        t = []
        for i in field:
            t.append('`{}`=%({})s'.format(i, i))

        sql = "UPDATE %s SET %s WHERE %s" % (self.table(table), ",".join(t), where)
        self.query(sql, params)
        self.conn.commit()
        return True

    def delete(self, table, where, params):
        sql = "DELETE FROM %s WHERE %s" % (self.table(table), where)
        self.query(sql, params)
        self.conn.commit()
        return True

    def sqlLog(self):
        return self.sql

    def close(self):
        self.db.close()
        self.conn.close()

    def table(self, tableName):
        return '%s%s' % (self.tablePrefix, tableName)

    def startStrans(self):
        self.conn.start_transaction()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()


if __name__ == '__main__':
    db = QyDb(host='127.0.0.1', username='username', password='password', database='dbname')
    db.connect()
    
    #查找某一行
    db.find('table', 'condition')

    #查找符合条件的所有行
    db.findAll('table', 'condition')

    #查找某一行的某一个字段
    db.findCol('table', 'condition', 'id')

    #插入数据
    db.insert('table', {'title': 'subject title', 'message':'subject message'})

    #更新数据
    db.update('table', 'id=1', {'title':'', 'message': 'message', 'updated':123456})

    #删除数据
    db.delete('table', 'id=1')
