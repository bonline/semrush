"""Python SEMrush API Wraper.

API V3.0
https://www.semrush.com/api-documentation/
"""
# !/usr/bin/env python

import logging
import requests


engine_database = {
    'google.com': 'us',
    'google.co.uk': 'uk',
    'google.ca': 'ca',
    'google.ru': 'ru',
    'google.de': 'de',
    'google.fr': 'fr',
    'google.es': 'es',
    'google.it': 'it',
    'google.com.br': 'br',
    'google.com.au': 'au',
    'bing.com': 'bing-us',
    'google.com.ar': 'ar',
    'google.be': 'be',
    'google.ch': 'ch',
    'google.dk': 'dk',
    'google.fi': 'fi',
    'google.com.hk': 'hk',
    'google.ie': 'ie',
    'google.co.il': 'il',
    'google.com.mx': 'mx',
    'google.nl': 'nl',
    'google.no': 'no',
    'google.pl': 'pl',
    'google.se': 'se',
    'google.com.sg': 'sg',
    'google.com.tr': 'tr',
    'google.com': 'mobile-us',
    'google.co.jp': 'jp',
    'google.co.in': 'in',
    'google.hu': 'hu',
    'google.af': 'af',
    'google.al': 'al',
    'google.dz': 'dz',
    'google.ao': 'ao',
    'google.am': 'am',
    'google.at': 'at',
    'google.az': 'az',
    'google.bh': 'bh',
    'google.bd': 'bd',
    'google.by': 'by',
    'google.bz': 'bz',
    'google.bo': 'bo',
    'google.ba': 'ba',
    'google.bw': 'bw',
    'google.bn': 'bn',
    'google.bg': 'bg',
    'google.cv': 'cv',
    'google.kh': 'kh',
    'google.cm': 'cm',
    'google.cl': 'cl',
    'google.co': 'co',
    'google.cr': 'cr',
    'google.hr': 'hr',
    'google.cy': 'cy',
    'google.cz': 'cz',
    'google.cd': 'cd',
    'google.do': 'do',
    'google.ec': 'ec',
    'google.eg': 'eg',
    'google.sv': 'sv',
    'google.ee': 'ee',
    'google.et': 'et',
    'google.ge': 'ge',
    'google.gh': 'gh',
    'google.gr': 'gr',
    'google.gt': 'gt',
    'google.gy': 'gy',
    'google.ht': 'ht',
    'google.hn': 'hn',
    'google.is': 'is',
    'google.id': 'id',
    'google.jm': 'jm',
    'google.jo': 'jo',
    'google.kz': 'kz',
    'google.kw': 'kw',
    'google.lv': 'lv',
    'google.lb': 'lb',
    'google.lt': 'lt',
    'google.lu': 'lu',
    'google.mg': 'mg',
    'google.my': 'my',
    'google.mt': 'mt',
    'google.mu': 'mu',
    'google.md': 'md',
    'google.mn': 'mn',
    'google.me': 'me',
    'google.ma': 'ma',
    'google.mz': 'mz',
    'google.na': 'na',
    'google.np': 'np',
    'google.nz': 'nz',
    'google.ni': 'ni',
    'google.ng': 'ng',
    'google.om': 'om',
    'google.py': 'py',
    'google.pe': 'pe',
    'google.ph': 'ph',
    'google.pt': 'pt',
    'google.ro': 'ro',
    'google.sa': 'sa',
    'google.sn': 'sn',
    'google.rs': 'rs',
    'google.sk': 'sk',
    'google.si': 'si',
    'google.za': 'za',
    'google.kr': 'kr',
    'google.lk': 'lk',
    'google.th': 'th',
    'google.bs': 'bs',
    'google.tt': 'tt',
    'google.tn': 'tn',
    'google.ua': 'ua',
    'google.ae': 'ae',
    'google.uy': 'uy',
    'google.ve': 've',
    'google.vn': 'vn',
    'google.zm': 'zm',
    'google.zw': 'zw',
    'google.ly': 'ly'
}


class SemrushClientException(BaseException):

    def __init__(self, error):
        self.error = error

    def __str__(self):
        return repr(self.error)


