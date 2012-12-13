#!/usr/bin/env python
# encoding: utf-8
# daanmathot@gmail.com
# Wed Dec 12 22:48:54 2012

from nnpluspy import db


def delete_release(releases):
    pass


def get_releases_by_id(release_ids, query_filter=None):
    con = db.connect()
    gen_keys = lambda myDict: [x + "=?" for x in myDict.keys()]
    query = "SELECT * FROM releases WHERE id IN({})".format(
            str(release_ids).strip('[]'))

    if query_filter:
        query += " AND " + " AND ".join(gen_keys(query_filter))

        return con.select(query, query_filter.values())

    else:

        return con.select(query)


def get_releases_by_name(release_name, query_filter=None, strict=False):
    con = db.connect()
    gen_keys = lambda myDict: [k + "=" + v for k, v in myDict.iteritems()]
    if strict:
        strictness = "="
    else:
        release_name = "%{}%".format(release_name)
        strictness = "LIKE"

    query = "SELECT * FROM releases WHERE name {strictness} '{release_name}'".format(
            strictness=strictness,
            release_name=release_name)

    if query_filter:
        query += " AND " + " AND ".join(gen_keys(query_filter))
        sqlResult = con.select(query, query_filter.values().insert(0, release_name))
    else:
        sqlResult = con.select(query, release_name)

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
            'categoryID': 12,
            'rageID': 13,
            'tvdbID': 14
        }

        self.rid = values[COL['id']]
        self.name = values[COL['name']]
        self.gid = values[COL['groupID']]
        self.size = values[COL['size']]
        self.postdate = values[COL['postdate']]
        self.add_date = values[COL['adddate']]
        self.cid = values[COL['categoryID']]
        self.rageid = values[COL['rageID']]
        self.tvdbid = values[COL['tvdbID']]
