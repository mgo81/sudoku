#!flask/bin/python
import pymysql.cursors
from DBUtils.PersistentDB import PersistentDB

dbConn = None

def connect_db():
    return PersistentDB(
        creator=pymysql,  # the rest keyword arguments belong to pymysql
        user='root',
        password='',
        database='Sudoku',
        autocommit=True,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)


def get_db():
    global dbConn

    if not dbConn:
        dbConn = connect_db()
    return dbConn.connection()

def query(sql, values=None):
    global dbConn

    with get_db().cursor() as cursor:
        if values:
            cursor.execute(sql, values)
            result = cursor.fetchall()
        else:
            cursor.execute(sql)
            result = cursor.fetchall()

    return result