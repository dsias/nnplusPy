#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Tue Dec 11 22:44:47 2012


import MySQLdb

from nnpluspy.nnplus_config import get_settings


class DBConnection():
    def __init__(self, db_password, db_user, db_name, host='archsrv'):
        if host:
            self.con = MySQLdb.connect(user=db_user,
                                       passwd=db_password,
                                       db=db_name,
                                       host=host)
        else:
            self.con = MySQLdb.connect(user=db_user,
                                       passwd=db_password,
                                       db=db_name)

        self.cur = self.con.cursor()

    def action(self, query, args=None):

        if args is None:
            self.cur.execute(query)
        else:
            self.cur.execute(query, args)

        return self.cur

    def select(self, query, args=None):
        self.cur.execute(query, args)

        return self.cur.fetchall()

    def update(self, table, value_dict, key_dict):
        gen_params = lambda myDict: [x + "=%s" for x in myDict.keys()]

        query = "UPDATE " + table + " SET " + ", ".join(gen_params(value_dict))\
                + " WHERE " + " AND ".join(gen_params(key_dict))

        self.action(query, value_dict.values() + key_dict.values())


def connect():

    db = DBConnection(**get_settings(['DB_PASSWORD', 'DB_USER', 'DB_NAME']))

    return db

