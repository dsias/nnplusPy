#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Tue Dec 11 22:44:47 2012


import MySQLdb
import re


class DBConnection():
    def __init__(self, db_password, db_user, db_name):
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
        sql_result = self.action(query, args)

        return sql_result.fetchall()

    def update(self, table, value_dict, key_dict):
        gen_params = lambda myDict: [x + "=%s" for x in myDict.keys()]

        query = "UPDATE " + table + " SET " + ", ".join(gen_params(value_dict))\
                + " WHERE " + " AND ".join(gen_params(key_dict))

        self.action(query, value_dict.values() + key_dict.values())


def connect():
    "Reads config.php and returns a db connection instance."
    setting_rgx = re.compile(r"^define\('([(A-Z_]+)', '(.*)'\);")
    settings_dict = {
        'DB_USER': None,
        'DB_PASSWORD': None,
        'DB_NAME': None
    }

    try:
        with open('/srv/http/nnplus/www/config.php', 'r') as f:

                for l in f.readlines():
                    setting_line = re.match(setting_rgx, l)
                    if setting_line:
                        setting, value = setting_line.groups()
                        if setting in settings_dict:
                            del settings_dict[setting]
                            settings_dict[setting.lower()] = value
    except IOError, e:
        print e
        return 1

    db = DBConnection(**settings_dict)

    return db
