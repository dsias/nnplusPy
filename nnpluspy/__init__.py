#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Wed Dec 12 18:45:23 2012

import logging

# the www dir has to be specified before we can begin:
WWW_DIR = '/srv/http/nnplus/www'

# Initialize the log
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] %(module)-8s :: %(message)s',
    datefmt='%H:%M:%S')


#NZB_DIR = get_nzb_path()
#AUDIO_DIR = os.path.join(WWW_DIR, 'covers', 'audio')
#IMG_DIR = os.path.join(WWW_DIR, 'covers', 'preview')
