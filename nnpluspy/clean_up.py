#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Sun Dec 16 14:42:07 2012


import logging

from nnpluspy import releases, db


logging.getLogger(__name__)


def remove_disabled_categories():
    """
    This function permanently removes all releases not belonging to any
    of the currently activated categories.
    """
    # Get the active categories
    cur = db.connect()
    query = "SELECT ID FROM category WHERE status=1"
    actv_cats = [int(c) for c in cur.select(query, unpack=True)]
    cur.close()

    # Get target releases
    tbd_releases = releases.get_releases_strict({'categoryID': actv_cats},
                                                negate=True)

    # Remove releases
    logging.info("Marked {} releases for removal.".format(len(tbd_releases)))
    releases.delete_releases(tbd_releases)
