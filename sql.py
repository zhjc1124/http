# -*- coding: utf8-*-
import pymysql.cursors
connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             password='zhang19981124',
                             db='http',
                             charset='utf8')


def save_info(username, lng, lat, location):
    with connection.cursor() as cursor:
        sql = 'INSERT INTO info(username, lng, lat, location) VALUES (%s, %s, %s, %s)'
        cursor.execute(sql, (username, lng, lat, location))
        connection.commit()