class SemrushClient(object):

    def __init__(self, key, database='uk'):
        """Initialise SemrushClient.

        key: The key Provide by SEMrush (https://www.semrush.com/api-use/)
        database: A regional database.
        """
        if not key:
            raise SemrushClientException('Valid SEMRush API key required')

        if database not in engine_database.values():
            raise NotImplementedError

        self.url = 'http://api.semrush.com/'
        self.key = key
        self.database = database

    def get_database_from_search_engine(self, search_engine='google.com'):
        if search_engine in engine_database:
            return engine_database[search_engine]
        else:
            raise NotImplementedError

    def get_main_report(self, domain, export_columns='Dn,Rk,Or,Ot,Oc,Ad,At,Ac', display_date=None):
        """DOMAIN OVERVIEW (ONE DATABASE): domain_rank.

        This report provides live or historical data on a domain's keyword rankings
        in both organic and paid search in a chosen regional database.
        """
        if display_date:
            return self._call_report('domain_rank', domain=domain,
                                     export_columns=export_columns, display_date=display_date)
        else:
            return self._call_report('domain_rank', domain=domain, export_columns=export_columns)

    def get_keyword_report(self, phrase):
        """KEYWORD OVERVIEW (ONE DATABASE): phrase_this.

        This report provides a summary of a keyword, including its volume, CPC, competition,
        and the number of results in a chosen regional database.
        """
        return self._call_report('phrase_this', phrase=phrase)

    def get_organic_keywords_report(self, domain,
                                    export_columns='Ph,Po,Pp,Pd,Nq,Cp,Ur,Tr,Tc,Co,Nr,Td',
                                    display_date=None):
        """DOMAIN ORGANIC SEARCH KEYWORDS: domain_organic.

        This report lists keywords that bring users to a domain via Google's top 20 organic search results.
        """
        if display_date:
            return self._call_report('domain_organic', domain=domain,
                                     export_columns=export_columns, display_date=display_date)
        else:
            return self._call_report('domain_organic', domain=domain, export_columns=export_columns)

    def get_adwords_keyword_report(self, domain,
                                   export_columns='Ph,Po,Pp,Pd,Ab,Nq,Cp,Tr,Tc,Co,Nr,Td,Tt,Ds,Vu,Ur',
                                   display_date=None):
        """DOMAIN PAID SEARCH KEYWORDS: domain_adwords.

        This report lists keywords that bring users to a domain via Google's paid search results.
        """
        if display_date:
            return self._call_report('domain_adwords', domain=domain,
                                     export_columns=export_columns, display_date=display_date)
        else:
            return self._call_report('domain_adwords', domain=domain, export_columns=export_columns)

    def get_organic_url_report(self, url, export_columns='Ph,Po,Nq,Cp,Co,Tr,Tc,Nr,Td', display_date=None):
        """URL ORGANIC SEARCH KEYWORDS: url_organic.

        This report lists keywords that bring users to a URL via Google's top 20 organic search results.
        """
        if display_date:
            return self._call_report('url_organic', url=url, export_columns=export_columns, display_date=display_date)
        else:
            return self._call_report('url_organic', url=url, export_columns=export_columns)

    def get_adwords_url_report(self, url, export_columns='Ph,Po,Nq,Cp,Co,Tr,Tc,Nr,Td,Tt,Ds', display_date=None):
        """URL PAID SEARCH KEYWORDSS: url_adwords.

        This report lists keywords that bring users to a URL via Google's paid search results.
        """
        if display_date:
            return self._call_report('url_adwords', url=url, export_columns=export_columns, display_date=display_date)
        else:
            return self._call_report('url_adwords', url=url, export_columns=export_columns)

    def get_competitors_in_organic_search_report(self,
                                                 domain,
                                                 export_columns='Dn,Cr,Np,Or,Ot,Oc,Ad',
                                                 display_date=None):
        """COMPETITORS IN ORGANIC SEARCH: domain_organic_organic.

        This report lists a domain's competitors in organic search results.
        """
        if display_date:
            return self._call_report('domain_organic_organic', domain=domain,
                                     export_columns=export_columns, display_date=display_date)
        else:
            return self._call_report('domain_organic_organic', domain=domain, export_columns=export_columns)

    def get_competitors_in_adwords_search_report(self,
                                                 domain,
                                                 export_columns='Dn,Cr,Np,Ad,At,Ac,Or',
                                                 display_date=None):
        """COMPETITORS IN PAID SEARCH: url_adwords.

        This report lists a domain's competitors in paid search results.
        """
        if display_date:
            return self._call_report('domain_adwords_adwords', domain=domain,
                                     export_columns=export_columns, display_date=display_date)
        else:
            return self._call_report('domain_adwords_adwords', domain=domain, export_columns=export_columns)

    def get_potential_ad_traffic_buyers_report(self, domain):
        """Deprecate on SEMrush API v3.0."""
        return self._call_report('domain_organic_adwords', domain=domain)

    def get_potential_ad_traffic_sellers_report(self, domain):
        """Deprecate on SEMrush API v3.0."""
        return self._call_report('domain_adwords_organic', domain=domain)

    def _call_report(self, report, **kwargs):
        data = self._query(report, **kwargs)
        return self._build_report(data)

    def _build_report(self, data):
        results = []

        lines = data.split('\r')
        columns = lines[0].split(';')

        for line in lines[1:]:
            result = {}
            for i, datum in enumerate(line.split(';')):
                result[columns[i]] = datum.strip('"\n\r\t')
            results.append(result)

        return results

    def _query(self, report, **kwargs):
        """Process the query to SEMrush.

        export_escape: If this parameter uses the value "1",
                       the report's columns will be wrapped in double quotation marks (").
        """
        universal = {
            'database': self.database,
            'type': report,
            'key': self.key,
            'export_escape': 1
        }
        params = universal.items() + kwargs.items()
        logging.info(" - - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - -")
        logging.info("param= %r", params)
        logging.info(" - - - - - - - - - - - - - - - - - -- - - - - - - - - - - - - -")

        response = requests.get(self.url, params=params)

        if response.status_code == 200:
            return response.content
        else:
            raise SemrushClientException(response.content)
