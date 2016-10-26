#!/usr/bin/env python3
from . import urlsec, urlende
import re
import pkg_resources

class Murl(object):
    def __init__(self, url='', queryDelim='&', isTemplate=False):
        self._attrs = urlsec.divideURL(url, queryDelim)
        self._queryDelim = queryDelim
        self.isTemplate = isTemplate

    def __str__(self):
        return urlsec.assembleURL(self._attrs, self.queryDelim)

    @property
    def queryDelim(self):
        return self._queryDelim
    
    @queryDelim.setter
    def queryDelim(self, val):
        self._queryDelim = val

    @property
    def scheme(self):
        return self._attrs['scheme']

    @scheme.setter
    def scheme(self, val):
        val = val.lower()
        if re.match(r'^([a-z]+)([a-z]|\d|\+|\.|\-)*$', val) is None:
            raise ValueError('Scheme has to start with a letter, followed by '
                            + 'letters, digits, +, ., or -.')
        else:
            self._attrs['scheme'] = val

    def _getAuthProperty(self, prop):
        return None if self._attrs['authority'] == '' or \
        self._attrs['authority'][prop] == '' else self._attrs['authority'][prop]

    def _setAuthProperty(self, prop, val):
        other = 'password' if prop == 'username' else 'username'
        if self._attrs['authority'] == '':
            raise ValueError('This URI has no host specified. Add one using the'
                            + ' \'host\' property.')
        elif prop != 'port' and self._attrs['authority'][other] == '':
            raise ValueError('This URI has no ' + other + ' already set. To set'
                            +' both, use  the \'auth\' property.')
        else: 
            self._attrs['authority'][prop] = val

    @property
    def host(self):
        return self._getAuthProperty('host')

    @host.setter
    def host(self, val):
        if self._attrs['authority'] == '':
            username = password = port = ''
            self._attrs['authority'] = dict(username=username, 
                                            password=password, 
                                            port=port,
                                            host=val
                                            )
        else:
            if ('[' in val and not ']' in val) or \
                (']' in val and not '[' in val):
                raise ValueError('Host has imbalanced IPv6 brackets.')
            self._attrs['authority']['host'] = val.lower()

    @property
    def domain(self):
        IPv4 = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}' \
             + r'(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
        if self.host is None or '[' in self.host or \
        re.match(IPv4, self.host) is not None:
            return self.host
        else: # not None, IPv6 or IPv4
        # We want to extract the domain + public suffix
            LOC = 'data/public_suffix_list.dat'
            DATA_PATH = pkg_resources.resource_filename(__name__, LOC)
            content = open(DATA_PATH)
            public_suffix = ''
            for i, line in enumerate(content):
                if not line.startswith('//') and not line.startswith('\n'):
                    suffix = '.' + line.split('\n')[0]
                    if suffix in self.host and \
                    self.host.rfind(suffix) + len(suffix) == len(self.host) and \
                     len(public_suffix) < len(suffix):
                        public_suffix = suffix
            
            if public_suffix != '':
                beginSuffix = self.host.rfind(public_suffix)
                beginDomain = self.host.rfind('.', 0, beginSuffix)
                return self.host[beginDomain+1:]
            else: # if no public suffix available, return entire host
                return self.host

    @domain.setter
    def domain(self, val):
        raise ValueError('Cannot set domain. Can, however, set entire host. '
                        + 'Use the \'host\' property to do that.')
    

    @property
    def auth(self):
        notFound = self._attrs['authority'] == '' or \
                   self._attrs['authority']['username'] == ''
        return None if notFound \
                else dict(username = self._attrs['authority']['username'],
                         password = self._attrs['authority']['password'])

    @auth.setter
    def auth(self, authdict):
        if self._attrs['authority'] == '':
            raise ValueError('Cannot add authentication without host. '
                            +'Add host using the \'host\' property.')
        elif type(authdict) is dict and 'username' in authdict and \
            'password' in authdict:
            self._attrs['authority']['username'] = authdict['username']
            self._attrs['authority']['password'] = authdict['password'] 
        else:
            raise ValueError('Auth value must be a dict with the keys '
                            +'\'username\' and \'password\'.')
    
    @property
    def username(self):
        return self._getAuthProperty('username')

    @username.setter
    def username(self, val):
        self._setAuthProperty('username', val)

    @property
    def password(self):
        return self._getAuthProperty('password')

    @password.setter
    def password(self, val):
        self._setAuthProperty('password', val)

    @property
    def port(self):
        return self._getAuthProperty('port')    

    @port.setter
    def port(self, val):
        self._setAuthProperty('port', val)

    @property
    def path(self):
        return None if self._attrs['path'] == '' else self._attrs['path']
    
    @path.setter
    def path(self, val, encoded=False):
        if val.startswith('//'):
            raise ValueError('Path cannot start with two forward slashes.')
        self._attrs['path'] = val if encoded else urlende.encode(val)

    def addQuery(self, key, val, encode=True, spaceIsPlus=True):
        oldQ = self._attrs['query']
        key = urlende.encode_query(key, spaceIsPlus) if encode else key 
        val = urlende.encode_query(val, spaceIsPlus) if encode else val
        if oldQ == '': # empty
            temp = {}
            temp[key.lower()] = [val]
            self._attrs['query'] = temp
        elif key.lower() in self._attrs['query']:
            self._attrs['query'][key.lower()].append(val)
        else:
            self._attrs['query'][key.lower()] = [val]

    def getQuery(self, key, decodeVal=True, keyEncoded=False, spaceIsPlus=True):
        if self._attrs['query'] != '':
            key = key if keyEncoded else urlende.encode_query(key, spaceIsPlus)
            arr = self._attrs['query'][key.lower()]
            res = [] if decodeVal else arr
            if decodeVal:
                for val in arr:
                    enc = urlende.decode_query(val, spaceIsPlus)
                    res.append(enc)
            return res
        else:
            raise KeyError('Key does not exist.')

    def removeQuery(self, key, keyEncoded=False, spaceIsPlus=True):
    # Will raise a KeyError if not a key that exists
        key = key if keyEncoded else urlende.encode_query(key, spaceIsPlus)
        if self._attrs['query'] != '' and key in self._attrs['query']:
            del self._attrs['query'][key.lower()]
            if len(self._attrs['query']) == 0:
                self._attrs['query'] = ''
        else:
            raise KeyError('This key does not exist.')


    @property
    def queryString(self):
        return '?' \
                + urlsec._assembleQuery(self._attrs['query'], self.queryDelim)

    @property
    def fragment(self):
        return None if self._attrs['fragment'] == '' \
                else self._attrs['fragment']

    @fragment.setter
    def fragment(self, val, encoded=False):
        self._attrs['fragment'] = val if encoded \
                                else urlende.encode(val, safe='')