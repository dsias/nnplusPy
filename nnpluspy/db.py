#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Tue Dec 11 22:44:47 2012

import MySQLdb
import logging


from nnpluspy.utils import get_config_php


logging.getLogger(__name__)


class DBConnection():
    def __init__(self, db_password, db_user, db_name, host='archsrv'):
        logging.info("Connecting to the database: {db_user}' @ '{db_name}'".format(
            db_user=db_user, db_name=db_name))

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

    def action(self, query, args=None, dry_run=False):
        logging.info("Query: {query} {args}".format(query=query, args=args))

        if args is None:
            self.cur.execute(query)
        else:
            self.cur.execute(query, args)

        return self.cur

    def select(self, query, args=None):
        logging.debug(query)
        self.cur.execute(query, args)
        sqlResult = self.cur.fetchall()

        # Unpack results
        return sqlResult

    def delete(self, table, where_dict):
        gen_params = lambda myDict: [x + "=%s" for x in myDict.keys()]
        query = "DELETE FROM " + table + " WHERE " + " AND ".join(gen_params(where_dict))

        sqlResult = self.action(query, where_dict.values())

        return sqlResult

    def update(self, table, value_dict, key_dict):
        gen_params = lambda myDict: [x + "=%s" for x in myDict.keys()]
        query = "UPDATE " + table + " SET " + ", ".join(gen_params(value_dict))\
                + " WHERE " + " AND ".join(gen_params(key_dict))
        sqlResult = self.action(query, value_dict.values() + key_dict.values())

        return sqlResult

    def close(self):
        logging.info("Closed connection to database.")
        self.con.close()


def connect():
    con = DBConnection(**get_config_php(['DB_PASSWORD', 'DB_USER', 'DB_NAME']))

    return con
