#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Wed Dec 12 18:45:23 2012


"""
nnpluspy.nnplus_config
~~~~~~~~~~~~~~~~~~~~~~

This module is used to access (and modify) settings defined in config.php.

"""

import os
import re

from nnpluspy import NNPLUS_WWW


setting_rgx = re.compile(r"^define\('([(A-Z_]+)', '?([a-zA-Z0-9_.-]*)'?\);")
settings_dict = {
    'DB_TYPE': None,
    'DB_HOST': None,
    'DB_USER': None,
    'DB_PASSWORD': None,
    'DB_NAME': None,
    'DB_PCONNECT': None,
    'NNTP_USERNAME': None,
    'NNTP_PASSWORD': None,
    'NNTP_SERVER': None,
    'NNTP_PORT': None,
    'NNTP_SSLENABLED': None,
    'CACHEOPT_METHOD': None,
    'CACHEOPT_TTLFAST': None,
    'CACHEOPT_TTLMEDIUM': None,
    'CACHEOPT_TTLSLOW': None,
    'CACHEOPT_MEMCACHE_SERVER': None,
    'CACHEOPT_MEMCACHE_PORT': None,
}


def get_config_php(req_settings):
    """ retrieves the settings set in www/config.php """
    _settings_dict = {}
    try:
        with open(os.path.join(NNPLUS_WWW, 'config.php'), 'r') as f:
                for l in f.readlines():
                    setting_line = re.match(setting_rgx, l)
                    if setting_line:
                        setting, value = setting_line.groups()
                        if setting in req_settings:
                            _settings_dict[setting.lower()] = value
    except IOError:
        return

    return _settings_dict
