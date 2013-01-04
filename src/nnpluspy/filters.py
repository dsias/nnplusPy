# -*- coding: utf-8 -*-
# dydrmntion@gmail.com ~ 2013

"""
nnpluspy.filterreleases
~~~~~~~~~~~~~~~~
This class deletes releases that match the criteria for one or more of
the following filters:
    - german: removes german releases
    - inactive: removes releases belonging to inactive categories
    - movies_oldies: removes movie releases from before the year n
    - movies_lowrating: removes movie releases with a (imdb) rating lower than n

"""

import re
import logging
import os

from nnpluspy.db import get_db
from nnpluspy import config


GERMAN, INACTIVE, OLDIES, LOWRATING = 'german', 'inactive', 'oldies', 'lowrating'


class Filters(object):

    def __init__(self):
        """
        Deletes releases matching the requested method's filter criteria.

        """
        self.logger = logging.getLogger('nnpluspy.FilterReleases')
        self.db = get_db()

    def german(self):
        """
        Yields releases marked as german by this filter

        Returns:
            release.ID
        """
        rgx_name = re.compile(r'(\W(das|der|ger|german|um|und|im|des|de|deutch)\W)', re.IGNORECASE)
        rgx_nfo = re.compile(r'(\W(das|der|um|und|im|des|deutch)\W)', re.IGNORECASE)
        nfo_sql = 'SELECT uncompress(nfo) as nfo FROM releasenfo where releaseID = %s'

        for release in self.db.releases.all():
            query = self.db.execute(nfo_sql % release.ID)
            nfo = query.fetchone()
            is_foreign = re.search(rgx_name, release.name)

            if is_foreign:
                match = is_foreign.group(2)
                # Make sure its not a multilingual release:
                if re.search(r'\W(english|eng)\W', release.name, re.IGNORECASE):
                    self.logger.debug('german->name->multilingual->{}'.format(release.name))
                # Or not a language designation
                elif match.lower() == 'de' and match != 'DE':
                    self.logger.debug('german->name->false positive->{}'.format(release.name))
                else:
                    self.logger.debug('german->name->{}->{}'.format(release.name, match))

                    yield release

            elif nfo:
                # dont yield english albums released by german scene group
                if release.categoryID not in ['3010', '3040']:
                    try:
                        is_foreign = re.search(rgx_nfo, nfo[0])
                    except TypeError:
                        self.logger.debug('error->corrupt nfo->ID: {}.'.format(release.ID))
                        is_foreign = None
                    if is_foreign:
                        self.logger.debug('german->nfo->{}->{}'.format(release.name, is_foreign.group(2)))

                        yield release

    def oldies(self, min_year=1960):
        """
        Yields movie releases older than min_year.

        Args:
            min_year(int)

        Returns:
            release.ID
        """
        for movie in self.db.movieinfo.all():
            if movie.year and int(movie.year) < min_year:
                query = self.db.releases.filter_by(imdbID=movie.imdbID)
                if query.count():
                    for release in query:
                        self.logger.debug('movie_oldies->{}->{}.'.format(release.name, movie.year))

                        yield release

    def lowrating(self, min_rating=4):
        """
        This filter yields movie releases with a rating lower than min_rating

        Args:
            min_rating(int)

        Returns:
            release.ID
        """
        where = self.db.session.query(self.db.movieinfo.imdbID).filter(self.db.movieinfo.rating < min_rating)
        for release in self.db.session.query(self.db.releases).filter(
                self.db.releases.imdbID.in_(where)).all():
            self.logger.debug('movie_lowrating->{}.'.format(release.name))

            yield release

    def inactive(self):
        """
        Yields releases belonging to inactive categories

        Returns:
            release.ID
        """
        where = self.db.session.query(self.db.category.ID).filter_by(status=1)
        for release in self.db.session.query(self.db.releases).filter(
                ~self.db.releases.categoryID.in_(where)).all():
            self.logger.debug('inactive_category->{}->{}.'.format(
                release.categoryID, release.name))

            yield release

    def delete_release(self, release):
        # Delete from database
        self.logger.info('delete->{}'.format(release.name))
        for name in ('releasenfo', 'releasefiles', 'usercart', 'userdownloads', 'releaseaudio',
                     'releasesubs', 'releaseextrafull', 'releasevideo', 'releasecomment',
                     'releases'):

            table = self.db.entity(name)
            if name == 'releases':
                self.logger.debug('-->self.db drop row->{}->{}.'.format(name, release.ID))
                self.db.delete(release)
            else:
                q = self.db.session.query(table).filter_by(releaseID=release.ID)
            if q.count():
                for row in q.all():
                    self.logger.debug('-->self.db drop row->{}->{}.'.format(name, row.ID))
                    self.db.delete(row)

        # Delete files
        nzbpath = self.db.site.filter_by(setting='nzbpath').one().value
        imgpath = os.path.join(config.WWW_DIR, 'covers')
        audiopath = os.path.join(config.WWW_DIR, 'covers', 'audio')

        for f in [os.path.join(nzbpath, release.guid[0], release.guid + '.nzb.gz'),
                  os.path.join(audiopath, release.guid[0], release.guid + '.mp3'),
                  os.path.join(imgpath, release.guid + '_thumb.jpg')]:
            try:
                os.unlink(f)
            except OSError:
                pass
            else:
                self.logger.info('-->file delete->{}.'.format(f))


def do_filter_releases(rfilter, args=None, dry_run=False):
    logging.getLogger('nnpluspy.do_filter_releases')
    logging.info('starting filter: ' + rfilter)
    f = Filters()
    release_filter = getattr(f, rfilter)
    cnt = 0
    for release in release_filter():
        cnt += 1
        if not dry_run:
            f.delete_release(release)

    logging.info('deleted: {} releases.'.format(cnt))
