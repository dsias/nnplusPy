#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Tue Jan  1 21:27:47 2013

import logging

import sqlsoup

from nnpluspy import config

logger = logging.getLogger('nnpluspy.database')


def get_db():
    url = 'mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'.format(**vars(config))
    db = sqlsoup.SQLSoup(url)
    logger.info('mysql_db->{}.'.format(url))

    return db
