# -*- coding: utf8-*-
import pymysql.cursors
connection = pymysql.connect(host='127.0.0.1',
                             port=3306,
                             user='root',
                             password='qwerty7620',
                             db='http',
                             charset='utf8')
with connection.cursor() as cursor:
    sql = 'INSERT INTO info(username, lng, lat, location) VALUES (%s, %s, %s, %s)'
    cursor.execute(sql, ('lc', 43, 45.3, '122233'))
    connection.commit()