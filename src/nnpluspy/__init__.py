#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Wed Dec 12 18:45:23 2012

import logging
import re
import os


# the www dir has to be specified before we can begin:
WWW_DIR = '/srv/http/nnplus/www'

logger = logging.getLogger('nnpluspy')
logger.setLevel(logging.DEBUG)
frmt = logging.Formatter(
    '[%(asctime)s] %(module)-8s %(levelname)s :: %(message)s', '%H:%M:%S'
)
fh = logging.FileHandler('nnpluspy.log', 'w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(frmt)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(frmt)
logger.addHandler(fh)
logger.addHandler(ch)


class Struct(object):
    def __init__(self):
        self.WWW_DIR = WWW_DIR
        # retrieve and parse settings from config.php
        setting_rgx = re.compile(r"define\('([(A-Z_]+)', '?([a-zA-Z0-9_.-]*)'?\);")
        SETTING, VALUE = 0, 1
        try:
            with open(os.path.join(self.WWW_DIR, 'config.php'), 'r') as f:
                for s in re.findall(setting_rgx, f.read()):
                    setattr(self, s[SETTING], s[VALUE])
        except IOError, e:
            logging.ERROR(e)

        self.DB_HOST = 'archsrv'

config = Struct()
