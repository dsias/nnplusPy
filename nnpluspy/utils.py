#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Sun Dec 16 09:01:41 2012


import os
import re

from nnpluspy import WWW_DIR


def get_config_php(req_settings):
    """ retrieves the settings set in www/config.php """
    setting_rgx = re.compile(r"^define\('([(A-Z_]+)', '?([a-zA-Z0-9_.-]*)'?\);")
    config_php = {}
    try:
        with open(os.path.join(WWW_DIR, 'config.php'), 'r') as f:
                for l in f.readlines():
                    setting_line = re.match(setting_rgx, l)
                    if setting_line:
                        setting, value = setting_line.groups()
                        if setting in req_settings:
                            config_php.update({setting.lower(): value})

    except IOError:
        return

    return config_php
