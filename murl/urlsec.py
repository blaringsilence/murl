#!/usr/bin/env python3

# This module deals with the format of URI's
# The general format, citing RFC 3986 (2005), is:
#   scheme:[//[user:password@]host[:port]][/]path[?query][#fragment]
# Pieces inside []'s are optional.
# This module assumes input adheres to the mentioned/standard format.
# The purpose of this module is to:
#   - Take an absolute URI and divide it into its components
#   - Given components, re-assemble a URI
# So basically, parse, cut, and glue together a URI for easier usage by 
# other modules/classes.
# Components:
#   1. scheme (must be separated from rest by :)
#   2. authority* (username*, password*, host, port) (must begin with // 
#      and end either with end of url or / or ? or #)
#   6. path (must begin with / if authority was present, 
#      may begin with / if not, but never //)
#   7. query* (must begin with ?, and is delimited with & or ;)
#   8. fragment* (must begin with #)
# *optional, otherwise = ''

def _getPartEnd(url, possible_ends=['/', '?', '#']):
# Get the a segment of the url, given the url starting from its possible 
# location to the earliest of the ends or the end of the url.
    end = len(url)
    for delim in possible_ends:
        pos = url.find(delim)
        if pos >= 0 and pos < end:
            end = pos
    return end

def _divideAuth(authority):
# Divide the authority part of a URL
    username = password = host = port = ''
    if '@' in authority: # There is an auth part consisting of username/pass
        u_pass = authority.split('@')[0].split(':')
        try:
            username = u_pass[0]
            password = u_pass[1]
        except IndexError as e:
            raise ValueError('There should be a username and a password, '
                            +'but there isn\'t.')
        atPlace = authority.find('@')
        authority = authority[atPlace+1:]

    if authority.startswith(':'):
        raise ValueError('There is no host specified '
            'despite there being an authority part,'
                        + 'or there\'s a colon at the beginning of '
                        + 'the authority without there being an @ '
                        + 'for the authentication.')
    else:
        if ('[' in authority and not ']' in authority) or \
            (']' in authority and not '[' in authority):
            raise ValueError('Host has imbalanced IPv6 brackets.')
        elif authority.startswith('[') and ']' in authority:
            lastBracket = authority.find(']')
            host = authority[:lastBracket+1]
            authority = authority[lastBracket+1:]
        colonPlace = authority.find(':')
        if colonPlace == -1:
            host = authority if host == '' else host
        elif authority.count(':') == 1 and len(authority) > colonPlace + 1:
            host = authority[:colonPlace] if host == '' else host
            port = int(authority[colonPlace+1:])
            if port < 0 or port > 65536:
                raise ValueError('Port number should be between '
                                +'0 and 65536 inclusive.')
        elif authority.count(':') > 1:
            raise ValueError('Too many colons in this host, '
                            + 'maybe you forgot an @?')
    return dict(username=username, password=password, host=host, port=port)
    
def _divideQuery(querystring):
# Divide query string into dict of keys and values if it's divided by & or ;, 
# otherwise, will try to divide into single keyvvalue pair, otherwise will
# present as is.
    qSplit = [querystring]

    if '&' in querystring:
        qSplit = querystring.split('&')
    elif ';' in querystring:
        qSplit = querystring.split(';')

    result = {}
    i = 0

    for pair in qSplit:
        eqPlace = pair.find('=')
        if eqPlace < 0: # if not found
            result[i] = pair
        elif eqPlace == 0:
            result[i] = '' if len(pair) == 1 else pair[1:]
        else:
            key = pair[:eqPlace].lower()
            result[key] = '' if len(pair) == len(key) + 1 else pair[eqPlace+1:]
        i+=1

    return result



def divideURL(url): 
    scheme = authority = path = query = fragment = ''
    hasPath = True

    # first, the scheme
    first_delim = url.find(':')
    if first_delim > 0:
        scheme = url[:first_delim].lower()

    # throw away scheme and ':'
    url = url[first_delim+1:] if first_delim >= 0 else url

    # second, authority
    if url[:2] == '//':
        url = url[2:]
        authorityEnd = _getPartEnd(url)
        authority = _divideAuth(url[:authorityEnd])
        url = url[authorityEnd:]
        if not url.startswith('/') or len(url) <= 1: # you do not have a path
            hasPath = False
        elif len(url) > 0:
            url = url[1:] # Remove forward slash
    
    if hasPath and len(url) > 0: # you have a path
        pathEnd = _getPartEnd(url, ['?', '#'])
        path = url[:pathEnd]
        url = url[pathEnd:]

    if url.startswith('?') and len(url) > 1: # you have a querystring
        queryEnd = _getPartEnd(url[1:], '#')
        query = _divideQuery(url[1:queryEnd+1])
        url = url[queryEnd+1:]

    if url.startswith('#') and len(url) > 1: # you have a fragment
        fragment = url[1:]
        

    return dict(scheme=scheme, 
                authority=authority,
                path=path,
                query=query,
                fragment=fragment
                )

def _ifNotEmptyAdd(what, addition):
    res = ''
    if what != '':
        res += addition
    return res

def _assembleQuery(querydict, queryDelim):
    res = ''
    i = 0
    for key in querydict:
        k = ''
        if type(key) is not int:
            k = key
        v = querydict[key]
        res+='='.join((k,v))
        if i != len(querydict) - 1:
            res+=queryDelim
        i+=1
    return res

def _assemblePath(authority, path):
    if authority != '' and not path.startswith('/'):
        return '/' + path
    else:
        return path

def assembleURL(urldict, queryDelim='&'):
# Re-assemble a URL dict divided by this same module (or uses same syntax)
    res = ''
    res += _ifNotEmptyAdd(urldict['scheme'], urldict['scheme'] + ':')
    if urldict['authority'] != '':
        res += ('//' 
            + _ifNotEmptyAdd(urldict['authority']['username'], 
                            urldict['authority']['username'] + ':' 
                            + urldict['authority']['password'] + '@')
            + _ifNotEmptyAdd(urldict['authority']['host'], 
                            urldict['authority']['host'])
            + _ifNotEmptyAdd(urldict['authority']['port'], 
                            ':' + str(urldict['authority']['port']))
            )
    res += _ifNotEmptyAdd(urldict['path'],
                         _assemblePath(urldict['authority'], urldict['path']))
    res += _ifNotEmptyAdd(urldict['query'], 
                        '?' + _assembleQuery(urldict['query'], queryDelim))
    res += _ifNotEmptyAdd(urldict['fragment'], '#' + urldict['fragment'])
    return res
