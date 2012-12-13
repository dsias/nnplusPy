#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Wed Dec 12 22:48:54 2012

import os

from nnpluspy import db
from nnpluspy import WWW_DIR


def delete_release(release):
    con = db.connect()

    # Remove from disk
    nzb_base_path = con.select("SELECT value FROM site WHERE setting='nzbpath'")[0][0]
    audio_base_path = os.path.join(WWW_DIR, 'covers', 'audio')
    img_base_path = os.path.join(WWW_DIR, 'covers', 'preview')

    if release.guid:
        files = [
            os.path.join(nzb_base_path, release.guid[0], release.guid + '.nzb.gz'),
            os.path.join(audio_base_path, release.guid[0], release.guid + '.mp3'),
            os.path.join(img_base_path, release.guid + '_thumb.jpg')
        ]
    else:
        files = [
            os.path.join(nzb_base_path, release.rid[0], release.rid + '.nzb.gz'),
            os.path.join(audio_base_path, release.rid[0], release.rid + '.mp3')
        ]

    try:
        os.remove(nzb_path)
        os.remove(audio_path)
    except IOError:
        pass

    # Remove from database
    """
    DELETE FROM releasefiles WHERE releaseID '%s'

    DELETE FROM releasecomment WHERE releaseID '%s'
    UPDATE releases SET comments = (select count(ID) from releasecomment WHERE
    releasecomment.releaseID = '%d')
    WHERE releases.ID = '%d', rid, rid

    DELETE FROM (releaseaudio, releasesubs, releaseextrafull, releasevideo) releaseid




    """














def get_releases_by_id(release_ids, query_filter=None):
    con = db.connect()
    gen_keys = lambda myDict: [x + "=?" for x in myDict.keys()]
    query = "SELECT * FROM releases WHERE id IN({})".format(
            str(release_ids).strip('[]'))

    if query_filter:
        query += " AND " + " AND ".join(gen_keys(query_filter))

        sqlResult = con.select(query, query_filter.values())
    else:
        sqlResult = con.select(query)

    con.close_db()

    return [Release(x) for x in sqlResult]


def get_releases_by_name(release_name, query_filter=None, strict=False):
    con = db.connect()
    gen_keys = lambda myDict: [k + "=" + v for k, v in myDict.iteritems()]

    if strict:
        strictness = "="
    else:
        release_name = "%{}%".format(release_name)
        strictness = "LIKE"

    query = "SELECT * FROM releases WHERE name {strictness} %s".format(
            strictness=strictness)

    if query_filter:
        query += " AND " + " AND ".join(gen_keys(query_filter))
        sqlResult = con.select(query, (release_name,))
    else:
        sqlResult = con.select(query, (release_name,))

    con.close_db()

    return [Release(x) for x in sqlResult]


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
