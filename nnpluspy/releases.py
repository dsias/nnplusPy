#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Wed Dec 12 22:48:54 2012

import logging
import os

from nnpluspy import db
from nnpluspy import WWW_DIR

logging.getLogger(__name__)


class Release(object):
    def __init__(self, values):
        COL = {
            'id': 0,
            'name': 1,
            'groupID': 4,
            'size': 5,
            'postdate': 6,
            'adddate': 7,
            'guid': 9,
            'categoryID': 12,
            'rageID': 13,
            'tvdbID': 14
        }

        self.rid = values[COL['id']]
        self.guid = values[COL['guid']]
        self.name = values[COL['name']]
        self.gid = values[COL['groupID']]
        self.size = values[COL['size']]
        self.postdate = values[COL['postdate']]
        self.add_date = values[COL['adddate']]
        self.cid = values[COL['categoryID']]
        self.rageid = values[COL['rageID']]
        self.tvdbid = values[COL['tvdbID']]

    def __repr__(self):
        return "{rid} {name}".format(rid=self.rid, name=self.name)

    def delete(self, nzb_dir=None):
        if not nzb_dir:
            nzb_dir = db.get_nzb_path()
        img_dir = os.path.join(WWW_DIR, 'covers')
        audio_dir = os.path.join(WWW_DIR, 'covers', 'audio')

        if self.guid:
            files = [
                os.path.join(nzb_dir, self.guid[0], self.guid + '.nzb.gz'),
                os.path.join(audio_dir, self.guid[0], self.guid + '.mp3'),
                os.path.join(img_dir, self.guid + '_thumb.jpg')
            ]
        else:
            files = [
                os.path.join(nzb_dir, self.rid[0], self.rid + '.nzb.gz'),
                os.path.join(audio_dir, self.rid[0], self.rid + '.mp3')
            ]

        logging.debug("Removing nzb/cover/audio preview..")
        for f in files:
            try:
                os.remove(f)
            except OSError:
                pass


def delete_releases(releases):
    cur = db.connect()
    nzb_dir = cur.select("SELECT value FROM site WHERE setting='nzbpath'")[0][0]

    for release in releases:
        logging.debug("Deleting release: {release}".format(release=release))
        # Remove static files
        try:
            release.delete(nzb_dir)
        except OSError, e:
            logging.debug(e)

        # Remove releases' database entries
        for table in ('releasenfo', 'releasefiles', 'usercart', 'userdownloads',
                      'releaseaudio', 'releasesubs', 'releaseextrafull',
                      'releasevideo', 'releasecomment', 'releases'):
            if table == 'releases':
                cur.delete(table, {'ID': release.rid})
            else:
                cur.delete(table, {'releaseID': release.rid})

        # Correct comment count
        cur.action("UPDATE releases SET comments = (SELECT count(ID) from releasecomment WHERE "
                   "releasecomment.releaseID = %s) WHERE releases.ID = %s",
                   (release.rid, release.rid,))

    cur.close()


def get_releases_strict(in_dict, negate=False, and_dict=None):
    cur = db.connect()
    gen_keys = lambda myDict: [x + "=?" for x in myDict.keys()]
    negate = 'IN'
    if negate:
        notin = 'NOT ' + negate

    query = "SELECT * FROM releases WHERE {in_query} {notin}({restrict})".format(
            in_query=in_dict.keys()[0],
            notin=notin,
            restrict=str(in_dict.values()[0]).strip('[]'))

    if and_dict:
        query += " AND " + " AND ".join(gen_keys(and_dict))

        sqlResult = cur.select(query, and_dict.values())
    else:
        sqlResult = cur.select(query)

    cur.close()

    return [Release(x) for x in sqlResult]


def get_releases_filter(where_dict, and_dict=None):
    cur = db.connect()
    gen_keys = lambda myDict: [k + "=" + v for k, v in myDict.iteritems()]

    # 'Encapsulate' query for fuzzy search
    query = "SELECT * FROM releases WHERE {like_query} LIKE {restrict}".format(
            like_query=where_dict.keys()[0],
            restrict="'%{}%'".format(where_dict.values()[0]))

    if and_dict:
        query += " AND " + " AND ".join(gen_keys(and_dict))

    sqlResult = cur.select(query)

    cur.close()

    return [Release(x) for x in sqlResult]
