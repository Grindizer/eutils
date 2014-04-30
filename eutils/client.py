import os

from eutils.exceptions import *
from eutils.queryservice import QueryService
from eutils.xmlfacades.dbsnp import ExchangeSet
from eutils.xmlfacades.einfo import EInfo, EInfoDB
from eutils.xmlfacades.esearchresults import ESearchResults
from eutils.xmlfacades.gbset import GBSet
from eutils.xmlfacades.gene import Gene
from eutils.xmlfacades.pubmed import PubMedArticle, PubMedArticleSet

default_cache_path = os.path.join(os.path.expanduser('~'),'.cache','eutils-cache.db')


class Client(object):

    def __init__(self,
                 cache_path=default_cache_path,
                 request_interval=0.4
                 ):
        self._qs = QueryService(cache_path=cache_path, request_interval=request_interval)
        #self.databases = self.einfo().databases


    def einfo(self,db=None):
        """query the einfo endpoint

        :param db: string (optional)
        :rtype: EInfo or EInfoDB object

        If db is None, the reply is a list of databases, which is returned
        in an EInfo object (which has a databases() method).

        If db is not None, the reply is information about the specified
        database, which is returned in an EInfoDB object.  (Version 2.0
        data is automatically requested.)
        """

        if db is None:
            return EInfo( self._qs.einfo() )
        return EInfoDB( self._qs.einfo({'db':db, 'version':'2.0'}) )
        

    def esearch(self, db, term, **kw):
        """query the esearch endpoint
        """
        kw.update({'db':db,'term':term})
        return ESearchResults( self._qs.esearch(kw) )


    def efetch(self, db, id=None, webenv=None, query_key=None, **kw):
        """query the efetch endpoint
        """
        db = db.lower()
        kw.update({'db':db})
        if id:
            kw.update({'id': id})
        else:
            kw.update({'webenv': webenv, 'query_key': query_key})
        xml = self._qs.efetch(kw)
        if db in ['gene']:
            return Gene(xml)
        if db in ['nuccore']:
            # TODO: GBSet is misnamed; it should be GBSeq and get the GBSeq XML node as root (see gbset.py)
            return GBSet(xml)
        if db in ['pubmed']:
            return PubMedArticleSet(xml)
        if db in ['snp']:
            return ExchangeSet(xml)
        raise EutilsError('database {db} is not currently supported by eutils'.format(db=db))
